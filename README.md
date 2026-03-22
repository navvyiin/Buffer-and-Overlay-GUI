# Buffer & Overlay GUI

An interactive GIS application for buffer zone and overlay analysis, built with Streamlit. Upload your spatial data or pull road networks directly from OpenStreetMap, run the analysis, and explore results on a live map.

---

## What It Does

- Upload parcel and road data (Shapefile ZIP or GeoJSON), or fetch roads from OpenStreetMap
- Select one or more buffer distances and run buffer zone analysis
- Detect and visualise intersecting parcels on an interactive map
- Download results as Shapefile ZIPs for use in QGIS or ArcGIS

---

## Who It Is For

Urban planners, environmental analysts, land use researchers, and anyone who needs quick spatial proximity analysis without writing GIS code from scratch.

---

## Getting Started

**Requirements:** Python 3.8 or above

```bash
git clone https://github.com/navvyiin/Buffer-and-Overlay-GUI.git
cd Buffer-and-Overlay-GUI
pip install -r requirements.txt
streamlit run streamlit_buffer_overlay_app.py
```

Then open the app in your browser, upload your data from the sidebar, set your buffer distances, and run the analysis.

---

## Supported Formats

| Input | Output |
|-------|--------|
| Shapefile (`.zip`) | Shapefile ZIP (buffer layers) |
| GeoJSON (`.geojson`) | Shapefile ZIP (intersecting parcels) |

---

## Tech Stack

`Streamlit` `GeoPandas` `OSMnx` `Folium` `streamlit-folium`

---

## Project Structure

```
Buffer-and-Overlay-GUI/
├── streamlit_buffer_overlay_app.py
├── requirements.txt
├── README.md
└── sample_data/
```

---

## Notes

- Processing time scales with dataset size and buffer complexity
- Best suited for exploratory and lightweight GIS workflows
- Large road networks or very wide buffer distances may take a moment to process

---

## Planned Improvements

- Spatial indexing for faster processing on large datasets
- GeoJSON and CSV export options
- Improved UI layout
- Automated tests

---

## License

MIT License. © 2026 navvyiin
