This project models synthetic mortality risk across Dallas-area ZIP codes using demographic predictors from the American Community Survey. Due to privacy constraints on granular death counts, ZIP-level risk is inferred from county-level mortality rates, adjusted for age, income, education, and race. The resulting scores highlight spatial disparities and identify neighborhoods with elevated risk exposure. Data is visualized via a choropleth map using GeoPandas, enabling clear geographic insight into public health vulnerability. This analysis can support resource allocation, outreach prioritization, or further modeling by city or nonprofit stakeholders.

# Dallas Mortality Mapping

This project analyzes spatial patterns in mortality across Dallas ZIP codes using demographic and death rate data. The output is an interactive choropleth map that visualizes estimated deaths per 1,000 residents over time.

## 📂 Project Structure

- `data/`: Raw demographic and mortality CSV data
- `outputs/`: Processed shapefiles and final maps
- `notebooks/` or `main.py`: Data processing and map rendering logic
- `requirements.txt`: Python dependencies

## 📊 Output: Mortality Map

The main output is a choropleth map showing death rates per ZIP code in Dallas County.

### ✅ To Check the Map Output

1. Make sure all dependencies are installed:
   ```bash
   pip install -r requirements.txt


# Dallas County ZIP-Level Mortality Estimates (2018–2022)

This dataset and codebase estimates yearly death counts and death rates at the ZIP code level for Dallas County, Texas, based on population-adjusted scaling of official county-wide death totals.

## 📊 Datasets Used

1. **Dallas County Yearly Death Totals (2011–2022)**
   - Source: Texas Health and Human Services
   - Contains annual total deaths in Dallas County
   - Used as the baseline for estimating deaths per ZIP code

2. **ZIP-Level Demographics (2022)**
   - Source: U.S. Census Bureau – ACS 5-Year Estimates via Census API
   - Variables: total population, median income, education, age 65+, race/ethnicity
   - Data reflects a rolling average from **2018–2022**
   - Limited to ZIP codes that fall within Dallas County

## ⚠️ Data Disclaimer

Demographic variables in this dataset are based on the **2022 ACS 5-Year Estimates**, which represent average conditions from **2018 to 2022**. Therefore:

- **Demographics are static** across all modeled years (2011–2022)
- They are not intended to represent specific year-to-year changes

## 📁 Output File

- `zip_yearly_death_estimates.csv`: Contains estimated yearly deaths, death rate per 1,000 residents, and demographics per ZIP code

## 🔧 Methodology

- Deaths were allocated to ZIP codes proportionally based on their share of the total Dallas County population
- Each ZIP/year entry includes death estimates and static demographic characteristics

