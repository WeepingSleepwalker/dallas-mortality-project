import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os

# === Load shapefile and death estimates ===
zcta_gdf = gpd.read_file("outputs/dallas_zcta_filtered.shp")
zcta_gdf["GEOID20"] = zcta_gdf["GEOID20"].astype(str).str.zfill(5)
zcta_gdf["centroid"] = zcta_gdf.geometry.centroid

death_df = pd.read_csv("data/zip_yearly_death_estimates.csv")
death_df["zip"] = death_df["zip"].apply(lambda x: str(int(float(x))).zfill(5))

# === Create output directory ===
os.makedirs("outputs/maps_by_year", exist_ok=True)

# === Loop over years ===
for year in range(2018, 2023):
    print(f"Processing year: {year}")
    year_df = death_df[death_df["year"] == year].copy()

    # Merge with shapefile
    merged = zcta_gdf.merge(year_df, left_on="GEOID20", right_on="zip", how="left")

    if merged["estimated_deaths"].isnull().all():
        print(f"⚠️  No matching ZIPs found for {year}")
        continue

    # Plot
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    merged.plot(
        column="estimated_deaths",
        cmap="OrRd",
        linewidth=0.8,
        ax=ax,
        edgecolor="0.8",
        legend=True,
        legend_kwds={"label": f"Estimated Deaths in {year}", "shrink": 0.7}
    )

    # Add ZIP code labels at centroid — only if they have death data
    for _, row in merged.dropna(subset=["estimated_deaths"]).iterrows():
        if row["geometry"].is_valid and row["centroid"] and row["GEOID20"]:
            x, y = row["centroid"].x, row["centroid"].y
            ax.text(x, y, row["GEOID20"], fontsize=6, ha='center', va='center', color='black')


    ax.set_title(f"Estimated Deaths by ZIP Code – Dallas County ({year})", fontsize=16)
    ax.axis("off")

    # Save
    filename = f"outputs/maps_by_year/zip_deaths_map_{year}.png"
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    print(f"✅ Saved: {filename}")
    plt.close()
