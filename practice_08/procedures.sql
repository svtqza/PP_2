-- procedures.sql

-- 1. Procedure: insert new user or update phone if user already exists
CREATE OR REPLACE PROCEDURE insert_or_update_user(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_phone VARCHAR
)
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM contacts
        WHERE first_name = p_first_name
          AND last_name = p_last_name
    ) THEN
        UPDATE contacts
        SET phone = p_phone
        WHERE first_name = p_first_name
          AND last_name = p_last_name;
    ELSE
        INSERT INTO contacts(first_name, last_name, phone)
        VALUES (p_first_name, p_last_name, p_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;


-- 2. Procedure: delete by username or phone
CREATE OR REPLACE PROCEDURE delete_user(p_value VARCHAR)
AS $$
BEGIN
    DELETE FROM contacts
    WHERE first_name = p_value
       OR phone = p_value;
END;
$$ LANGUAGE plpgsql;