import streamlit as st
st.set_option("client.showErrorDetails", False)
from streamlit_folium import st_folium
import folium
import geopandas as gpd
import tempfile
import zipfile
import io
import os
import osmnx as ox

st.set_page_config(layout="wide", page_title="Buffer & Overlay Tool")

# ----------------- Helper Functions -----------------

def read_vector_upload(uploaded_file):
    """Robustly read an uploaded vector file (ZIP shapefile or GeoJSON). Returns GeoDataFrame in EPSG:32643."""
    if uploaded_file is None:
        return None

    name = uploaded_file.name.lower()

    if name.endswith(".zip"):
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                zip_path = os.path.join(tmpdir, "uploaded.zip")
                with open(zip_path, "wb") as f:
                    f.write(uploaded_file.read())
                with zipfile.ZipFile(zip_path, "r") as z:
                    z.extractall(tmpdir)
                shp_files = [os.path.join(tmpdir, f) for f in os.listdir(tmpdir) if f.endswith(".shp")]
                if not shp_files:
                    st.error("No .shp file found in uploaded ZIP.")
                    return None
                gdf = gpd.read_file(shp_files[0])
            except Exception as e:
                st.error(f"Error reading shapefile ZIP: {e}")
                return None

    elif name.endswith(".geojson") or name.endswith(".json"):
        try:
            gdf = gpd.read_file(uploaded_file)
        except Exception as e:
            st.error(f"Error reading GeoJSON: {e}")
            return None
    else:
        st.error("Unsupported file type. Please upload a ZIP shapefile or GeoJSON.")
        return None

    if gdf.crs is None:
        gdf.set_crs(epsg=32643, inplace=True)
    else:
        gdf = gdf.to_crs(epsg=32643)
    return gdf

def fetch_roads_from_place(place_name, network_type="all_private"):
    """Fetch road network edges for a given place name (EPSG:32643)."""
    try:
        G = ox.graph_from_place(place_name, network_type=network_type)
        gdf_edges = ox.graph_to_gdfs(G, nodes=False, edges=True).reset_index(drop=True)
        gdf_edges = gdf_edges.to_crs(epsg=32643)
        return gdf_edges
    except Exception as e:
        st.error(f"Error fetching OSM data: {e}")
        return None

def ensure_utm(gdf):
    """Project to metric CRS appropriate for centroid (UTM zone) for buffering."""
    centroid = gdf.unary_union.centroid
    lon, lat = centroid.x, centroid.y
    utm_zone = int((lon + 180) / 6) + 1
    epsg = 32600 + utm_zone if lat >= 0 else 32700 + utm_zone
    try:
        gdf_m = gdf.to_crs(epsg=epsg)
        return gdf_m, epsg
    except Exception:
        gdf_m = gdf.to_crs(epsg=3857)
        return gdf_m, 3857

def make_buffer(roads_gdf, distance_m):
    """Return buffer GeoDataFrame (EPSG:32643)."""
    roads_m, epsg = ensure_utm(roads_gdf)
    dissolved = roads_m.unary_union
    buf = gpd.GeoSeries([dissolved.buffer(distance_m)], crs=roads_m.crs)
    buf_gdf = gpd.GeoDataFrame({"geometry": buf})
    buf_gdf = buf_gdf.to_crs(epsg=32643)
    return buf_gdf

def count_intersecting_parcels(parcels_gdf, buffer_gdf):
    """Count parcels that intersect buffer."""
    intersects = parcels_gdf.geometry.intersects(buffer_gdf.unary_union)
    return int(intersects.sum()), parcels_gdf[intersects]

def save_gdf_as_shapefile_zipped(gdf, filename_prefix):
    """Save GeoDataFrame as zipped shapefile and return bytes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        shp_path = os.path.join(tmpdir, f"{filename_prefix}.shp")
        gdf.to_file(shp_path, driver="ESRI Shapefile")
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in os.listdir(tmpdir):
                zf.write(os.path.join(tmpdir, f), arcname=f)
        zip_buffer.seek(0)
        return zip_buffer.read()

def folium_style(feature, color="#3388ff", weight=2, fill=False):
    return {"color": color, "weight": weight, "fill": fill, "fillOpacity": 0.5}

# ----------------- Streamlit Interface -----------------

st.title("Buffer Zone & Overlay Analysis")
st.markdown("Create buffer zones around roads and find intersecting parcels. Download results as shapefiles for further analysis.")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("Input data")
    uploaded_parcels = st.file_uploader(
        "Upload parcels (shapefile ZIP or GeoJSON)",
        type=["zip", "geojson", "json", "shp"]
    )
    parcels_gdf = read_vector_upload(uploaded_parcels)

    st.markdown("---")
    st.write("Roads input:")
    road_option = st.radio(
        "Choose roads source",
        ["Upload roads file", "Fetch from OSM by place name"],
        index=1
    )

    uploaded_roads = None
    roads_gdf = None

    if road_option == "Upload roads file":
        uploaded_roads = st.file_uploader(
            "Upload roads (shapefile ZIP or GeoJSON)",
            type=["zip", "geojson", "json", "shp"]
        )
        roads_gdf = read_vector_upload(uploaded_roads)
    else:
        place_name = st.text_input('Enter place name (e.g. "Bengaluru, India"):')
        if st.button("Fetch roads from OSM"):
            if place_name.strip() == "":
                st.error("Please enter a place name.")
            else:
                with st.spinner("Fetching roads from OSM..."):
                    roads_gdf = fetch_roads_from_place(place_name)

    st.markdown("---")
    st.write("Buffer options (meters)")
    buffer_choices = [10, 50, 100, 200, 250]
    selected_buffer = st.selectbox("Select buffer distance", buffer_choices, index=2)

    st.write("Or choose multiple buffers for comparison:")
    multi_select_buffers = st.multiselect(
        "Select additional distances (optional)",
        buffer_choices,
        default=[selected_buffer]
    )

    if selected_buffer not in multi_select_buffers:
        multi_select_buffers.insert(0, selected_buffer)

with col2:
    st.header("Map & Actions")
    show_osm = st.checkbox("Show OSM base layer", value=True)
    run_button = st.button("Run buffer & overlay")

# ----------------- Processing -----------------

if run_button:
    if roads_gdf is None:
        st.error("Roads data is required. Upload or fetch roads first.")
        st.stop()
    if parcels_gdf is None:
        st.error("Parcels data is required. Upload parcels first.")
        st.stop()

    st.success("Processing...")

    # Geometry safety check
    for name, gdf in [("roads", roads_gdf), ("parcels", parcels_gdf)]:
        if gdf is not None:
            if "geometry" not in gdf.columns:
                geom_col = [c for c in gdf.columns if gdf[c].apply(lambda x: hasattr(x, "geom_type")).any()]
                if geom_col:
                    gdf.rename(columns={geom_col[0]: "geometry"}, inplace=True)
                else:
                    st.error(f"The {name} layer has no geometry column.")
                    st.stop()
            if not isinstance(gdf, gpd.GeoDataFrame):
                gdf = gpd.GeoDataFrame(gdf, geometry="geometry", crs="EPSG:32643")

    roads_gdf = roads_gdf.to_crs(epsg=32643)
    parcels_gdf = parcels_gdf.to_crs(epsg=32643)

    # Compute map center
    try:
        display_ref = (
            parcels_gdf.to_crs(epsg=4326)
            if parcels_gdf is not None and not parcels_gdf.empty
            else roads_gdf.to_crs(epsg=4326)
        )
        minx, miny, maxx, maxy = display_ref.total_bounds
        center = [(miny + maxy) / 2, (minx + maxx) / 2]
    except Exception:
        center = [20.5937, 78.9629]

    # Create folium map
    m = folium.Map(location=center, zoom_start=13, control_scale=True, tiles="OpenStreetMap")

    # Add alternative tiles
    folium.TileLayer(
        tiles="CartoDB positron",
        name="Carto Light",
        attr="© OpenStreetMap contributors © CARTO",
    ).add_to(m)

    folium.TileLayer(
        tiles="Stamen Terrain",
        name="Terrain",
        attr="Map tiles by Stamen Design, under CC BY 3.0 — Data © OpenStreetMap contributors",
    ).add_to(m)

    folium.TileLayer(
        tiles="Stamen Toner",
        name="Toner",
        attr="Map tiles by Stamen Design, under CC BY 3.0 — Data © OpenStreetMap contributors",
    ).add_to(m)

    # Display layers
    parcels_display = parcels_gdf.to_crs(epsg=4326)
    roads_display = roads_gdf.to_crs(epsg=4326)

    if not parcels_display.empty:
        folium.GeoJson(
            parcels_display.to_json(),
            name="Parcels",
            style_function=lambda feat: {"color": "#800026", "weight": 1, "fill": True, "fillOpacity": 0.4},
        ).add_to(folium.FeatureGroup(name="Parcels", show=True).add_to(m))

    if not roads_display.empty:
        folium.GeoJson(
            roads_display.to_json(),
            name="Roads",
            style_function=lambda feat: {"color": "#08519c", "weight": 2},
        ).add_to(folium.FeatureGroup(name="Roads", show=True).add_to(m))

    # Buffers and intersections
    results = []
    for dist in multi_select_buffers:
        buf_gdf = make_buffer(roads_gdf, dist)
        count, intersect_gdf = count_intersecting_parcels(parcels_gdf, buf_gdf)
        results.append({"distance_m": dist, "buffer": buf_gdf, "intersections": intersect_gdf, "count": count})

        buf_disp = buf_gdf.to_crs(epsg=4326)
        inter_disp = intersect_gdf.to_crs(epsg=4326)

        folium.GeoJson(
            buf_disp.to_json(),
            name=f"Buffer {dist} m",
            style_function=lambda feat: folium_style(feat, color="#FEB24C", weight=1, fill=True),
        ).add_to(folium.FeatureGroup(name=f"Buffer {dist} m", show=(dist == selected_buffer)).add_to(m))

        if not inter_disp.empty:
            folium.GeoJson(
                inter_disp.to_json(),
                name=f"Intersection {dist} m",
                style_function=lambda feat: folium_style(feat, color="#238b45", weight=1, fill=True),
            ).add_to(folium.FeatureGroup(name=f"Intersection {dist} m", show=(dist == selected_buffer)).add_to(m))

    folium.LayerControl().add_to(m)
    st.subheader("Interactive map")

    with st.spinner("Rendering interactive map..."):
        st_data = st_folium(m, width=900, height=600, key="main_map", returned_objects=[])

    st.subheader("Results")
    for r in results:
        st.write(f"Buffer: {r['distance_m']} m — Parcels intersecting: {r['count']}")
        colA, colB = st.columns(2)
        with colA:
            if not r["buffer"].empty:
                shp_bytes = save_gdf_as_shapefile_zipped(r["buffer"], f"buffer_{r['distance_m']}m")
                st.download_button(
                    label=f"Download buffer {r['distance_m']}m (shapefile .zip)",
                    data=shp_bytes,
                    file_name=f"buffer_{r['distance_m']}m.zip",
                )
        with colB:
            if not r["intersections"].empty:
                shp_bytes = save_gdf_as_shapefile_zipped(r["intersections"], f"intersection_{r['distance_m']}m")
                st.download_button(
                    label=f"Download intersection {r['distance_m']}m (shapefile .zip)",
                    data=shp_bytes,
                    file_name=f"intersection_{r['distance_m']}m.zip",
                )

    st.success("Done — download layers using the buttons above.")