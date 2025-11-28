SELECT 
    id AS event_id,
    user_id,
    session_id,
    sequence_number,
    event_type,
    uri AS page_url,
    traffic_source,
    ip_address,
    city,
    state,
    created_at AS event_at,
    DATE(created_at) AS event_date
FROM {{ source('look', 'events') }}
