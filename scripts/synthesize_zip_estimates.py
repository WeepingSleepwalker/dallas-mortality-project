import pandas as pd

# Load county-wide deaths and ZIP-level census weights
mortality_df = pd.read_csv("data/dallas_county_deaths_2011_2022.csv")
census_df = pd.read_csv("data/zip_yearly_death_estimates.csv")

# Clean types
mortality_df["Year"] = mortality_df["Year"].astype(int)
census_df["zip"] = census_df["zip"].astype(str)

# Filter years 2018–2022
recent = mortality_df[mortality_df["Year"] >= 2018]
yearly_totals = recent.groupby("Year")["Deaths"].sum().reset_index()

# Calculate weight per ZIP
census_df["weight"] = (census_df["percent_65_plus"] / 100) * census_df["estimated_deaths"]
census_df["weight_fraction"] = census_df["weight"] / census_df["weight"].sum()

# Generate synthetic ZIP-level death estimates for each year
zip_yearly_rows = []
for _, row in yearly_totals.iterrows():
    year = row["Year"]
    total = row["Deaths"]
    temp = census_df.copy()
    temp["year"] = year
    temp["estimated_deaths"] = temp["weight_fraction"] * total
    zip_yearly_rows.append(temp[["zip", "year", "estimated_deaths"]])

# Combine into one DataFrame and save
zip_deaths_df = pd.concat(zip_yearly_rows, ignore_index=True)
zip_deaths_df.to_csv("outputs/zip_death_estimates.csv", index=False)
print("✅ Saved to outputs/zip_death_estimates.csv")
