import pandas as pd
from pathlib import Path

RAW_DATA = Path("data/raw")
CLEANED_DATA = Path("data/cleaned")
CLEANED_DATA.mkdir(parents=True, exist_ok=True)

crime_file = RAW_DATA / "Crimes_-_One_year_prior_to_present_20260624.csv"
# output_file = CLEANED_DATA / "cleaned_crime_2025_2026.csv" changes after discrepencies found in the dates
output_file = CLEANED_DATA / "cleaned_crime_2015_2026_partial.csv"


columns_to_use = [
    "DATE  OF OCCURRENCE",
    " PRIMARY DESCRIPTION",
    " SECONDARY DESCRIPTION",
    " LOCATION DESCRIPTION",
    "ARREST",
    "DOMESTIC",
    "WARD",
    "LATITUDE",
    "LONGITUDE",
]

chunks = []

for chunk in pd.read_csv(crime_file, usecols=columns_to_use, chunksize=100000):
    chunk = chunk.rename(
        columns={
            "DATE  OF OCCURRENCE": "date",
            " PRIMARY DESCRIPTION": "primary_type",
            " SECONDARY DESCRIPTION": "description",
            " LOCATION DESCRIPTION": "location_description",
            "ARREST": "arrest",
            "DOMESTIC": "domestic",
            "WARD": "ward",
            "LATITUDE": "latitude",
            "LONGITUDE": "longitude",
        }
    )

    chunk["date"] = pd.to_datetime(chunk["date"], errors="coerce")
    chunk = chunk.dropna(subset=["date"])

    chunk["year"] = chunk["date"].dt.year
    chunk = chunk[(chunk["year"] >= 2015) & (chunk["year"] <= 2026)]
    chunk["month"] = chunk["date"].dt.month

    chunk["ward"] = pd.to_numeric(chunk["ward"], errors="coerce")
    chunk["latitude"] = pd.to_numeric(chunk["latitude"], errors="coerce")
    chunk["longitude"] = pd.to_numeric(chunk["longitude"], errors="coerce")

    chunk["primary_type"] = chunk["primary_type"].astype(str).str.strip()
    chunk["description"] = chunk["description"].astype(str).str.strip()
    chunk["location_description"] = chunk["location_description"].astype(str).str.strip()

    chunks.append(chunk)

cleaned = pd.concat(chunks, ignore_index=True)

cleaned.to_csv(output_file, index=False)

print("Cleaned crime data saved to:", output_file)
print("Rows:", len(cleaned))
print("Columns:", cleaned.columns.tolist())
print(cleaned.head())