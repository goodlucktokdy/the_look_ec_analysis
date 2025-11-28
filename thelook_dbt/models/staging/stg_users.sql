SELECT 
    id AS user_id,
    first_name,
    last_name,
    email,
    age,
    gender,
    state,
    country,
    traffic_source,
    created_at AS signup_at,
    DATE(created_at) AS signup_date
FROM {{ source('look', 'users') }}