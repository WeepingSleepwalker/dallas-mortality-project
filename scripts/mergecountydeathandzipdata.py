import pandas as pd

# === Define known ZIPs in Dallas County ===
dallas_zips = [
    75006, 75019, 75038, 75039, 75041, 75042, 75043, 75044, 75048, 75050,
    75051, 75052, 75060, 75061, 75062, 75080, 75081, 75082, 75104, 75115,
    75116, 75134, 75137, 75138, 75141, 75146, 75149, 75150, 75159, 75172,
    75180, 75181, 75182, 75185, 75187,
    *range(75201, 75255)  # Covers ZIPs 75201 to 75254
]

# === Load your inputs ===
zip_df = pd.read_csv("data/dallas_zip_demographics.csv")
county_df = pd.read_csv("data/dallas_county_deaths_2011_2022.csv")

# === Filter to only Dallas County ZIPs ===
zip_df = zip_df[zip_df["zip"].isin(dallas_zips)].copy()

# === Compute total ZIP population ===
total_zip_pop = zip_df["total_population"].sum()

# === Generate ZIP-year-level records with estimated deaths and death rates ===
rows = []

for _, zip_row in zip_df.iterrows():
    zip_code = zip_row["zip"]
    zip_pop = zip_row["total_population"]
    zip_share = zip_pop / total_zip_pop

    for _, county_row in county_df.iterrows():
        year = county_row["Year"]
        county_deaths = county_row["Deaths"]
        estimated_deaths = round(zip_share * county_deaths)
        death_rate_per_1000 = (estimated_deaths / zip_pop) * 1000

        rows.append({
            "zip": zip_code,
            "year": year,
            "estimated_deaths": estimated_deaths,
            "death_rate_per_1000": round(death_rate_per_1000, 2),
            "median_income": zip_row["median_income"],
            "percent_65_plus": zip_row["percent_65_plus"],
            "percent_no_hs": zip_row["percent_no_hs"],
            "percent_bachelor_or_higher": zip_row["percent_bachelor_or_higher"],
            "percent_white_non_hispanic": zip_row["percent_white_non_hispanic"],
            "percent_black": zip_row["percent_black"],
            "percent_hispanic": zip_row["percent_hispanic"]
        })

# === Convert to DataFrame ===
df_zip_deaths = pd.DataFrame(rows)

# === Save to file ===
df_zip_deaths.to_csv("data/zip_yearly_death_estimates.csv", index=False)
print("Saved to data/zip_yearly_death_estimates.csv")
