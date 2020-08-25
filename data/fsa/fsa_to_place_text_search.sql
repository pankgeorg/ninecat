-- Use this to add new places for geocoding

INSERT INTO places.place_text_search (
    text_input,
    source_entity_id
)
SELECT
    name || ', ' || address || ', ' || area as text_input,
    fsa_id as source_entity_id
FROM fsa.pharmacy
WHERE fsa_id NOT IN (
    SELECT DISTINCT source_entity_id id
    FROM places.place_text_search
    WHERE source_entity_id IS NOT NULL
);