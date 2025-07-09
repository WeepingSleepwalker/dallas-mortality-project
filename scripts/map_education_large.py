import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.patheffects as path_effects

# === Paths ===
shapefile_path = "outputs/dallas_zcta_filtered.shp"
census_path = "data/dallas_zip_demographics.csv"
output_path = "outputs/maps_by_year/education_map_large.png"

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

# === Plot ===
print("Generating plot...")
fig, ax = plt.subplots(1, 1, figsize=(36, 30))  # Much larger size for user zoom
merged.plot(
    column="percent_bachelor_or_higher",
    cmap="Purples",
    linewidth=0.8,
    edgecolor="0.8",
    legend=True,
    ax=ax,
    legend_kwds={
        "label": "% with Bachelor’s Degree or Higher",
        "shrink": 0.5
    }
)

# Add ZIP labels with white outline for contrast
for _, row in merged.iterrows():
    if pd.notnull(row["label_point"]) and pd.notnull(row["GEOID20"]):
        x, y = row["label_point"].x, row["label_point"].y
        txt = ax.text(x, y, row["GEOID20"], fontsize=9, ha='center', va='center', color='black')
        txt.set_path_effects([path_effects.Stroke(linewidth=2, foreground='white'),
                              path_effects.Normal()])

ax.set_title("Dallas ZIP Code Education Map\n% with Bachelor's Degree or Higher", fontsize=26)
ax.axis("off")

# === Save output ===
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.close()
print(f"✅ Saved: {output_path}")
