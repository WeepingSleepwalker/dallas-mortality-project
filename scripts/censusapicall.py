import requests
import pandas as pd

API_KEY = "94ba843de1bba8a8b85c58671d3adabe5810b6d0"  # Replace with your key

# Add all variables of interest
variables = {
    # Population
    "B01003_001E": "total_population",
    # Income
    "B19013_001E": "median_income",
    # Age 65+
    "B01001_020E": "male_65_66",
    "B01001_021E": "male_67_69",
    "B01001_022E": "male_70_74",
    "B01001_023E": "male_75_79",
    "B01001_024E": "male_80_84",
    "B01001_025E": "male_85_plus",
    "B01001_044E": "female_65_66",
    "B01001_045E": "female_67_69",
    "B01001_046E": "female_70_74",
    "B01001_047E": "female_75_79",
    "B01001_048E": "female_80_84",
    "B01001_049E": "female_85_plus",
    # Education
    "B15003_001E": "education_total",
    "B15003_016E": "less_than_9th",
    "B15003_017E": "no_diploma",
    "B15003_022E": "bachelor",
    "B15003_023E": "masters",
    "B15003_024E": "professional",
    "B15003_025E": "doctorate",
    # Race/Ethnicity
    "B03002_001E": "race_total",
    "B03002_003E": "white_non_hispanic",
    "B03002_004E": "black",
    "B03002_012E": "hispanic"
}

# Fetch data
base_url = "https://api.census.gov/data/2022/acs/acs5"
params = {
    "get": ",".join(variables.keys()),
    "for": "zip code tabulation area:*",
    "key": API_KEY
}
response = requests.get(base_url, params=params)
data = response.json()

# Build DataFrame
df = pd.DataFrame(data[1:], columns=data[0])
df = df.rename(columns=variables)

# Filter to Dallas ZIPs
df = df[df["zip code tabulation area"].str.startswith(("750", "751", "752", "753"))].copy()
df = df.rename(columns={"zip code tabulation area": "zip"})

# Convert numerics
for col in list(variables.values()):
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Calculate age 65+
age_cols = [
    "male_65_66", "male_67_69", "male_70_74", "male_75_79", "male_80_84", "male_85_plus",
    "female_65_66", "female_67_69", "female_70_74", "female_75_79", "female_80_84", "female_85_plus"
]
df["age_65_plus"] = df[age_cols].sum(axis=1)
df["percent_65_plus"] = df["age_65_plus"] / df["total_population"] * 100

# Education breakdown
df["percent_no_hs"] = (df["less_than_9th"] + df["no_diploma"]) / df["education_total"] * 100
df["percent_bachelor_or_higher"] = (
    df["bachelor"] + df["masters"] + df["professional"] + df["doctorate"]
) / df["education_total"] * 100

# Race breakdown
df["percent_white_non_hispanic"] = df["white_non_hispanic"] / df["race_total"] * 100
df["percent_black"] = df["black"] / df["race_total"] * 100
df["percent_hispanic"] = df["hispanic"] / df["race_total"] * 100

# Final DataFrame
final = df[[
    "zip", "total_population", "median_income", "percent_65_plus",
    "percent_no_hs", "percent_bachelor_or_higher",
    "percent_white_non_hispanic", "percent_black", "percent_hispanic"
]]



final.to_csv("dallas_zip_demographics.csv", index=False)
