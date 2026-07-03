CREATE DATABASE IF NOT EXISTS chicago_livability;
USE chicago_livability;

DROP TABLE IF EXISTS final_livability_scores;

CREATE TABLE final_livability_scores (
    community_area_number INT PRIMARY KEY,
    total_crimes INT,
    violent_crimes INT,
    property_crimes INT,
    arrest_count INT,
    domestic_crimes INT,
    first_year INT,
    last_year INT,
    arrest_rate DECIMAL(10,4),
    housing_score DECIMAL(10,4),
    grocery_score DECIMAL(10,4),
    safety_score DECIMAL(10,4),
    violent_safety_score DECIMAL(10,4),
    final_livability_score DECIMAL(10,4)
);