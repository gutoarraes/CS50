SELECT AVG (rating)
FROM ratings
WHERE (SELECT year FROM movies WHERE year >= 2012);
