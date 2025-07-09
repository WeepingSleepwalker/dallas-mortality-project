import geopandas as gpd

gdf = gpd.read_file("outputs/dallas_zcta_filtered.shp")
print(gdf.columns)