SELECT 
    id AS product_id,
    category,
    name AS product_name,
    brand,
    cost,
    retail_price,
    department
FROM {{ source('look', 'products') }}