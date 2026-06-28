import pandas as pd
from pathlib import Path

RAW_DATA = Path("data/raw")
CLEANED_DATA = Path("data/cleaned")
CLEANED_DATA.mkdir(parents=True, exist_ok=True)

grocery_file = RAW_DATA / "Grocery_Stores_-_2013_20260625.csv"
output_file = CLEANED_DATA / "grocery_by_community_area.csv"

columns_to_use = [
    "STORE NAME",
    "SQUARE FEET",
    "ADDRESS",
    "ZIP CODE",
    "COMMUNITY AREA NAME",
    "COMMUNITY AREA",
    "WARD",
    "LATITUDE",
    "LONGITUDE",
]

grocery = pd.read_csv(grocery_file, usecols=columns_to_use)

grocery = grocery.rename(
    columns={
        "STORE NAME": "store_name",
        "SQUARE FEET": "square_feet",
        "ADDRESS": "address",
        "ZIP CODE": "zip_code",
        "COMMUNITY AREA NAME": "community_area_name",
        "COMMUNITY AREA": "community_area",
        "WARD": "ward",
        "LATITUDE": "latitude",
        "LONGITUDE": "longitude",
    }
)

grocery["community_area"] = pd.to_numeric(grocery["community_area"], errors="coerce")
grocery["square_feet"] = pd.to_numeric(grocery["square_feet"], errors="coerce").fillna(0)

grocery = grocery.dropna(subset=["community_area"])
grocery["community_area"]