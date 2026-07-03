USE chicago_livability;

CREATE OR REPLACE VIEW top_livability_areas AS
SELECT community_area_number, final_livability_score, safety_score, housing_score, grocery_score
FROM final_livability_scores
ORDER BY final_livability_score DESC;

CREATE OR REPLACE VIEW high_crime_areas AS
SELECT community_area_number, total_crimes, violent_crimes, property_crimes
FROM final_livability_scores
ORDER BY total_crimes DESC;