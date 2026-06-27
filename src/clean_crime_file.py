import pandas as pd
from pathlib import Path

RAW_DATA = Path("data/raw")
CLEANED_DATA = Path("data/cleaned")
CLEANED_DATA.mkdir(parents=True, exist_ok=True)

crime_file = RAW_DATA / "Crimes_-_One_year_prior_to_present_20260624.csv"
output_file = CLEANED_DATA / "cleaned_crime_2025_2026.csv"

columns_to_use = [
    "Date",
    "Primary Type",
    "Description",
    "Location Description",
    "Arrest",
    "Domestic",
    "Community Area",
    "Year",
    "Latitude",
    "Longitude",
]

chunks = []

for chunk in pd.read_csv(crime_file, usecols=columns_to_use, chunksize=100000):
    chunk = chunk.dropna(subset=["Community Area"])

    chunk["Community Area"] = chunk["Community Area"].astype(int)

    chunk = chunk[chunk["Community Area"] != 0]

    chunk["Date"] = pd.to_datetime(chunk["Date"], errors="coerce")
    chunk = chunk.dropna(subset=["Date"])

    chunks.append(chunk)

cleaned = pd.concat(chunks, ignore_index=True)

cleaned.to_csv(output_file, index=False)

print("Cleaned crime data saved to:", output_file)
print("Rows:", len(cleaned))
print("Columns:", cleaned.columns.tolist())
print(cleaned.head())