# 🧠 Script Overview

Here's a quick breakdown of the main scripts and what each one does:

### `main.py` *(or your notebook)*
- **Purpose:** Central pipeline that loads, processes, merges, and visualizes mortality data.
- **What it does:**
  - Loads ZIP-level shapefiles using GeoPandas
  - Reads cleaned demographic + death CSV data
  - Merges shapefile geometry with death rate statistics
  - Plots a choropleth map colored by death rate per 1,000 people
  - Saves output to `outputs/` folder

---

### `scripts/clean_demographics.py`
- **Purpose:** Cleans raw census ZIP code demographic data
- **Key actions:**
  - Converts ZIPs to string format (with zero-padding)
  - Handles nulls, converts percentages, renames columns

---

### `scripts/clean_deaths.py`
- **Purpose:** Processes death count and rate data
- **Key actions:**
  - Standardizes ZIP and year formats
  - Calculates rates if needed
  - Filters or aggregates multi-year data

---

### `scripts/merge_data.py`
- **Purpose:** Joins death data and demographic data by ZIP
- **Key actions:**
  - Left-joins cleaned census and mortality data on ZIP
  - Validates against shapefile ZIPs for geospatial join

---

### `scripts/plot_map.py`
- **Purpose:** Creates the final choropleth map
- **Key actions:**
  - Uses GeoPandas + Matplotlib to visualize the merged GeoDataFrame
  - Allows for color scaling, zooming, and saving map to file

---

### `scripts/utils.py`
- **Purpose:** Utility functions for file loading, formatting, etc.
- **What it helps with:**
  - Dynamic file paths
  - Logging and debug prints
  - Year selection or ZIP filtering

