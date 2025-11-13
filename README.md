# Buffer-and-Overlay-GUI
This Streamlit app performs buffer zone and overlay analysis on road and parcel data. Users can upload or fetch OSM roads, select buffer distances, visualize results interactively, and download intersecting parcels and buffer layers as shapefiles for GIS analysis.

## Buffer & Overlay Analysis Tool
This tool enables GIS buffer zone and overlay analysis using Streamlit.  
Users can upload parcel and road data (shapefile ZIP/GeoJSON) or fetch roads via OSM, select buffer distances, and visualize intersecting parcels interactively on a map.  
Results are downloadable as shapefiles for further GIS processing.

### Features
- Upload or fetch road network data  
- Select and compare multiple buffer distances  
- View parcel-road intersections on interactive folium map  
- Download buffer and intersection layers (shapefile ZIP)

### Usage
1. Install packages from `requirements.txt`  
2. Run with:  
   `streamlit run streamlit_buffer_overlay_app.py`  
3. Follow the interface to upload data, set parameters, and download results

### Requirements
- Python 3.8+  
- Dependencies: Streamlit, GeoPandas, Folium, OSMnx, streamlit_folium

### Applications
- Urban planning  
- Environmental impact studies  
- Land parcel analysis

For more details, see code and comments in `streamlit_buffer_overlay_app.py`.
