WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

order_items AS (
    SELECT * FROM {{ ref('stg_order_items') }}
),

-- 1. 유저별 RFM 기초 집계
rfm_base AS (
    SELECT
        o.user_id,
        -- 기준일은 분석 시점에 따라 달라질 수 있으므로 현재는 고정값 사용 (또는 변수화 가능)
        DATE_DIFF(DATE('2025-01-01'), MAX(o.order_date), DAY) AS recency_days,
        COUNT(DISTINCT o.order_id) AS frequency,
        ROUND(SUM(oi.sale_price), 2) AS monetary
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.user_id
),

-- 2. 점수 부여 (동윤님의 기준 적용)
rfm_scored AS (
    SELECT
        *,
        CASE
            WHEN recency_days <= 90 THEN 5
            WHEN recency_days <= 180 THEN 4
            WHEN recency_days <= 365 THEN 3
            WHEN recency_days <= 545 THEN 2
            ELSE 1
        END AS r_score,
        CASE
            WHEN frequency >= 3 THEN 5
            WHEN frequency = 2 THEN 4
            ELSE 1 -- frequency 1
        END AS f_score,
        CASE
            WHEN monetary >= 300 THEN 5
            WHEN monetary >= 135 THEN 4
            WHEN monetary >= 67 THEN 3
            WHEN monetary >= 34 THEN 2
            ELSE 1
        END AS m_score
    FROM rfm_base
)

-- 3. 최종 세그먼트 정의
SELECT
    *,
    CASE
        -- VIP Champions
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'VIP'
        -- Loyal High Value
        WHEN r_score >= 3 AND f_score >= 4 AND m_score >= 3 THEN 'Loyal High Value'
        -- Loyal Low Value
        WHEN r_score >= 3 AND f_score >= 4 AND m_score <= 2 THEN 'Loyal Low Value'
        -- Promising High Value
        WHEN r_score >= 4 AND f_score = 1 AND m_score >= 3 THEN 'Promising High Value'
        -- Promising Low Value
        WHEN r_score >= 4 AND f_score = 1 AND m_score <= 2 THEN 'Promising Low Value'
        -- Need Attention
        WHEN r_score <= 2 AND f_score >= 4 AND m_score >= 3 THEN 'Need Attention'
        -- At Risk
        WHEN r_score = 3 AND f_score = 1 THEN 'At Risk'
        -- Hibernating
        WHEN r_score <= 2 AND f_score <= 2 THEN 'Hibernating'
        ELSE 'Others'
    END AS customer_segment
FROM rfm_scored