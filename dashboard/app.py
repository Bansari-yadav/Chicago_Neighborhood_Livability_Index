import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Chicago Livability Dashboard",
    page_icon="🏙️",
    layout="wide"
)

DATA_PATH = Path("data/cleaned/final_livability_with_clusters.csv")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

st.title("Chicago Neighborhood Livability Dashboard")
st.write("Safety, housing, grocery access, and ML cluster analysis by Chicago community area.")

# Sidebar filters
st.sidebar.header("Filters")

min_score = st.sidebar.slider(
    "Minimum Livability Score",
    min_value=float(df["final_livability_score"].min()),
    max_value=float(df["final_livability_score"].max()),
    value=float(df["final_livability_score"].min())
)

selected_clusters = st.sidebar.multiselect(
    "Select Clusters",
    options=sorted(df["cluster"].unique()),
    default=sorted(df["cluster"].unique())
)

filtered = df[
    (df["final_livability_score"] >= min_score)
    & (df["cluster"].isin(selected_clusters))
]

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Community Areas", len(filtered))
col2.metric("Avg Livability Score", round(filtered["final_livability_score"].mean(), 2))
col3.metric("Avg Safety Score", round(filtered["safety_score"].mean(), 2))
col4.metric("Avg Grocery Score", round(filtered["grocery_score"].mean(), 2))

st.divider()

# Top and bottom rankings
left, right = st.columns(2)

with left:
    st.subheader("Top 10 Livability Areas")
    top10 = filtered.sort_values("final_livability_score", ascending=False).head(10)
    st.dataframe(
        top10[
            [
                "community_area_number",
                "total_crimes",
                "violent_crimes",
                "housing_score",
                "grocery_score",
                "final_livability_score",
                "cluster",
            ]
        ],
        use_container_width=True
    )

with right:
    st.subheader("Bottom 10 Livability Areas")
    bottom10 = filtered.sort_values("final_livability_score", ascending=True).head(10)
    st.dataframe(
        bottom10[
            [
                "community_area_number",
                "total_crimes",
                "violent_crimes",
                "housing_score",
                "grocery_score",
                "final_livability_score",
                "cluster",
            ]
        ],
        use_container_width=True
    )

st.divider()

# Charts
st.subheader("Livability Score by Community Area")

fig_score = px.bar(
    filtered.sort_values("final_livability_score", ascending=False),
    x="community_area_number",
    y="final_livability_score",
    color="cluster",
    title="Final Livability Score by Community Area",
    labels={
        "community_area_number": "Community Area",
        "final_livability_score": "Livability Score",
        "cluster": "ML Cluster"
    }
)

st.plotly_chart(fig_score, use_container_width=True)

st.subheader("Crime vs Livability")

fig_crime = px.scatter(
    filtered,
    x="total_crimes",
    y="final_livability_score",
    color="cluster",
    size="violent_crimes",
    hover_data=["community_area_number", "housing_score", "grocery_score"],
    title="Total Crime vs Final Livability Score",
    labels={
        "total_crimes": "Total Crimes",
        "final_livability_score": "Livability Score",
        "violent_crimes": "Violent Crimes"
    }
)

st.plotly_chart(fig_crime, use_container_width=True)

st.subheader("Housing Score vs Grocery Score")

fig_access = px.scatter(
    filtered,
    x="housing_score",
    y="grocery_score",
    color="cluster",
    size="final_livability_score",
    hover_data=["community_area_number", "total_crimes", "violent_crimes"],
    title="Housing Access vs Grocery Access",
    labels={
        "housing_score": "Housing Score",
        "grocery_score": "Grocery Score"
    }
)

st.plotly_chart(fig_access, use_container_width=True)

st.subheader("Cluster Summary")

cluster_summary = (
    filtered.groupby("cluster")
    .agg(
        community_areas=("community_area_number", "count"),
        avg_total_crimes=("total_crimes", "mean"),
        avg_violent_crimes=("violent_crimes", "mean"),
        avg_housing_score=("housing_score", "mean"),
        avg_grocery_score=("grocery_score", "mean"),
        avg_livability_score=("final_livability_score", "mean"),
    )
    .round(2)
    .reset_index()
)

st.dataframe(cluster_summary, use_container_width=True)

st.divider()

st.subheader("Full Dataset")
st.dataframe(filtered, use_container_width=True)