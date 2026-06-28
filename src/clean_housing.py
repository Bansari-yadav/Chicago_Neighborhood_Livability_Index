import pandas as pd
from pathlib import Path

RAW_DATA = Path("data/raw")
CLEANED_DATA = Path("data/cleaned")
CLEANED_DATA.mkdir(parents=True, exist_ok=True)

housing_file = RAW_DATA / "Affordable_Rental_Housing_Developments.csv"
output_file = CLEANED_DATA / "housing_by_community_area.csv"

housing = pd.read_csv(housing_file)

housing = housing.rename(
    columns={
        "Community Area Name": "community_area_name",
        "Community Area Number": "community_area",
        "Property Type": "property_type",
        "Property Name": "property_name",
        "Address": "address",
        "Zip Code": "zip_code",
        "Units": "units",
        "Latitude": "latitude",
        "Longitude": "longitude",
    }
)

housing["community_area"] = pd.to_numeric(housing["community_area"], errors="coerce")
housing["units"] = pd.to_numeric(housing["units"], errors="coerce").fillna(0)

housing = housing.dropna(subset=["community_area"])
housing["community_area"] = housing["community_area"].astype(int)

summary = (
    housing.groupby(["community_area", "community_area_name"])
    .agg(
        affordable_property_count=("property_name", "count"),
        affordable_unit_count=("units", "sum"),
        avg_units_per_property=("units", "mean"),
    )
    .reset_index()
)

summary.to_csv(output_file, index=False)

print("Housing summary saved to:", output_file)
print("Rows:", len(summary))
print(summary.head())