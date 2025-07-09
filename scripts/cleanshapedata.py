import geopandas as gpd

# Path to your ZCTA shapefile
shapefile_path = "shapefiles/tl_2022_us_zcta520/tl_2022_us_zcta520.shp"

# Load shapefile
zcta_gdf = gpd.read_file(shapefile_path)

# Ensure ZIP code column is string
zcta_gdf["ZCTA5CE20"] = zcta_gdf["ZCTA5CE20"].astype(str)

# Filter for Dallas-area ZIPs
dallas_zcta = zcta_gdf[zcta_gdf["ZCTA5CE20"].str.startswith(("750", "751", "752", "753"))].copy()

# Rename for merge consistency
dallas_zcta = dallas_zcta.rename(columns={"ZCTA5CE20": "zip"})

# Save cleaned output (Shapefile + GeoJSON)
dallas_zcta.to_file("outputs/dallas_zcta_filtered.shp")
dallas_zcta.to_file("outputs/dallas_zcta_filtered.geojson", driver="GeoJSON")

print(f"Saved {len(dallas_zcta)} Dallas-area ZCTAs.")
