import pandas as pd
from pathlib import Path

RAW_DATA = Path("data/raw")
CLEANED_DATA = Path("data/cleaned")
CLEANED_DATA.mkdir(parents=True, exist_ok=True)

input_file = RAW_DATA / "Crimes_-_2015_20260626.csv"
cleaned_output = CLEANED_DATA / "cleaned_crime_community_area.csv"
summary_output = CLEANED_DATA / "crime_by_community_area.csv"

columns_to_use = [
    "ID",
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

violent_types = {
    "HOMICIDE",
    "ASSAULT",
    "BATTERY",
    "ROBBERY",
    "CRIMINAL SEXUAL ASSAULT",
}

property_types = {
    "THEFT",
    "BURGLARY",
    "MOTOR VEHICLE THEFT",
    "CRIMINAL DAMAGE",
    "ARSON",
}

chunks = []

for chunk in pd.read_csv(input_file, usecols=columns_to_use, chunksize=100000, low_memory=False):
    chunk = chunk.rename(columns={
        "ID": "crime_id",
        "Date": "date",
        "Primary Type": "primary_type",
        "Description": "description",
        "Location Description": "location_description",
        "Arrest": "arrest",
        "Domestic": "domestic",
        "Community Area": "community_area",
        "Year": "year",
        "Latitude": "latitude",
        "Longitude": "longitude",
    })

    chunk["date"] = pd.to_datetime(chunk["date"], errors="coerce")
    chunk["community_area"] = pd.to_numeric(chunk["community_area"], errors="coerce")

    chunk = chunk.dropna(subset=["date", "community_area"])
    chunk = chunk[chunk["community_area"] != 0]

    chunk["community_area"] = chunk["community_area"].astype(int)
    chunk["year"] = pd.to_numeric(chunk["year"], errors="coerce")
    chunk["month"] = chunk["date"].dt.month

    chunk["primary_type"] = chunk["primary_type"].astype(str).str.upper()

    chunk["violent_crime"] = chunk["primary_type"].isin(violent_types).astype(int)
    chunk["property_crime"] = chunk["primary_type"].isin(property_types).astype(int)
    chunk["arrest_count"] = chunk["arrest"].astype(str).str.lower().eq("true").astype(int)
    chunk["domestic_crime"] = chunk["domestic"].astype(str).str.lower().eq("true").astype(int)

    chunks.append(chunk)

crime = pd.concat(chunks, ignore_index=True)
crime = crime.drop_duplicates(subset=["crime_id"])

crime.to_csv(cleaned_output, index=False)

summary = (
    crime.groupby("community_area")
    .agg(
        total_crimes=("crime_id", "count"),
        violent_crimes=("violent_crime", "sum"),
        property_crimes=("property_crime", "sum"),
        arrest_count=("arrest_count", "sum"),
        domestic_crimes=("domestic_crime", "sum"),
        first_year=("year", "min"),
        last_year=("year", "max"),
    )
    .reset_index()
)

summary["arrest_rate"] = summary["arrest_count"] / summary["total_crimes"]

summary.to_csv(summary_output, index=False)

print("Saved:", cleaned_output)
print("Saved:", summary_output)
print("Rows cleaned:", len(crime))
print(summary.head())
