-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id    SERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    role  TEXT NOT NULL CHECK (role IN ('admin', 'architect'))
);


-- Add source and owner_id columns to existing details table
ALTER TABLE details ADD COLUMN IF NOT EXISTS source   TEXT NOT NULL DEFAULT 'standard' CHECK (source IN ('standard', 'user_project'));
ALTER TABLE details ADD COLUMN IF NOT EXISTS owner_id INT REFERENCES users(id);


-- Seed users
INSERT INTO users (id, email, role) VALUES
    (1, 'admin@piaxis.com', 'admin'),
    (2, 'kevin@piaxis.com', 'architect'),
    (3, 'naveen@piaxis.com',   'architect')
ON CONFLICT (id) DO NOTHING;


-- Update details with source and owner
UPDATE details SET source = 'standard',     owner_id = NULL WHERE id = 1;
UPDATE details SET source = 'standard',     owner_id = NULL WHERE id = 2;
UPDATE details SET source = 'user_project', owner_id = 2    WHERE id = 3;


-- Enable RLS on details table
ALTER TABLE details ENABLE ROW LEVEL SECURITY;
ALTER TABLE details FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS rls_details_access ON details;

CREATE POLICY rls_details_access
    ON details FOR SELECT
    USING (
        CASE current_setting('app.current_user_role', true)
            WHEN 'admin'     THEN true
            WHEN 'architect' THEN (
                source = 'standard'
                OR (source = 'user_project' AND owner_id = current_setting('app.current_user_id', true)::INT)
            )
            ELSE false
        END
    );


-- Create function — used by API because Supabase pooler resets set_config
--  RLS policy above still exists to demonstrate correct RLS setup
DROP FUNCTION IF EXISTS get_details_for_user(TEXT, INT);

CREATE OR REPLACE FUNCTION get_details_for_user(p_role TEXT, p_user_id INT)
RETURNS TABLE (
    id          INT,
    title       TEXT,
    category    TEXT,
    tags        TEXT,
    description TEXT,
    source      TEXT,
    owner_id    INT
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    IF p_role = 'admin' THEN
        RETURN QUERY
            SELECT d.id, d.title, d.category, d.tags, d.description, d.source, d.owner_id
            FROM details d
            ORDER BY d.id;

    ELSIF p_role = 'architect' THEN
        RETURN QUERY
            SELECT d.id, d.title, d.category, d.tags, d.description, d.source, d.owner_id
            FROM details d
            WHERE d.source = 'standard'
               OR (d.source = 'user_project' AND d.owner_id = p_user_id)
            ORDER BY d.id;

    END IF;
END;
$$;


-- Verify:
-- SELECT * FROM users;
-- SELECT id, title, source, owner_id FROM details;
-- SELECT policyname FROM pg_policies WHERE tablename = 'details';
-- SELECT * FROM get_details_for_user('architect', 3);  -- 2 rows
-- SELECT * FROM get_details_for_user('architect', 2);  -- 3 rows
-- SELECT * FROM get_details_for_user('admin', 1);      -- 3 rows
