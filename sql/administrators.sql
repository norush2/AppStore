CREATE OR REPLACE VIEW administrators AS (
    SELECT student_id FROM users WHERE is_admin
)