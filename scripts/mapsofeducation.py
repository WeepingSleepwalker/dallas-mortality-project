import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os

# === Paths ===
shapefile_path = "outputs/dallas_zcta_filtered.shp"
census_path = "data/dallas_zip_demographics.csv"
output_path = "outputs/maps_by_year/education_map.png"
os.makedirs("outputs/maps_by_year", exist_ok=True)

# === Load shapefile ===
print("Loading shapefile...")
zcta_gdf = gpd.read_file(shapefile_path)
zcta_gdf["GEOID20"] = zcta_gdf["GEOID20"].astype(str).str.zfill(5)
zcta_gdf["label_point"] = zcta_gdf.representative_point()

# === Load education data ===
print("Loading census data...")
census_df = pd.read_csv(census_path)
census_df["zip"] = census_df["zip"].apply(lambda x: str(int(float(x))).zfill(5))

# === Merge ===
merged = zcta_gdf.merge(census_df, left_on="GEOID20", right_on="zip", how="left")

# === Filter ZIPs with 30%+ bachelor's for labels ===
label_df = merged[merged["percent_bachelor_or_higher"] > 30]

# === Plot ===
fig, ax = plt.subplots(1, 1, figsize=(18, 16))  # Larger canvas
merged.plot(
    column="percent_bachelor_or_higher",
    cmap="Purples",
    linewidth=0.5,
    edgecolor="gray",
    legend=True,
    ax=ax,
    legend_kwds={"label": "% with Bachelor’s Degree or Higher", "shrink": 0.6}
)

# Add ZIP code labels only for selected areas
for _, row in label_df.iterrows():
    if pd.notnull(row["label_point"]) and pd.notnull(row["GEOID20"]):
        x, y = row["label_point"].x, row["label_point"].y
        ax.text(x, y, row["GEOID20"], fontsize=6.5, ha='center', va='center', color='black')

ax.set_title("Dallas ZIP Code Education Map\n% with Bachelor’s Degree or Higher", fontsize=18)
ax.axis("off")

plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"✅ Saved readable map: {output_path}")
