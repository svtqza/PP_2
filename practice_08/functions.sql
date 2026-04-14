-- functions.sql

-- 1. Function: search records by pattern
CREATE OR REPLACE FUNCTION search_contacts(pattern_text TEXT)
RETURNS TABLE (
    id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.last_name, c.phone
    FROM contacts c
    WHERE c.first_name ILIKE '%' || pattern_text || '%'
       OR c.last_name ILIKE '%' || pattern_text || '%'
       OR c.phone ILIKE '%' || pattern_text || '%';
END;
$$ LANGUAGE plpgsql;


-- 2. Function: query with pagination
CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, offs INT)
RETURNS TABLE (
    id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.last_name, c.phone
    FROM contacts c
    ORDER BY c.id
    LIMIT lim OFFSET offs;
END;
$$ LANGUAGE plpgsql;