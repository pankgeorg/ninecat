-- Use this to add new places for geocoding

INSERT INTO places.place_text_search (
    text_input,
    source_entity_id,
    priority,
    locationbias,
   	input_type
)
SELECT
    name || ', ' || address || ', ' || area as text_input,
    fsa_id as source_entity_id,
    0 as priority,
    'circle:1000000@37.8945342,23.7307223' as locationbias,
    'textquery' as input_type
FROM fsa.pharmacy
WHERE fsa_id NOT IN (
    SELECT DISTINCT source_entity_id id
    FROM places.place_text_search
    WHERE source_entity_id IS NOT NULL
);