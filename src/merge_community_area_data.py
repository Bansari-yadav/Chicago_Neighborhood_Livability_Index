import pandas as pd
from pathlib import Path

CLEANED_DATA = Path("data/cleaned")
OUTPUT_FILE = CLEANED_DATA / "final_livability_dataset.csv"

crime_file = CLEANED_DATA / "crime_by_community_area.csv"
housing_file = CLEANED_DATA / "housing_by_community_area.csv"
grocery_file = CLEANED_DATA / "grocery_by_community_area.csv"

crime = pd.read_csv(crime_file)
housing = pd.read_csv(housing_file)
grocery = pd.read_csv(grocery_file)

print("Crime columns:", crime.columns.tolist())
print("Housing columns:", housing.columns.tolist())
print("Grocery columns:", grocery.columns.tolist())

# Standardize merge key names
crime = crime.rename(columns={
    "community_area": "community_area_number"
})

# These two lines are flexible in case your files use slightly different names
housing = housing.rename(columns={
    "Community Area Number": "community_area_number",
    "community_area": "community_area_number",
    "community_area_name": "community_area_name",
    "Community Area Name": "community_area_name",
})

grocery = grocery.rename(columns={
    "community_area": "community_area_number",
    "Community Area": "community_area_number",
    "community_area_name": "community_area_name",
    "Community Area Name": "community_area_name",
})

# Make sure keys are numeric
crime["community_area_number"] = pd.to_numeric(crime["community_area_number"], errors="coerce")
housing["community_area_number"] = pd.to_numeric(housing["community_area_number"], errors="coerce")
grocery["community_area_number"] = pd.to_numeric(grocery["community_area_number"], errors="coerce")

crime = crime.dropna(subset=["community_area_number"])
housing = housing.dropna(subset=["community_area_number"])
grocery = grocery.dropna(subset=["community_area_number"])

crime["community_area_number"] = crime["community_area_number"].astype(int)
housing["community_area_number"] = housing["community_area_number"].astype(int)
grocery["community_area_number"] = grocery["community_area_number"].astype(int)

# Merge crime + housing + grocery
final = crime.merge(
    housing,
    on="community_area_number",
    how="left"
)

final = final.merge(
    grocery,
    on="community_area_number",
    how="left",
    suffixes=("_housing", "_grocery")
)

# Fill missing numeric values
numeric_columns = final.select_dtypes(include="number").columns
final[numeric_columns] = final[numeric_columns].fillna(0)

# Create simple scores
def min_max_score(series, higher_is_better=True):
    if series.max() == series.min():
        return pd.Series([100] * len(series), index=series.index)

    score = (series - series.min()) / (series.max() - series.min()) * 100

    if not higher_is_better:
        score = 100 - score

    return score

final["safety_score"] = min_max_score(final["total_crimes"], higher_is_better=False)
final["violent_safety_score"] = min_max_score(final["violent_crimes"], higher_is_better=False)

if "affordable_unit_count" in final.columns:
    final["housing_score"] = min_max_score(final["affordable_unit_count"], higher_is_better=True)
elif "affordable_units" in final.columns:
    final["housing_score"] = min_max_score(final["affordable_units"], higher_is_better=True)
else:
    final["housing_score"] = 0

if "grocery_store_count" in final.columns:
    final["grocery_score"] = min_max_score(final["grocery_store_count"], higher_is_better=True)
elif "store_count" in final.columns:
    final["grocery_score"] = min_max_score(final["store_count"], higher_is_better=True)
else:
    final["grocery_score"] = 0

final["final_livability_score"] = (
    final["safety_score"] * 0.45
    + final["violent_safety_score"] * 0.25
    + final["housing_score"] * 0.20
    + final["grocery_score"] * 0.10
)

final = final.sort_values("final_livability_score", ascending=False)

final.to_csv(OUTPUT_FILE, index=False)

print("Saved:", OUTPUT_FILE)
print("Rows:", len(final))
print(final.head(10))