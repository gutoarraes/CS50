SELECT name from people
JOIN stars ON people.id = stars.person_id
JOIN movies ON movies.id = stars.movie_id
WHERE name != "Kevin Bacon"
AND
movie_id IN (
    SELECT movies.id FROM movies
    JOIN stars ON stars.movie_id = movies.id
    JOIN people ON people.id = stars.person_id
    WHERE name = "Kevin Bacon" AND birth = 1958);

