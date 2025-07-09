import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Use the filtered Dallas ZCTA shapefile
shapefile_path = "outputs/dallas_zcta_filtered.shp"
zcta_gdf = gpd.read_file(shapefile_path)

# Load your demographic + mortality dataset
csv_path = "data/zip_yearly_death_estimates.csv"  # or your merged CSV if you renamed it
mortality_df = pd.read_csv(csv_path)

# Format ZIPs to match


# Fix zip formatting in the CSV
mortality_df["zip"] = mortality_df["zip"].astype(float).astype(int).astype(str).str.zfill(5)
zcta_gdf["GEOID20"] = zcta_gdf["GEOID20"].astype(str)

# Now merge
merged = zcta_gdf.merge(mortality_df, left_on="GEOID20", right_on="zip")
print("Merged rows:", len(merged))
print("Geometry valid:", merged.geometry.notnull().sum())
print(mortality_df["zip"].head())
print(mortality_df["zip"].dtype)
# === Diagnostic Checks ===
print("📊 Death Rate Stats:")
print(merged["death_rate_per_1000"].describe())  # Option 1

print("\n🔍 Unique Death Rate Values:")
print(merged["death_rate_per_1000"].unique())    # Option 2
print(mortality_df[["year"]].drop_duplicates())


# Plotting
fig, ax = plt.subplots(1, 1, figsize=(12, 10))
merged.plot(
    column='death_rate_per_1000',
    cmap='OrRd',
    linewidth=0.5,
    ax=ax,
    edgecolor='0.9',
    legend=True
)
ax.set_title('Dallas Area: Death Rate per 1,000 Residents by Zip Code', fontsize=14)
ax.axis('off')
plt.tight_layout()
plt.show()
