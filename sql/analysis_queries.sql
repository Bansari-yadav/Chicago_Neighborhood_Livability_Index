USE chicago_livability;

-- Top 10 highest livability areas
SELECT community_area_number, final_livability_score
FROM final_livability_scores
ORDER BY final_livability_score DESC
LIMIT 10;

-- Top 10 highest crime areas
SELECT community_area_number, total_crimes
FROM final_livability_scores
ORDER BY total_crimes DESC
LIMIT 10;

-- Top 10 lowest crime areas
SELECT community_area_number, total_crimes
FROM final_livability_scores
ORDER BY total_crimes ASC
LIMIT 10;

-- Areas with high housing score but lower safety score
SELECT community_area_number, housing_score, safety_score, final_livability_score
FROM final_livability_scores
WHERE housing_score >= 70 AND safety_score < 50
ORDER BY housing_score DESC;

-- Areas with balanced livability
SELECT community_area_number, safety_score, housing_score, grocery_score, final_livability_score
FROM final_livability_scores
WHERE safety_score >= 60
  AND housing_score >= 40
  AND grocery_score >= 40
ORDER BY final_livability_score DESC;