SELECT
    order_id,
    user_id,
    status,
    created_at,
    num_of_item,
    DATE(created_at) as order_date
FROM {{ source('look', 'orders') }}

WHERE 
    -- 1. 기본 필터링 (취소/반품 제외)
    status NOT IN ('Cancelled', 'Returned')
    AND DATE(created_at) BETWEEN '2023-01-01' AND '2024-12-31'