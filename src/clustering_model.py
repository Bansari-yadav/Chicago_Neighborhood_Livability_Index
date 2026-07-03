import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

CLEANED_DATA = Path("data/cleaned")

input_file = CLEANED_DATA / "final_livability_dataset.csv"
output_file = CLEANED_DATA / "final_livability_with_clusters.csv"

df = pd.read_csv(input_file)

features = [
    "total_crimes",
    "violent_crimes",
    "property_crimes",
    "housing_score",
    "grocery_score",
    "final_livability_score",
]

model_data = df[features].fillna(0)

scaler = StandardScaler()
scaled_data = scaler.fit_transform(model_data)

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(scaled_data)

cluster_summary = (
    df.groupby("cluster")[features]
    .mean()
    .round(2)
    .reset_index()
)

print("Cluster Summary:")
print(cluster_summary)

df.to_csv(output_file, index=False)

print("Saved:", output_file)
print(df[["community_area_number", "cluster", "final_livability_score"]].head())