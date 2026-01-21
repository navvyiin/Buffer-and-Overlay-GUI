# 🗺️ Buffer & Overlay GUI

**Buffer & Overlay GUI** is an interactive **Streamlit-based GIS application** for performing **buffer zone and overlay analysis** on road and parcel data.
It allows users to upload spatial datasets or fetch roads from **OpenStreetMap**, visualize spatial intersections on an interactive map, and download analysis results for further GIS processing.

---

## ✨ Key Features

* 📂 Upload **parcel and road data** (Shapefile ZIP or GeoJSON)
* 🌍 Fetch road networks directly from **OpenStreetMap (OSM)**
* 📏 Create and compare **multiple buffer distances**
* 🔄 Perform **overlay / intersection analysis**
* 🗺️ Visualize results on an **interactive Folium map**
* 📥 Download **buffer zones and intersecting parcels** as Shapefile ZIPs

---

## 🖥️ Demo Workflow

1. Upload parcel data and road data *or* fetch roads via OSM
2. Select one or more buffer distances
3. Run buffer and overlay analysis
4. Explore results on an interactive map
5. Download processed layers for use in GIS software (QGIS, ArcGIS)

---

## 📦 Installation

### Prerequisites

* **Python 3.8+**
* pip or virtual environment recommended

### Setup

```bash
git clone https://github.com/navvyiin/Buffer-and-Overlay-GUI.git
cd Buffer-and-Overlay-GUI
pip install -r requirements.txt
```

---

## ▶️ Usage

Start the Streamlit application:

```bash
streamlit run streamlit_buffer_overlay_app.py
```

Then:

* Use the sidebar to upload data or fetch OSM roads
* Configure buffer distances
* Run the analysis and download results

---

## 🧰 Supported Data Formats

* **Input**

  * Shapefile (`.zip`)
  * GeoJSON (`.geojson`)
* **Output**

  * Shapefile ZIP (buffer layers & intersecting parcels)

---

## 🧠 Applications

This tool is useful for:

* 🏙️ Urban and regional planning
* 🌱 Environmental impact analysis
* 🏡 Land parcel and zoning analysis
* 🛣️ Infrastructure proximity studies
* 📊 Rapid GIS prototyping and teaching

---

## ⚙️ Technologies Used

* **Streamlit** – Web UI
* **GeoPandas** – Spatial processing
* **OSMnx** – OpenStreetMap road data
* **Folium** – Interactive maps
* **streamlit-folium** – Streamlit–Folium integration

---

## 📁 Project Structure

```
Buffer-and-Overlay-GUI/
├── streamlit_buffer_overlay_app.py
├── requirements.txt
├── README.md
└── sample_data/
```

---

## ⚠️ Notes & Limitations

* Performance depends on dataset size
* Large buffers or dense road networks may take longer to process
* Recommended for exploratory and lightweight GIS workflows

---

## 🛠️ Future Improvements (Planned)

* ⏱️ Performance optimization for large datasets
* 📍 Spatial indexing support
* 🎨 Improved UI layout and theming
* 📤 Export to GeoJSON and CSV
* 🧪 Automated tests

---

## 📄 License

MIT License
© 2026 navvyiin

---

## 🤝 Contributing

Contributions are welcome!
Feel free to open an issue or submit a pull request with improvements, fixes, or feature ideas.
