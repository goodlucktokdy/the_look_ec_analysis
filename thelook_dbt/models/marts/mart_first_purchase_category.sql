WITH rfm_segment AS (
    SELECT * FROM {{ ref('int_user_rfm') }}
),
products AS (
    SELECT * FROM {{ ref('stg_products') }}
),
order_items AS (
    SELECT * FROM {{ ref('stg_order_items') }}
),
first_purchase_info AS (
    SELECT 
        r.user_id,
        r.customer_segment,
        r.frequency,
        r.monetary,
        r.recency_days,
        o.product_id,
        o.sale_price,
        ROW_NUMBER() OVER(PARTITION BY r.user_id ORDER BY o.created_at ASC) AS rn
    FROM rfm_segment r
    INNER JOIN order_items o ON r.user_id = o.user_id
    WHERE LOWER(r.customer_segment) IN ('promising high value', 'promising low value', 'vip')
    QUALIFY rn = 1
),
first_pur_cat AS (
    SELECT 
        f.user_id,
        f.recency_days,
        f.monetary AS ltv,
        f.frequency,
        p.category,
        f.sale_price,
        f.customer_segment
    FROM first_purchase_info f
    INNER JOIN products p ON f.product_id = p.product_id
)
SELECT 
    customer_segment,
    category,
    COUNT(DISTINCT user_id) AS users,

    -- LTV 지표
    ROUND(AVG(ltv), 3) AS avg_ltv,
    ROUND(STDDEV(ltv), 3) AS std_ltv,
    ROUND(MIN(ltv), 3) AS min_ltv,
    ROUND(MAX(ltv), 3) AS max_ltv,
    ROUND(SUM(ltv), 3) AS sum_ltv,

    -- RFM 지표
    ROUND(AVG(frequency), 3) AS avg_frequency,
    ROUND(AVG(recency_days), 3) AS avg_recency,
    ROUND(AVG(sale_price), 3) AS first_item_price,

    ROUND(MAX(frequency), 3) AS max_frequency,
    ROUND(MAX(recency_days), 3) AS max_recency,
    ROUND(MAX(sale_price), 3) AS max_price
FROM first_pur_cat
GROUP BY customer_segment, category
ORDER BY avg_ltv DESC