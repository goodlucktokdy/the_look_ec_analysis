SELECT 
    id AS order_item_id,
    inventory_item_id,
    order_id,
    user_id,
    product_id,
    status,
    sale_price,
    created_at,
    DATE(created_at) AS order_date,
    DATE(shipped_at) AS shipped_date,
    DATE(delivered_at) AS delivered_date,
    DATE(returned_at) AS returned_date
FROM {{ source('look', 'order_items') }}
WHERE status NOT IN ('Cancelled', 'Returned')
    AND DATE(created_at) BETWEEN '2023-01-01' AND '2024-12-31'