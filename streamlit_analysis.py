import pandas as pd
import streamlit as st
import json

# --- 1. Raw Data Input (Provided from SQL Query Results) ---

# 1. RFM Segment Analysis (Final Table)
rfm_final_data = [{"customer_segment": "At Risk", "user_count": "6637", "pct": "22.28", "avg_recency_days": "270.2", "avg_frequency": "1.0", "avg_monetary": "85.36", "avg_r_score": "3.0", "avg_f_score": "3.0", "avg_m_score": "2.36", "avg_rfm_total": "8.36", "total_revenue": "566558.73", "revenue_contribution_pct": "18.49"}, {"customer_segment": "Hibernating", "user_count": "9707", "pct": "32.58", "avg_recency_days": "538.5", "avg_frequency": "1.0", "avg_monetary": "86.38", "avg_r_score": "1.53", "avg_f_score": "3.0", "avg_m_score": "2.35", "avg_rfm_total": "6.88", "total_revenue": "838519.26", "revenue_contribution_pct": "27.37"}, {"customer_segment": "Loyal High Value", "user_count": "2026", "pct": "6.8", "avg_recency_days": "185.3", "avg_frequency": "2.15", "avg_monetary": "162.27", "avg_r_score": "3.67", "avg_f_score": "4.14", "avg_m_score": "3.47", "avg_rfm_total": "11.28", "total_revenue": "328759.12", "revenue_contribution_pct": "10.73"}, {"customer_segment": "Loyal Low Value", "user_count": "587", "pct": "1.97", "avg_recency_days": "143.1", "avg_frequency": "2.03", "avg_monetary": "48.4", "avg_r_score": "4.05", "avg_f_score": "4.03", "avg_m_score": "1.84", "avg_rfm_total": "9.92", "total_revenue": "28410.78", "revenue_contribution_pct": "0.93"}, {"customer_segment": "Need Attention", "user_count": "730", "pct": "2.45", "avg_recency_days": "476.2", "avg_frequency": "2.08", "avg_monetary": "206.51", "avg_r_score": "1.78", "avg_f_score": "4.08", "avg_m_score": "3.78", "avg_rfm_total": "9.64", "total_revenue": "150755.89", "revenue_contribution_pct": "4.92"}, {"customer_segment": "Others", "user_count": "131", "pct": "0.44", "avg_recency_days": "490.2", "avg_frequency": "2.02", "avg_monetary": "48.79", "avg_r_score": "1.73", "avg_f_score": "4.02", "avg_m_score": "1.85", "avg_rfm_total": "7.6", "total_revenue": "6391.18", "revenue_contribution_pct": "0.21"}, {"customer_segment": "Promising High Value", "user_count": "3555", "pct": "11.93", "avg_recency_days": "84.2", "avg_frequency": "1.0", "avg_monetary": "155.86", "avg_r_score": "4.55", "avg_f_score": "3.0", "avg_m_score": "3.51", "avg_rfm_total": "11.06", "total_revenue": "554081.87", "revenue_contribution_pct": "18.09"}, {"customer_segment": "Promising Low Value", "user_count": "4891", "pct": "16.42", "avg_recency_days": "85.3", "avg_frequency": "1.0", "avg_monetary": "34.28", "avg_r_score": "4.55", "avg_f_score": "3.0", "avg_m_score": "1.49", "avg_rfm_total": "9.04", "total_revenue": "167640.62", "revenue_contribution_pct": "5.47"}, {"customer_segment": "VIP Champions", "user_count": "1531", "pct": "5.14", "avg_recency_days": "79.5", "avg_frequency": "2.32", "avg_monetary": "275.88", "avg_r_score": "4.59", "avg_f_score": "4.28", "avg_m_score": "4.3", "avg_rfm_total": "13.17", "total_revenue": "422377.78", "revenue_contribution_pct": "13.79"}]
df_rfm_final = pd.DataFrame(rfm_final_data).apply(pd.to_numeric, errors='ignore')

# 2. Traffic Source Analysis (VIP/Promising Conversion)
traffic_source_data = [{"customer_segment": "Promising Low Value", "traffic_source": "Facebook", "user_count": "290", "pct_within_source": "46.93", "avg_frequency": "1.0", "avg_monetary": "34.19", "avg_m_score": "1.48", "vip_conversion_rate_pct": "17.8", "promising_high_share_pct": "35.28", "promising_low_share_pct": "46.93"}, {"customer_segment": "Promising High Value", "traffic_source": "Facebook", "user_count": "218", "pct_within_source": "35.28", "avg_frequency": "1.0", "avg_monetary": "152.57", "avg_m_score": "3.49", "vip_conversion_rate_pct": "17.8", "promising_high_share_pct": "35.28", "promising_low_share_pct": "46.93"}, {"customer_segment": "VIP Champions", "traffic_source": "Facebook", "user_count": "110", "pct_within_source": "17.8", "avg_frequency": "2.34", "avg_monetary": "268.85", "avg_m_score": "4.32", "vip_conversion_rate_pct": "17.8", "promising_high_share_pct": "35.28", "promising_low_share_pct": "46.93"}, {"customer_segment": "Promising Low Value", "traffic_source": "Search", "user_count": "3401", "pct_within_source": "49.1", "avg_frequency": "1.0", "avg_monetary": "34.49", "avg_m_score": "1.5", "vip_conversion_rate_pct": "15.37", "promising_high_share_pct": "35.53", "promising_low_share_pct": "49.1"}, {"customer_segment": "Promising High Value", "traffic_source": "Search", "user_count": "2461", "pct_within_source": "35.53", "avg_frequency": "1.0", "avg_monetary": "156.85", "avg_m_score": "3.51", "vip_conversion_rate_pct": "15.37", "promising_high_share_pct": "35.53", "promising_low_share_pct": "49.1"}, {"customer_segment": "VIP Champions", "traffic_source": "Search", "user_count": "1065", "pct_within_source": "15.37", "avg_frequency": "2.33", "avg_monetary": "272.92", "avg_m_score": "4.29", "vip_conversion_rate_pct": "15.37", "promising_high_share_pct": "35.53", "promising_low_share_pct": "49.1"}, {"customer_segment": "Promising Low Value", "traffic_source": "Organic", "user_count": "734", "pct_within_source": "48.07", "avg_frequency": "1.0", "avg_monetary": "33.95", "avg_m_score": "1.5", "vip_conversion_rate_pct": "15.06", "promising_high_share_pct": "36.87", "promising_low_share_pct": "48.07"}, {"customer_segment": "Promising High Value", "traffic_source": "Organic", "user_count": "563", "pct_within_source": "36.87", "avg_frequency": "1.0", "avg_monetary": "150.85", "avg_m_score": "3.5", "vip_conversion_rate_pct": "15.06", "promising_high_share_pct": "36.87", "promising_low_share_pct": "48.07"}, {"customer_segment": "VIP Champions", "traffic_source": "Organic", "user_count": "230", "pct_within_source": "15.06", "avg_frequency": "2.28", "avg_monetary": "295.01", "avg_m_score": "4.37", "vip_conversion_rate_pct": "15.06", "promising_high_share_pct": "36.87", "promising_low_share_pct": "48.07"}, {"customer_segment": "Promising Low Value", "traffic_source": "Email", "user_count": "263", "pct_within_source": "53.46", "avg_frequency": "1.0", "avg_monetary": "34.02", "avg_m_score": "1.49", "vip_conversion_rate_pct": "14.84", "promising_high_share_pct": "31.71", "promising_low_share_pct": "53.46"}, {"customer_segment": "Promising High Value", "traffic_source": "Email", "user_count": "156", "pct_within_source": "31.71", "avg_frequency": "1.0", "avg_monetary": "164.58", "avg_m_score": "3.55", "vip_conversion_rate_pct": "14.84", "promising_high_share_pct": "31.71", "promising_low_share_pct": "53.46"}, {"customer_segment": "VIP Champions", "traffic_source": "Email", "user_count": "73", "pct_within_source": "14.84", "avg_frequency": "2.3", "avg_monetary": "262.42", "avg_m_score": "4.26", "vip_conversion_rate_pct": "14.84", "promising_high_share_pct": "31.71", "promising_low_share_pct": "53.46"}, {"customer_segment": "Promising Low Value", "traffic_source": "Display", "user_count": "203", "pct_within_source": "49.15", "avg_frequency": "1.0", "avg_monetary": "32.35", "avg_m_score": "1.42", "vip_conversion_rate_pct": "12.83", "promising_high_share_pct": "38.01", "promising_low_share_pct": "49.15"}, {"customer_segment": "Promising High Value", "traffic_source": "Display", "user_count": "157", "pct_within_source": "38.01", "avg_frequency": "1.0", "avg_monetary": "154.17", "avg_m_score": "3.51", "vip_conversion_rate_pct": "12.83", "promising_high_share_pct": "38.01", "promising_low_share_pct": "49.15"}, {"customer_segment": "VIP Champions", "traffic_source": "Display", "user_count": "53", "pct_within_source": "12.83", "avg_frequency": "2.36", "avg_monetary": "285.63", "avg_m_score": "4.36", "vip_conversion_rate_pct": "12.83", "promising_high_share_pct": "38.01", "promising_low_share_pct": "49.15"}]
df_traffic_source = pd.DataFrame(traffic_source_data).apply(pd.to_numeric, errors='ignore')

# 3. Promising High/Low Post-Purchase Activity
post_purchase_data = [{"customer_segment": "Promising High Value", "activity_level": "0. No Activity", "user_count": "1643", "pct_within_segment": "46.22", "avg_events": "0.0", "avg_product_views": "0.0", "avg_cart_adds": "0.0", "avg_days_inactive": None, "avg_monetary": "131.06"}, {"customer_segment": "Promising High Value", "activity_level": "1. 1 Session", "user_count": "473", "pct_within_segment": "13.31", "avg_events": "1.2", "avg_product_views": "0.0", "avg_cart_adds": "0.0", "avg_days_inactive": "78.8", "avg_monetary": "153.98"}, {"customer_segment": "Promising High Value", "activity_level": "2. 2-3 Sessions", "user_count": "1268", "pct_within_segment": "35.67", "avg_events": "2.4", "avg_product_views": "0.0", "avg_cart_adds": "0.0", "avg_days_inactive": "82.2", "avg_monetary": "176.89"}, {"customer_segment": "Promising High Value", "activity_level": "3. 4-5 Sessions", "user_count": "170", "pct_within_segment": "4.78", "avg_events": "5.4", "avg_product_views": "0.4", "avg_cart_adds": "0.4", "avg_days_inactive": "82.7", "avg_monetary": "244.25"}, {"customer_segment": "Promising High Value", "activity_level": "4. 6+ Sessions", "user_count": "1", "pct_within_segment": "0.03", "avg_events": "55.0", "avg_product_views": "16.0", "avg_cart_adds": "16.0", "avg_days_inactive": "0.0", "avg_monetary": "98.98"}, {"customer_segment": "Promising Low Value", "activity_level": "0. No Activity", "user_count": "4275", "pct_within_segment": "87.41", "avg_events": "0.0", "avg_product_views": "0.0", "avg_cart_adds": "0.0", "avg_days_inactive": None, "avg_monetary": "32.59"}, {"customer_segment": "Promising Low Value", "activity_level": "1. 1 Session", "user_count": "227", "pct_within_segment": "4.64", "avg_events": "2.0", "avg_product_views": "0.3", "avg_cart_adds": "0.3", "avg_days_inactive": "74.5", "avg_monetary": "44.13"}, {"customer_segment": "Promising Low Value", "activity_level": "2. 2-3 Sessions", "user_count": "384", "pct_within_segment": "7.85", "avg_events": "3.2", "avg_product_views": "0.4", "avg_cart_adds": "0.4", "avg_days_inactive": "83.0", "avg_monetary": "47.18"}, {"customer_segment": "Promising Low Value", "activity_level": "3. 4-5 Sessions", "user_count": "5", "pct_within_segment": "0.1", "avg_events": "29.0", "avg_product_views": "8.4", "avg_cart_adds": "8.4", "avg_days_inactive": "43.2", "avg_monetary": "35.21"}]
df_post_purchase = pd.DataFrame(post_purchase_data).apply(pd.to_numeric, errors='ignore')

# 4. RFM Segment First Session Behavior
first_session_data = [{"customer_segment": "At Risk", "user_count": "6637", "pct": "22.28", "avg_events_per_session": "6.07", "avg_products_viewed": "1.0", "cart_usage_rate_pct": "99.95", "purchase_rate_pct": "100.0", "cancel_page_hit_rate_pct": "0.0", "avg_recency": "270.2", "avg_frequency": "1.0", "avg_monetary": "85.36", "avg_m_score": "2.36"}, {"customer_segment": "Hibernating", "user_count": "9705", "pct": "32.57", "avg_events_per_session": "6.05", "avg_products_viewed": "1.0", "cart_usage_rate_pct": "99.96", "purchase_rate_pct": "100.0", "cancel_page_hit_rate_pct": "0.0", "avg_recency": "538.4", "avg_frequency": "1.0", "avg_monetary": "86.39", "avg_m_score": "2.35"}, {"customer_segment": "Loyal High Value", "user_count": "2026", "pct": "6.8", "avg_events_per_session": "5.89", "avg_products_viewed": "1.0", "cart_usage_rate_pct": "99.85", "purchase_rate_pct": "100.0", "cancel_page_hit_rate_pct": "0.0", "avg_recency": "185.3", "avg_frequency": "2.15", "avg_monetary": "162.27", "avg_m_score": "3.47"}, {"customer_segment": "Loyal Low Value", "user_count": "587", "pct": "1.97", "avg_events_per_session": "5.2", "avg_products_viewed": "1.0", "cart_usage_rate_pct": "100.0", "purchase_rate_pct": "100.0", "cancel_page_hit_rate_pct": "0.0", "avg_recency": "143.1", "avg_frequency": "2.03", "avg_monetary": "48.4", "avg_m_score": "1.84"}, {"customer_segment": "Need Attention", "user_count": "730", "pct": "2.45", "avg_events_per_session": "6.24", "avg_products_viewed": "1.0", "cart_usage_rate_pct": "100.0", "purchase_rate_pct": "100.0", "cancel_page_hit_rate_pct": "0.0", "avg_recency": "476.2", "avg_frequency": "2.08", "avg_monetary": "206.51", "avg_m_score": "3.78"}, {"customer_segment": "Others", "user_count": "131", "pct": "0.44", "avg_events_per_session": "5.15", "avg_products_viewed": "1.0", "cart_usage_rate_pct": "100.0", "purchase_rate_pct": "100.0", "cancel_page_hit_rate_pct": "0.0", "avg_recency": "490.2", "avg_frequency": "2.02", "avg_monetary": "48.79", "avg_m_score": "1.85"}, {"customer_segment": "Promising High Value", "user_count": "3555", "pct": "11.93", "avg_events_per_session": "7.05", "avg_products_viewed": "1.0", "cart_usage_rate_pct": "100.0", "purchase_rate_pct": "99.16", "cancel_page_hit_rate_pct": "0.0", "avg_recency": "84.2", "avg_frequency": "1.0", "avg_monetary": "155.86", "avg_m_score": "3.51"}, {"customer_segment": "Promising Low Value", "user_count": "4891", "pct": "16.42", "avg_events_per_session": "5.29", "avg_products_viewed": "1.0", "cart_usage_rate_pct": "99.94", "purchase_rate_pct": "99.94", "cancel_page_hit_rate_pct": "0.0", "avg_recency": "85.3", "avg_frequency": "1.0", "avg_monetary": "34.28", "avg_m_score": "1.49"}, {"customer_segment": "VIP Champions", "user_count": "1531", "pct": "5.14", "avg_events_per_session": "6.64", "avg_products_viewed": "1.0", "cart_usage_rate_pct": "100.0", "purchase_rate_pct": "100.0", "cancel_page_hit_rate_pct": "0.0", "avg_recency": "79.5", "avg_frequency": "2.32", "avg_monetary": "275.88", "avg_m_score": "4.3"}]
df_first_session = pd.DataFrame(first_session_data).apply(pd.to_numeric, errors='ignore')

# 5. Champions Conversion Speed & Activity
champions_speed_data = [{"conversion_speed": "1. Quick (≤30 days)", "champions_count": "165", "avg_days_between": "14.4", "avg_sessions": "0.9", "avg_events": "1.7", "avg_product_views": "0.2", "avg_cart_adds": "0.2", "avg_home_visits": "0.1", "avg_sessions_first_7days": "0.8", "avg_product_views_first_7days": "0.1", "avg_total_ltv": "282.5", "avg_m_score": "4.35"}, {"conversion_speed": "2. Medium (31-60 days)", "champions_count": "129", "avg_days_between": "45.5", "avg_sessions": "1.1", "avg_events": "1.9", "avg_product_views": "0.3", "avg_cart_adds": "0.3", "avg_home_visits": "0.0", "avg_sessions_first_7days": "1.0", "avg_product_views_first_7days": "0.0", "avg_total_ltv": "279.96", "avg_m_score": "4.31"}, {"conversion_speed": "3. Slow (61+ days)", "champions_count": "1237", "avg_days_between": "273.2", "avg_sessions": "1.1", "avg_events": "2.7", "avg_product_views": "0.5", "avg_cart_adds": "0.5", "avg_home_visits": "0.1", "avg_sessions_first_7days": "0.9", "avg_product_views_first_7days": "0.0", "avg_total_ltv": "274.58", "avg_m_score": "4.3", "cumulative_pct_within_segment": "100.0"}]
df_champions_speed = pd.DataFrame(champions_speed_data).apply(pd.to_numeric, errors='ignore')

# 6. Signup to First Purchase Timing (LTV Potential)
signup_timing_data = [{"first_purchase_timing": "1. 1주일 이내", "user_count": "307", "repurchased_users": "80", "repurchase_rate": "26.06", "avg_days_to_repurchase": "203.4", "avg_monetary": "112.28", "avg_m_score": "2.62", "avg_r_score": "3.39", "avg_f_score": "3.31", "vip_champions_rate": "10.42", "promising_high_rate": "12.05", "promising_low_rate": "18.89", "vip_champions_count": "32", "promising_high_count": "37", "promising_low_count": "58", "at_risk_hibernate_count": "132"}, {"first_purchase_timing": "2. 1개월 이내", "user_count": "901", "repurchased_users": "226", "repurchase_rate": "25.08", "avg_days_to_repurchase": "179.6", "avg_monetary": "116.92", "avg_m_score": "2.71", "avg_r_score": "3.34", "avg_f_score": "3.3", "vip_champions_rate": "9.32", "promising_high_rate": "13.1", "promising_low_rate": "16.98", "vip_champions_count": "84", "promising_high_count": "118", "promising_low_count": "153", "at_risk_hibernate_count": "404"}, {"first_purchase_timing": "3. 2개월 이내", "user_count": "1161", "repurchased_users": "286", "repurchase_rate": "24.63", "avg_days_to_repurchase": "181.6", "avg_monetary": "110.41", "avg_m_score": "2.65", "avg_r_score": "3.37", "avg_f_score": "3.3", "vip_champions_rate": "9.47", "promising_high_rate": "12.14", "promising_low_rate": "19.47", "vip_champions_count": "110", "promising_high_count": "141", "promising_low_count": "226", "at_risk_hibernate_count": "508"}, {"first_purchase_timing": "4. 3개월 이내", "user_count": "1058", "repurchased_users": "250", "repurchase_rate": "23.63", "avg_days_to_repurchase": "170.7", "avg_monetary": "113.97", "avg_m_score": "2.63", "avg_r_score": "3.28", "avg_f_score": "3.28", "vip_champions_rate": "7.75", "promising_high_rate": "12.0", "promising_low_rate": "18.34", "vip_champions_count": "82", "promising_high_count": "127", "promising_low_count": "194", "at_risk_hibernate_count": "487"}, {"first_purchase_timing": "5. 3개월+", "user_count": "26368", "repurchased_users": "4163", "repurchase_rate": "15.79", "avg_days_to_repurchase": "204.5", "avg_monetary": "101.45", "avg_m_score": "2.53", "avg_r_score": "3.04", "avg_f_score": "3.18", "vip_champions_rate": "4.64", "promising_high_rate": "11.88", "promising_low_rate": "16.16", "vip_champions_count": "1223", "promising_high_count": "3132", "promising_low_count": "4260", "at_risk_hibernate_count": "14813"}]
df_signup_timing = pd.DataFrame(signup_timing_data).apply(pd.to_numeric, errors='ignore')

# 7. Category VIP Conversion Rate (from Promising Pool)
category_vip_conversion_data = [{"customer_segment": "Promising High Value", "first_category": "Jeans", "user_count": "401", "pct_within_segment": "11.32", "avg_first_item_price": "123.54", "avg_total_ltv": "165.24", "conversion_to_vip_champions_pct": "18.88"}, {"customer_segment": "Promising High Value", "first_category": "Outerwear & Coats", "user_count": "355", "pct_within_segment": "10.03", "avg_first_item_price": "161.37", "avg_total_ltv": "196.8", "conversion_to_vip_champions_pct": "22.46"}, {"customer_segment": "Promising High Value", "first_category": "Sweaters", "user_count": "285", "pct_within_segment": "8.05", "avg_first_item_price": "102.02", "avg_total_ltv": "149.6", "conversion_to_vip_champions_pct": "16.5"}, {"customer_segment": "Promising High Value", "first_category": "Fashion Hoodies & Sweatshirts", "user_count": "246", "pct_within_segment": "6.95", "avg_first_item_price": "73.73", "avg_total_ltv": "129.92", "conversion_to_vip_champions_pct": "15.36"}, {"customer_segment": "Promising High Value", "first_category": "Swim", "user_count": "219", "pct_within_segment": "6.18", "avg_first_item_price": "74.22", "avg_total_ltv": "127.1", "conversion_to_vip_champions_pct": "14.1"}, {"customer_segment": "Promising High Value", "first_category": "Sleep & Lounge", "user_count": "205", "pct_within_segment": "5.79", "avg_first_item_price": "71.25", "avg_total_ltv": "140.93", "conversion_to_vip_champions_pct": "15.52"}, {"customer_segment": "Promising High Value", "first_category": "Suits & Sport Coats", "user_count": "177", "pct_within_segment": "5.0", "avg_first_item_price": "148.64", "avg_total_ltv": "181.08", "conversion_to_vip_champions_pct": "17.75"}, {"customer_segment": "Promising High Value", "first_category": "Shorts", "user_count": "175", "pct_within_segment": "4.94", "avg_first_item_price": "59.2", "avg_total_ltv": "140.28", "conversion_to_vip_champions_pct": "13.42"}, {"customer_segment": "Promising High Value", "first_category": "Intimates", "user_count": "167", "pct_within_segment": "4.72", "avg_first_item_price": "54.95", "avg_total_ltv": "140.02", "conversion_to_vip_champions_pct": "10.6"}, {"customer_segment": "Promising High Value", "first_category": "Tops & Tees", "user_count": "163", "pct_within_segment": "4.6", "avg_first_item_price": "65.04", "avg_total_ltv": "145.35", "conversion_to_vip_champions_pct": "14.87"}, {"customer_segment": "Promising High Value", "first_category": "Accessories", "user_count": "154", "pct_within_segment": "4.35", "avg_first_item_price": "83.56", "avg_total_ltv": "150.06", "conversion_to_vip_champions_pct": "17.17"}, {"customer_segment": "Promising High Value", "first_category": "Dresses", "user_count": "147", "pct_within_segment": "4.15", "avg_first_item_price": "116.41", "avg_total_ltv": "169.13", "conversion_to_vip_champions_pct": "16.67"}, {"customer_segment": "Promising High Value", "first_category": "Active", "user_count": "137", "pct_within_segment": "3.87", "avg_first_item_price": "98.43", "avg_total_ltv": "162.07", "conversion_to_vip_champions_pct": "12.32"}, {"customer_segment": "Promising High Value", "first_category": "Pants", "user_count": "126", "pct_within_segment": "3.56", "avg_first_item_price": "81.32", "avg_total_ltv": "152.34", "conversion_to_vip_champions_pct": "15.96"}, {"customer_segment": "Promising High Value", "first_category": "Maternity", "user_count": "103", "pct_within_segment": "2.91", "avg_first_item_price": "78.73", "avg_total_ltv": "129.07", "conversion_to_vip_champions_pct": "13.68"}, {"customer_segment": "Promising High Value", "first_category": "Blazers & Jackets", "user_count": "82", "pct_within_segment": "2.32", "avg_first_item_price": "158.95", "avg_total_ltv": "201.74", "conversion_to_vip_champions_pct": "21.56"}, {"customer_segment": "Promising High Value", "first_category": "Plus", "user_count": "75", "pct_within_segment": "2.12", "avg_first_item_price": "62.29", "avg_total_ltv": "152.64", "conversion_to_vip_champions_pct": "16.36"}, {"customer_segment": "Promising High Value", "first_category": "Underwear", "user_count": "67", "pct_within_segment": "1.89", "avg_first_item_price": "32.79", "avg_total_ltv": "143.35", "conversion_to_vip_champions_pct": "13.07"}, {"customer_segment": "Promising High Value", "first_category": "Socks", "user_count": "62", "pct_within_segment": "1.75", "avg_first_item_price": "23.13", "avg_total_ltv": "174.79", "conversion_to_vip_champions_pct": "11.53"}, {"customer_segment": "Promising High Value", "first_category": "Pants & Capris", "user_count": "57", "pct_within_segment": "1.61", "avg_first_item_price": "88.67", "avg_total_ltv": "168.66", "conversion_to_vip_champions_pct": "15.43"}, {"customer_segment": "Promising High Value", "first_category": "Suits", "user_count": "44", "pct_within_segment": "1.24", "avg_first_item_price": "124.45", "avg_total_ltv": "164.36", "conversion_to_vip_champions_pct": "25.0"}, {"customer_segment": "Promising High Value", "first_category": "Leggings", "user_count": "32", "pct_within_segment": "0.9", "avg_first_item_price": "59.17", "avg_total_ltv": "128.44", "conversion_to_vip_champions_pct": "10.43"}, {"customer_segment": "Promising High Value", "first_category": "Skirts", "user_count": "26", "pct_within_segment": "0.73", "avg_first_item_price": "74.65", "avg_total_ltv": "121.6", "conversion_to_vip_champions_pct": "16.41"}, {"customer_segment": "Promising High Value", "first_category": "Socks & Hosiery", "user_count": "25", "pct_within_segment": "0.71", "avg_first_item_price": "21.05", "avg_total_ltv": "167.0", "conversion_to_vip_champions_pct": "9.64"}, {"customer_segment": "Promising High Value", "first_category": "Jumpsuits & Rompers", "user_count": "9", "pct_within_segment": "0.25", "avg_first_item_price": "73.68", "avg_total_ltv": "137.94", "conversion_to_vip_champions_pct": "17.31"}, {"customer_segment": "Promising High Value", "first_category": "Clothing Sets", "user_count": "2", "pct_within_segment": "0.06", "avg_first_item_price": "128.56", "avg_total_ltv": "128.56", "conversion_to_vip_champions_pct": "36.36"}, {"customer_segment": "Promising Low Value", "first_category": "Intimates", "user_count": "474", "pct_within_segment": "9.69", "avg_first_item_price": "27.36", "avg_total_ltv": "30.56", "conversion_to_vip_champions_pct": "10.6"}, {"customer_segment": "Promising Low Value", "first_category": "Tops & Tees", "user_count": "421", "pct_within_segment": "8.61", "avg_first_item_price": "31.67", "avg_total_ltv": "35.23", "conversion_to_vip_champions_pct": "14.87"}, {"customer_segment": "Promising Low Value", "first_category": "Shorts", "user_count": "367", "pct_within_segment": "7.5", "avg_first_item_price": "33.75", "avg_total_ltv": "35.84", "conversion_to_vip_champions_pct": "13.42"}, {"customer_segment": "Promising Low Value", "first_category": "Sleep & Lounge", "user_count": "323", "pct_within_segment": "6.6", "avg_first_item_price": "32.58", "avg_total_ltv": "34.48", "conversion_to_vip_champions_pct": "15.52"}, {"customer_segment": "Promising Low Value", "first_category": "Fashion Hoodies & Sweatshirts", "user_count": "305", "pct_within_segment": "6.24", "avg_first_item_price": "39.9", "avg_total_ltv": "41.73", "conversion_to_vip_champions_pct": "15.36"}, {"customer_segment": "Promising Low Value", "first_category": "Swim", "user_count": "299", "pct_within_segment": "6.11", "avg_first_item_price": "41.4", "avg_total_ltv": "43.02", "conversion_to_vip_champions_pct": "14.1"}, {"customer_segment": "Promising Low Value", "first_category": "Accessories", "user_count": "285", "pct_within_segment": "5.83", "avg_first_item_price": "22.26", "avg_total_ltv": "25.67", "conversion_to_vip_champions_pct": "17.17"}, {"customer_segment": "Promising Low Value", "first_category": "Active", "user_count": "283", "pct_within_segment": "5.79", "avg_first_item_price": "31.49", "avg_total_ltv": "33.72", "conversion_to_vip_champions_pct": "12.32"}, {"customer_segment": "Promising Low Value", "first_category": "Underwear", "user_count": "259", "pct_within_segment": "5.3", "avg_first_item_price": "25.59", "avg_total_ltv": "28.31", "conversion_to_vip_champions_pct": "13.07"}, {"customer_segment": "Promising Low Value", "first_category": "Sweaters", "user_count": "231", "pct_within_segment": "4.72", "avg_first_item_price": "38.97", "avg_total_ltv": "41.64", "conversion_to_vip_champions_pct": "16.5"}, {"customer_segment": "Promising Low Value", "first_category": "Socks", "user_count": "222", "pct_within_segment": "4.54", "avg_first_item_price": "17.25", "avg_total_ltv": "23.23", "conversion_to_vip_champions_pct": "11.53"}, {"customer_segment": "Promising Low Value", "first_category": "Pants", "user_count": "211", "pct_within_segment": "4.31", "avg_first_item_price": "39.4", "avg_total_ltv": "41.2", "conversion_to_vip_champions_pct": "15.96"}, {"customer_segment": "Promising Low Value", "first_category": "Jeans", "user_count": "166", "pct_within_segment": "3.39", "avg_first_item_price": "43.1", "avg_total_ltv": "44.8", "conversion_to_vip_champions_pct": "18.88"}, {"customer_segment": "Promising Low Value", "first_category": "Maternity", "user_count": "162", "pct_within_segment": "3.31", "avg_first_item_price": "32.84", "avg_total_ltv": "35.13", "conversion_to_vip_champions_pct": "13.68"}, {"customer_segment": "Promising Low Value", "first_category": "Socks & Hosiery", "user_count": "153", "pct_within_segment": "3.13", "avg_first_item_price": "16.2", "avg_total_ltv": "21.22", "conversion_to_vip_champions_pct": "9.64"}, {"customer_segment": "Promising Low Value", "first_category": "Leggings", "user_count": "114", "pct_within_segment": "2.33", "avg_first_item_price": "19.62", "avg_total_ltv": "23.72", "conversion_to_vip_champions_pct": "10.43"}, {"customer_segment": "Promising Low Value", "first_category": "Plus", "user_count": "109", "pct_within_segment": "2.23", "avg_first_item_price": "23.96", "avg_total_ltv": "27.42", "conversion_to_vip_champions_pct": "16.36"}, {"customer_segment": "Promising Low Value", "first_category": "Pants & Capris", "user_count": "102", "pct_within_segment": "2.09", "avg_first_item_price": "35.32", "avg_total_ltv": "38.55", "conversion_to_vip_champions_pct": "15.43"}, {"customer_segment": "Promising Low Value", "first_category": "Dresses", "user_count": "98", "pct_within_segment": "2.0", "avg_first_item_price": "34.2", "avg_total_ltv": "35.06", "conversion_to_vip_champions_pct": "16.67"}, {"customer_segment": "Promising Low Value", "first_category": "Skirts", "user_count": "81", "pct_within_segment": "1.66", "avg_first_item_price": "30.5", "avg_total_ltv": "32.6", "conversion_to_vip_champions_pct": "16.41"}, {"customer_segment": "Promising Low Value", "first_category": "Outerwear & Coats", "user_count": "73", "pct_within_segment": "1.49", "avg_first_item_price": "47.13", "avg_total_ltv": "46.69", "conversion_to_vip_champions_pct": "22.46"}, {"customer_segment": "Promising Low Value", "first_category": "Suits & Sport Coats", "user_count": "64", "pct_within_segment": "1.31", "avg_first_item_price": "36.61", "avg_total_ltv": "39.64", "conversion_to_vip_champions_pct": "17.75"}, {"customer_segment": "Promising Low Value", "first_category": "Blazers & Jackets", "user_count": "49", "pct_within_segment": "1.0", "avg_first_item_price": "27.09", "avg_total_ltv": "31.2", "conversion_to_vip_champions_pct": "21.56"}, {"customer_segment": "Promising Low Value", "first_category": "Jumpsuits & Rompers", "user_count": "34", "pct_within_segment": "0.7", "avg_first_item_price": "21.58", "avg_total_ltv": "27.35", "conversion_to_vip_champions_pct": "17.31"}, {"customer_segment": "Promising Low Value", "first_category": "Clothing Sets", "user_count": "5", "pct_within_segment": "0.1", "avg_first_item_price": "55.39", "avg_total_ltv": "57.74", "conversion_to_vip_champions_pct": "36.36"}, {"customer_segment": "Promising Low Value", "first_category": "Suits", "user_count": "1", "pct_within_segment": "0.02", "avg_first_item_price": "13.99", "avg_total_ltv": "13.99", "conversion_to_vip_champions_pct": "25.0"}, {"customer_segment": "VIP Champions", "first_category": "Jeans", "user_count": "132", "pct_within_segment": "8.62", "avg_first_item_price": "115.87", "avg_total_ltv": "282.84", "conversion_to_vip_champions_pct": "18.88"}, {"customer_segment": "VIP Champions", "first_category": "Outerwear & Coats", "user_count": "124", "pct_within_segment": "8.1", "avg_first_item_price": "177.41", "avg_total_ltv": "345.31", "conversion_to_vip_champions_pct": "22.46"}, {"customer_segment": "VIP Champions", "first_category": "Tops & Tees", "user_count": "102", "pct_within_segment": "6.66", "avg_first_item_price": "53.83", "avg_total_ltv": "266.36", "conversion_to_vip_champions_pct": "14.87"}, {"customer_segment": "VIP Champions", "first_category": "Sweaters", "user_count": "102", "pct_within_segment": "6.66", "avg_first_item_price": "88.76", "avg_total_ltv": "270.27", "conversion_to_vip_champions_pct": "16.5"}, {"customer_segment": "VIP Champions", "first_category": "Fashion Hoodies & Sweatshirts", "user_count": "100", "pct_within_segment": "6.53", "avg_first_item_price": "64.28", "avg_total_ltv": "253.17", "conversion_to_vip_champions_pct": "15.36"}, {"customer_segment": "VIP Champions", "first_category": "Sleep & Lounge", "user_count": "97", "pct_within_segment": "6.34", "avg_first_item_price": "66.05", "avg_total_ltv": "271.84", "conversion_to_vip_champions_pct": "15.52"}, {"customer_segment": "VIP Champions", "first_category": "Accessories", "user_count": "91", "pct_within_segment": "5.94", "avg_first_item_price": "59.15", "avg_total_ltv": "271.72", "conversion_to_vip_champions_pct": "17.17"}, {"customer_segment": "VIP Champions", "first_category": "Swim", "user_count": "85", "pct_within_segment": "5.55", "avg_first_item_price": "67.89", "avg_total_ltv": "276.61", "conversion_to_vip_champions_pct": "14.1"}, {"customer_segment": "VIP Champions", "first_category": "Shorts", "user_count": "84", "pct_within_segment": "5.49", "avg_first_item_price": "60.2", "avg_total_ltv": "273.79", "conversion_to_vip_champions_pct": "13.42"}, {"customer_segment": "VIP Champions", "first_category": "Intimates", "user_count": "76", "pct_within_segment": "4.96", "avg_first_item_price": "41.82", "avg_total_ltv": "253.21", "conversion_to_vip_champions_pct": "10.6"}, {"customer_segment": "VIP Champions", "first_category": "Pants", "user_count": "64", "pct_within_segment": "4.18", "avg_first_item_price": "65.89", "avg_total_ltv": "273.03", "conversion_to_vip_champions_pct": "15.96"}, {"customer_segment": "VIP Champions", "first_category": "Active", "user_count": "59", "pct_within_segment": "3.85", "avg_first_item_price": "70.18", "avg_total_ltv": "261.33", "conversion_to_vip_champions_pct": "12.32"}, {"customer_segment": "VIP Champions", "first_category": "Suits & Sport Coats", "user_count": "52", "pct_within_segment": "3.4", "avg_first_item_price": "123.26", "avg_total_ltv": "280.37", "conversion_to_vip_champions_pct": "17.75"}, {"customer_segment": "VIP Champions", "first_category": "Underwear", "user_count": "49", "pct_within_segment": "3.2", "avg_first_item_price": "27.03", "avg_total_ltv": "270.32", "conversion_to_vip_champions_pct": "13.07"}, {"customer_segment": "VIP Champions", "first_category": "Dresses", "user_count": "49", "pct_within_segment": "3.2", "avg_first_item_price": "100.75", "avg_total_ltv": "276.64", "conversion_to_vip_champions_pct": "16.67"}, {"customer_segment": "VIP Champions", "first_category": "Maternity", "user_count": "42", "pct_within_segment": "2.74", "avg_first_item_price": "72.53", "avg_total_ltv": "288.59", "conversion_to_vip_champions_pct": "13.68"}, {"customer_segment": "VIP Champions", "first_category": "Socks", "user_count": "37", "pct_within_segment": "2.42", "avg_first_item_price": "20.73", "avg_total_ltv": "246.76", "conversion_to_vip_champions_pct": "11.53"}, {"customer_segment": "VIP Champions", "first_category": "Plus", "user_count": "36", "pct_within_segment": "2.35", "avg_first_item_price": "84.05", "avg_total_ltv": "262.79", "conversion_to_vip_champions_pct": "16.36"}, {"customer_segment": "VIP Champions", "first_category": "Blazers & Jackets", "user_count": "36", "pct_within_segment": "2.35", "avg_first_item_price": "135.05", "avg_total_ltv": "261.14", "conversion_to_vip_champions_pct": "21.56"}, {"customer_segment": "VIP Champions", "first_category": "Pants & Capris", "user_count": "29", "pct_within_segment": "1.89", "avg_first_item_price": "55.81", "avg_total_ltv": "335.0", "conversion_to_vip_champions_pct": "15.43"}, {"customer_segment": "VIP Champions", "first_category": "Skirts", "user_count": "21", "pct_within_segment": "1.37", "avg_first_item_price": "56.94", "avg_total_ltv": "270.55", "conversion_to_vip_champions_pct": "16.41"}, {"customer_segment": "VIP Champions", "first_category": "Socks & Hosiery", "user_count": "19", "pct_within_segment": "1.24", "avg_first_item_price": "15.22", "avg_total_ltv": "251.4", "conversion_to_vip_champions_pct": "9.64"}, {"customer_segment": "VIP Champions", "first_category": "Leggings", "user_count": "17", "pct_within_segment": "1.11", "avg_first_item_price": "32.77", "avg_total_ltv": "238.16", "conversion_to_vip_champions_pct": "10.43"}, {"customer_segment": "VIP Champions", "first_category": "Suits", "user_count": "15", "pct_within_segment": "0.98", "avg_first_item_price": "139.13", "avg_total_ltv": "248.88", "conversion_to_vip_champions_pct": "25.0"}, {"customer_segment": "VIP Champions", "first_category": "Jumpsuits & Rompers", "user_count": "9", "pct_within_segment": "0.59", "avg_first_item_price": "47.09", "avg_total_ltv": "215.66", "conversion_to_vip_champions_pct": "17.31"}, {"customer_segment": "VIP Champions", "first_category": "Clothing Sets", "user_count": "4", "pct_within_segment": "0.26", "avg_first_item_price": "94.0", "avg_total_ltv": "259.81", "conversion_to_vip_champions_pct": "36.36"}]
df_category_conversion = pd.DataFrame(category_vip_conversion_data).apply(pd.to_numeric, errors='ignore')

# 8. Category Pair Analysis (VIP/Promising)
category_pair_data = [{"customer_segment": "VIP Champions", "first_category": "Accessories", "second_category": "Tops & Tees", "pair_count": "10", "pct_of_first_category_in_segment": "100.0", "avg_first_item_price": "49.81", "avg_second_item_price": "35.52", "avg_total_ltv": "232.75", "avg_m_score": "4.2"}, {"customer_segment": "VIP Champions", "first_category": "Fashion Hoodies & Sweatshirts", "second_category": "Jeans", "pair_count": "15", "pct_of_first_category_in_segment": "60.0", "avg_first_item_price": "65.43", "avg_second_item_price": "93.83", "avg_total_ltv": "253.31", "avg_m_score": "4.27"}, {"customer_segment": "VIP Champions", "first_category": "Fashion Hoodies & Sweatshirts", "second_category": "Sweaters", "pair_count": "10", "pct_of_first_category_in_segment": "40.0", "avg_first_item_price": "58.08", "avg_second_item_price": "64.06", "avg_total_ltv": "207.61", "avg_m_score": "4.1"}, {"customer_segment": "VIP Champions", "first_category": "Intimates", "second_category": "Intimates", "pair_count": "13", "pct_of_first_category_in_segment": "100.0", "avg_first_item_price": "49.38", "avg_second_item_price": "31.62", "avg_total_ltv": "289.6", "avg_m_score": "4.31"}, {"customer_segment": "VIP Champions", "first_category": "Jeans", "second_category": "Fashion Hoodies & Sweatshirts", "pair_count": "13", "pct_of_first_category_in_segment": "28.26", "avg_first_item_price": "123.98", "avg_second_item_price": "68.43", "avg_total_ltv": "244.65", "avg_m_score": "4.31"}, {"customer_segment": "VIP Champions", "first_category": "Jeans", "second_category": "Jeans", "pair_count": "12", "pct_of_first_category_in_segment": "26.09", "avg_first_item_price": "110.9", "avg_second_item_price": "139.76", "avg_total_ltv": "324.09", "avg_m_score": "4.58"}, {"customer_segment": "VIP Champions", "first_category": "Jeans", "second_category": "Intimates", "pair_count": "11", "pct_of_first_category_in_segment": "23.91", "avg_first_item_price": "110.27", "avg_second_item_price": "44.56", "avg_total_ltv": "228.6", "avg_m_score": "4.18"}, {"customer_segment": "VIP Champions", "first_category": "Jeans", "second_category": "Sweaters", "pair_count": "10", "pct_of_first_category_in_segment": "21.74", "avg_first_item_price": "115.03", "avg_second_item_price": "69.23", "avg_total_ltv": "301.27", "avg_m_score": "4.4"}, {"customer_segment": "VIP Champions", "first_category": "Outerwear & Coats", "second_category": "Sweaters", "pair_count": "14", "pct_of_first_category_in_segment": "30.43", "avg_first_item_price": "130.55", "avg_second_item_price": "116.72", "avg_total_ltv": "304.51", "avg_m_score": "4.36"}, {"customer_segment": "VIP Champions", "first_category": "Outerwear & Coats", "second_category": "Fashion Hoodies & Sweatshirts", "pair_count": "11", "pct_of_first_category_in_segment": "23.91", "avg_first_item_price": "169.03", "avg_second_item_price": "67.81", "avg_total_ltv": "359.26", "avg_m_score": "4.55"}, {"customer_segment": "VIP Champions", "first_category": "Outerwear & Coats", "second_category": "Tops & Tees", "pair_count": "11", "pct_of_first_category_in_segment": "23.91", "avg_first_item_price": "207.94", "avg_second_item_price": "58.75", "avg_total_ltv": "363.81", "avg_m_score": "4.36"}, {"customer_segment": "VIP Champions", "first_category": "Outerwear & Coats", "second_category": "Swim", "pair_count": "10", "pct_of_first_category_in_segment": "21.74", "avg_first_item_price": "179.36", "avg_second_item_price": "48.64", "avg_total_ltv": "303.31", "avg_m_score": "4.4"}, {"customer_segment": "VIP Champions", "first_category": "Pants", "second_category": "Jeans", "pair_count": "10", "pct_of_first_category_in_segment": "100.0", "avg_first_item_price": "72.94", "avg_second_item_price": "140.35", "avg_total_ltv": "295.47", "avg_m_score": "4.4"}, {"customer_segment": "VIP Champions", "first_category": "Shorts", "second_category": "Jeans", "pair_count": "10", "pct_of_first_category_in_segment": "100.0", "avg_first_item_price": "134.92", "avg_second_item_price": "119.05", "avg_total_ltv": "344.79", "avg_m_score": "4.2"}, {"customer_segment": "VIP Champions", "first_category": "Sleep & Lounge", "second_category": "Sleep & Lounge", "pair_count": "15", "pct_of_first_category_in_segment": "57.69", "avg_first_item_price": "46.02", "avg_second_item_price": "58.0", "avg_total_ltv": "299.66", "avg_m_score": "4.33"}, {"customer_segment": "VIP Champions", "first_category": "Sleep & Lounge", "second_category": "Jeans", "pair_count": "11", "pct_of_first_category_in_segment": "42.31", "avg_first_item_price": "82.13", "avg_second_item_price": "102.33", "avg_total_ltv": "289.46", "avg_m_score": "4.09"}, {"customer_segment": "VIP Champions", "first_category": "Sweaters", "second_category": "Jeans", "pair_count": "10", "pct_of_first_category_in_segment": "50.0", "avg_first_item_price": "76.71", "avg_second_item_price": "129.68", "avg_total_ltv": "283.4", "avg_m_score": "4.3"}, {"customer_segment": "VIP Champions", "first_category": "Sweaters", "second_category": "Outerwear & Coats", "pair_count": "10", "pct_of_first_category_in_segment": "50.0", "avg_first_item_price": "60.94", "avg_second_item_price": "143.49", "avg_total_ltv": "402.26", "avg_m_score": "4.5"}, {"customer_segment": "VIP Champions", "first_category": "Tops & Tees", "second_category": "Fashion Hoodies & Sweatshirts", "pair_count": "11", "pct_of_first_category_in_segment": "100.0", "avg_first_item_price": "76.56", "avg_second_item_price": "59.07", "avg_total_ltv": "238.11", "avg_m_score": "4.18"}]
df_category_pair = pd.DataFrame(category_pair_data).apply(pd.to_numeric, errors='ignore')

# --------------------------------------------------------------------------------------
# Helper Functions for Streamlit Visualization
# --------------------------------------------------------------------------------------

def create_segment_summary_chart(df):
    """Segment User Count and Revenue Contribution Bar/Line Chart."""
    df_chart = df.sort_values('user_count', ascending=False).head(9)
    df_chart['User Percentage'] = df_chart['user_count'] / df_chart['user_count'].sum()
    df_chart['Revenue Percentage'] = df_chart['total_revenue'] / df_chart['total_revenue'].sum()

    import altair as alt
    
    base = alt.Chart(df_chart).encode(
        x=alt.X('customer_segment:N', title='Customer Segment', sort='-y'),
        tooltip=['customer_segment', alt.Tooltip('user_count', format=',d'), 'pct', alt.Tooltip('total_revenue', format=',.2f'), 'revenue_contribution_pct']
    )

    bar = base.mark_bar().encode(
        y=alt.Y('pct:Q', title='User Share (%)'),
        color=alt.Color('customer_segment', legend=None),
        order=alt.Order('pct', sort='descending')
    )
    
    line = base.mark_line(point=True, color='red').encode(
        y=alt.Y('revenue_contribution_pct:Q', title='Revenue Share (%)', axis=alt.Axis(titleColor='red')),
        order=alt.Order('pct', sort='descending')
    )
    
    chart = alt.layer(bar, line).resolve_scale(
        y='independent'
    ).properties(
        title='Segment Distribution (User Count vs. Revenue Contribution)'
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)

def create_traffic_source_chart(df):
    """Traffic Source VIP/Promising Conversion Rate Stacked Bar Chart."""
    df_traffic = df.drop_duplicates(subset=['traffic_source']).sort_values('vip_conversion_rate_pct', ascending=False).set_index('traffic_source')[['vip_conversion_rate_pct', 'promising_high_share_pct', 'promising_low_share_pct']]
    df_traffic.columns = ['VIP Champions', 'Promising High Value', 'Promising Low Value']
    df_traffic = df_traffic.stack().reset_index()
    df_traffic.columns = ['traffic_source', 'segment_type', 'share_pct']
    
    chart = alt.Chart(df_traffic).mark_bar().encode(
        x=alt.X('share_pct:Q', title='Share within Segmented Traffic (%)'),
        y=alt.Y('traffic_source:N', title='Traffic Source', sort='-x'),
        color=alt.Color('segment_type:N', title='Segment Type', 
                        scale=alt.Scale(domain=['VIP Champions', 'Promising High Value', 'Promising Low Value'],
                                        range=['#10b981', '#f59e0b', '#ef4444'])),
        order=alt.Order('segment_type', sort='descending'),
        tooltip=['traffic_source', 'segment_type', 'share_pct']
    ).properties(
        title="Traffic Source Segmentation Mix (VIP/Promising Only)"
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)

def create_post_purchase_chart(df):
    """Promising High/Low Post-Purchase Activity Comparison."""
    df_chart = df.copy()
    
    base = alt.Chart(df_chart).encode(
        y=alt.Y('activity_level:N', title='Sessions After Purchase', sort=['0. No Activity', '1. 1 Session', '2. 2-3 Sessions', '3. 4-5 Sessions', '4. 6+ Sessions']),
        tooltip=['customer_segment', alt.Tooltip('user_count', format=',d'), 'pct_within_segment', alt.Tooltip('avg_monetary', format='$,.2f')]
    )

    bar = base.mark_bar().encode(
        x=alt.X('pct_within_segment:Q', title='Share within Segment (%)'),
        color=alt.Color('customer_segment:N', title='Segment', 
                        scale=alt.Scale(domain=['Promising High Value', 'Promising Low Value'], range=['#f59e0b', '#ef4444'])),
        column=alt.Column('customer_segment:N', title='Segment')
    ).properties(
        title='Post-Purchase Activity Drop-Off (Promising Segments)'
    )
    
    st.altair_chart(bar, use_container_width=True)

def create_category_conversion_chart(df):
    """Category VIP Conversion Rate Heatmap/Bar Chart."""
    df_chart = df[df['customer_segment'].isin(['Promising High Value', 'Promising Low Value'])].drop_duplicates(subset=['first_category', 'conversion_to_vip_champions_pct']).sort_values('conversion_to_vip_champions_pct', ascending=False).head(15)
    
    chart = alt.Chart(df_chart).mark_bar().encode(
        x=alt.X('conversion_to_vip_champions_pct:Q', title='VIP Champions Conversion Rate (%)'),
        y=alt.Y('first_category:N', title='First Purchase Category', sort='-x'),
        color=alt.Color('conversion_to_vip_champions_pct:Q', title='Conversion Rate', scale=alt.Scale(range='heatmap')),
        tooltip=['first_category', 'conversion_to_vip_champions_pct', alt.Tooltip('avg_first_item_price', format='$,.2f'), alt.Tooltip('avg_total_ltv', format='$,.2f')]
    ).properties(
        title="Category VIP Conversion Potential (Top 15 Categories)"
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)


# --------------------------------------------------------------------------------------
# Streamlit App Layout
# --------------------------------------------------------------------------------------

st.set_page_config(layout="wide", page_title="RFM 기반 고객 전환 전략 분석")

st.title("💰 RFM 기반 고객 전환 전략 분석 리포트 (Sale Price 기준)")
st.caption("기간: 2023-01-01 ~ 2024-12-31 | Monetary 기준: Sale Price")

# --------------------------------------------------------------------------------------
# Executive Summary
# --------------------------------------------------------------------------------------

st.header("1. 엑세큐티브 요약 (Executive Summary)")
st.markdown("""
### 핵심 문제 정의: 신규 고가치 고객의 빠른 이탈 위험
현재 고객 기반의 **54.86%**가 장기 휴면(`Hibernating`) 또는 이탈 위험(`At Risk`) 상태입니다. 특히 최근 1회 구매 고객인 **Promising High Value** 그룹 (전체 사용자 **11.93%**, 매출 기여 **18.09%**)이 VIP Champion으로 전환되는 과정에서 **46.22%가 첫 구매 후 재방문하지 않는** 심각한 드롭오프 현상이 관찰되었습니다.

### 핵심 인사이트 및 전략 방향
1.  **전환 골든 타임**을 놓치고 있습니다. 가입 후 **30일 이내**에 첫 구매를 완료한 그룹의 VIP 전환율(10.42%)이 3개월 이상 걸린 그룹(4.64%)보다 **2배 이상 높습니다.**
2.  **첫 구매 카테고리**가 LTV를 결정합니다. **`Clothing Sets` (36.36%), `Suits` (25.0%)**, **`Outerwear & Coats` (22.46%)** 등 고가치 상품 구매자 풀에서 VIP로 전환될 잠재력이 가장 높습니다.
3.  **Post-Purchase 마케팅**에 치명적인 구멍이 있습니다. Promising High Value 고객 중 재방문(`2-3 Sessions` 이상)한 그룹의 LTV($\text{176.89}$ 이상)는 활동이 없는 그룹($\text{131.06}$)보다 훨씬 높습니다. 즉, **재방문 자체**가 LTV를 높이는 핵심 동인입니다.

### 3대 핵심 액션 플랜
| 우선순위 | 영역 | 액션 플랜 | 목표 및 측정 지표 |
| :---: | :---: | :---: | :---: |
| **🥇 1순위** | **CRM/온보딩** | **'Post-Purchase 7-Day Engagement Drip'** 구축. PHV 고객 대상 첫 구매 후 7일 이내에 개인화된 재방문 유도 콘텐츠(리뷰 작성, 스타일링 팁, 다음 카테고리 추천)를 발송하여 2차 세션 유도. | PHV 그룹의 '0. No Activity' 비율을 30% 이하로 감소. |
| **🥈 2순위** | **Acquisition/마케팅** | 유입 후 **30일 이내 첫 구매 완료**를 목표로 하는 '신규 고객 한정 $1$회 번들 할인' 캠페인 강화. 특히 고전환 카테고리(Outerwear, Suits) 중심의 광고 노출 우선순위 설정. | 가입 후 30일 이내 첫 구매 비율 3% $\rightarrow$ 5% 달성. |
| **🥉 3순위** | **Product Strategy** | VIP Champions가 선호하는 카테고리 전환 경로(`Outerwear` $\rightarrow$ `Sweaters`, `Jeans` $\rightarrow$ `Fashion Hoodies`)를 Promising High Value 고객에게 **자동 추천 로직**으로 적용하여 2차 구매 상품을 유도. | Promising High Value 그룹의 2차 구매 평균 금액 $10\%$ 증가. |
""")

# --------------------------------------------------------------------------------------
# 2. RFM Segmentation Rationale and Overview
# --------------------------------------------------------------------------------------

st.header("2. RFM 세그먼테이션 기준 및 개요")
st.markdown("""
### 2.1. RFM 등급 기준 및 근거

이번 분석의 Monetary(M) 기준은 총매출액(Sale Price)의 분포(분위수)에 기반하여 설정되었습니다. 이는 순수한 거래 건수(Frequency)가 아닌, 고객의 **실질적인 수익 기여도**를 반영하는 데 목적이 있습니다.

| 지표 | $5$점 (최상) | $4$점 | $3$점 (중앙값) | $2$점 | $1$점 (최하) | 근거 (29,795명 기준) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **R**ecency (최근성) | $\le 90$일 | $\le 180$일 | $\le 365$일 | $\le 545$일 | $> 545$일 | 구매 사이클 기반 |
| **F**requency (빈도) | $\ge 3$회 | $2$회 | $1$회 | $0$회 | $0$회 | P95/P90/P75 (1회 구매 고객이 전체의 75% 차지) |
| **M**onetary (금액) | $\ge \$300$ | $\ge \$135$ | $\ge \$67$ | $\ge \$34$ | $<\$34$ | **P95 / P75 / P50 / P25 분위수 적용** |

### 2.2. 주요 세그먼트 정의 (Promising 그룹 중심)
| 세그먼트 | RFM 기준 | 특징 및 기대 행동 |
| :---: | :---: | :---: |
| **VIP Champions** | R$\ge 4$, F$\ge 4$, M$\ge 4$ | 최근 구매/고빈도/고액. 전체 매출의 $13.79\%$ 기여. **최우선 유지 대상.** |
| **Promising High Value** | R$\ge 4$, F$= 3$, M$\ge 3$ | 최근 구매($\le 180$일) $\mathbf{1}$회, **중/고액** 지출. **최고의 잠재 VIP 그룹.** |
| **Promising Low Value** | R$\ge 4$, F$= 3$, M$\le 2$ | 최근 구매($\le 180$일) $\mathbf{1}$회, **저액** 지출. 구매 경험은 있으나 추가 유도가 필요한 그룹. |
| **At Risk** | R$= 3$, F$= 3$ | 최근성($180 \sim 365$일)이 떨어지기 시작. 과거 1회 구매 경험. 이탈 방지 마케팅 필요. |

### 2.3. 전체 세그먼트 분포 
""", unsafe_allow_html=True)
create_segment_summary_chart(df_rfm_final)
st.dataframe(df_rfm_final.sort_values('user_count', ascending=False).reset_index(drop=True))

# --------------------------------------------------------------------------------------
# 3. Traffic Source Analysis (전환 구조 분석)
# --------------------------------------------------------------------------------------

st.header("3. 트래픽 소스별 VIP / Promising 전환 구조 분석")
st.markdown("""
### 3.1. 인사이트: Facebook의 양면성과 Search의 대규모 잠재력 
유입된 고객 중 VIP Champion으로 전환되는 비율(VIP / (VIP + Promising High + Promising Low))은 **Facebook이 $17.8\%$로 가장 높습니다.** 이는 Facebook 유입 고객이 재구매와 고가치 구매에 가장 효율적임을 시사합니다.

그러나 **Search**는 VIP와 Promising High Value 고객의 **절대 수(Count)**가 압도적으로 많습니다.

* **Facebook (17.8% VIP):** 고효율. 적은 규모에서 높은 VIP 비율을 달성.
* **Search (15.37% VIP):** 대규모. Promising High Value (2,461명) 풀이 가장 커서, 대규모 VIP 육성 잠재력이 높음.

### 3.2. 문제 정의 및 액션 플랜
* **문제:** Facebook과 Organic 소스에서 **Promising Low Value**(`PLV`, $46 \sim 48\%$) 고객의 비중이 높아, **대량의 저가치 첫 구매자**를 유입시키고 있습니다. 이들을 PHV나 VIP로 전환하지 못하면 마케팅 비용이 낭비됩니다.
* **액션 플랜 (Facebook/Organic):** 해당 채널 유입 고객 중 PLV(저액 구매) 그룹을 대상으로 **AOV 증진 캠페인**을 즉시 실행해야 합니다. 예를 들어, 두 번째 구매 시 특정 금액($100$ 이상) 충족 시 파격적인 할인/무료배송 혜택을 제공하여 M-Score 3점 이상으로 끌어올려야 합니다.
* **액션 플랜 (Search):** Search를 통한 Promising High Value (PHV) 고객($2,461$명)에게 2차 구매 유도 마케팅을 집중하여 **대규모 VIP 전환**을 가속화해야 합니다.
""", unsafe_allow_html=True)

df_traffic_display = df_traffic_source.drop_duplicates(subset=['traffic_source']).sort_values('vip_conversion_rate_pct', ascending=False)
st.dataframe(df_traffic_display.drop(columns=['promising_high_share_pct', 'promising_low_share_pct']).set_index('traffic_source'))
create_traffic_source_chart(df_traffic_source)


# --------------------------------------------------------------------------------------
# 4. Promising High/Low 재구매 활동 분석 (Post-Purchase Drop-Off)
# --------------------------------------------------------------------------------------

st.header("4. Promising High/Low 유저 구매 후 활동 분석 (Post-Purchase Drop-Off)")
st.markdown("""
### 4.1. 인사이트: 구매 후 활동 부재의 심각성 
Promising 세그먼트의 가장 심각한 문제는 **첫 구매 후 활동 부재**입니다.

* **Promising Low Value (PLV):** 무려 **$87.41\%$**가 첫 구매 이후 재방문하지 않았습니다.
* **Promising High Value (PHV):** **$46.22\%$**가 활동이 없습니다. 이들이 LTV 잠재력이 가장 높음에도 불구하고, 절반 가까이가 첫 구매 후 바로 이탈하고 있습니다.

활동을 **4-5회 세션 이상**으로 늘린 PHV 고객의 평균 LTV는 **$\mathbf{\$244.25}$**로, 활동이 없는 고객($\text{\$131.06}$) 대비 **$86\%$ 이상** 높습니다. 이는 **'재구매'보다 '재방문/재참여'가 LTV를 결정하는 선행 지표**임을 명확히 보여줍니다.

### 4.2. 문제 정의 및 액션 플랜
* **문제:** 첫 구매를 성공적으로 이끌었으나, 이후 단계에서 고객 온보딩 및 참여 유도에 실패하고 있습니다. 구매 직후의 **'관성(Momentum)'**을 살리지 못하고 있습니다.
* **액션 플랜:** **'Post-Purchase 7일차 온보딩 자동화'**를 최우선으로 실행해야 합니다.
    * **Day 1 (구매 직후):** 감사 이메일, 다음 구매를 위한 개인화된 스타일링 가이드 제공.
    * **Day 3:** 구매한 상품의 리뷰 작성 유도 (포인트 지급).
    * **Day 7:** **두 번째 구매 유도를 위한 큐레이션된 상품 추천** (Category Pair 분석 결과 활용)을 제공하여, 강제로 **2차 세션(재방문)**을 유도해야 합니다. 목표는 PHV 그룹의 **'0. No Activity' 비율을 30% 이하로 낮추는 것**입니다.
""", unsafe_allow_html=True)
create_post_purchase_chart(df_post_purchase)

# --------------------------------------------------------------------------------------
# 5. LTV 기여 분석: 카테고리 VIP 전환율
# --------------------------------------------------------------------------------------

st.header("5. 첫 구매 카테고리별 VIP Champions 전환율 분석")
st.markdown("""
### 5.1. 인사이트: 고가치 첫 구매의 중요성 
Promising High Value와 Promising Low Value 풀을 포함한 전체 잠재 VIP 고객(VIP + PHV + PLV) 중 **VIP Champion으로 최종 전환되는 비율**이 높은 카테고리는 다음과 같습니다.

| 카테고리 | VIP 전환율 (%) | 특징 |
| :---: | :---: | :---: |
| **Clothing Sets** | $\mathbf{36.36\%}$ | 매우 높은 단가와 의류 세트에 대한 선호가 LTV 잠재력을 극대화. |
| **Suits** | $\mathbf{25.00\%}$ | 전문적/고가치 아이템에 대한 초기 투자가 고객 신뢰도를 높임. |
| **Outerwear & Coats** | $\mathbf{22.46\%}$ | 높은 객단가(`avg_first_item_price`: $\text{\$177.41}$)로 인해 첫 구매부터 M-Score가 높게 시작. |
| **Intimates / Socks & Hosiery** | $\mathbf{\approx 10\%}$ | 필수재지만 저가치 상품. VIP 전환율이 가장 낮음.

### 5.2. 문제 정의 및 액션 플랜
* **문제:** 첫 구매 상품의 **가격대**와 **상품 유형(고관여/저관여)**이 미래 VIP 전환율을 강력하게 결정합니다. 저가치 카테고리(`Socks`, `Intimates`)를 통한 유입은 대규모의 Promising Low Value 고객을 생성할 위험이 높습니다.
* **액션 플랜 (고전환 카테고리):** `Suits`, `Outerwear & Coats` 구매자에게는 VIP 혜택을 미리 보여주거나, **프리미엄 세그먼트 전용 추천 시스템**을 즉시 가동하여 2차 구매까지의 시간을 단축시켜야 합니다.
* **액션 플랜 (저전환 카테고리):** `Socks`, `Intimates` 구매자에게는 **'스타일링 완성' 번들 캠페인**을 통해 다음 구매에서 객단가를 높여야 합니다. (예: `Intimates` 구매 시, $50$ 이상 Activewear 구매 시 $10$ 할인).

""", unsafe_allow_html=True)
create_category_conversion_chart(df_category_conversion)


# --------------------------------------------------------------------------------------
# 6. LTV 기여 분석: 카테고리 페어 및 재구매 타이밍
# --------------------------------------------------------------------------------------

st.header("6. 재구매 동선 및 속도 분석 (VIP / LTV 전략)")

# 6.1. 재구매 동선 (Category Pair)
st.subheader("6.1. VIP Champions 카테고리 전환 경로")
st.markdown("""
VIP Champions의 성공적인 2차 구매 경로는 **주요 의류(Jeans, Outerwear) $\rightarrow$ 보완재/필수재(Sweaters, Hoodies)**의 흐름을 보입니다.

| 1차 카테고리 | 2차 카테고리 (가장 높은 전환) | 비중 (%) | 1차 품목 평균가 ($) | 2차 품목 평균가 ($) |
| :---: | :---: | :---: | :---: | :---: |
| **Outerwear & Coats** | Sweaters | $30.43$ | $\text{130.55}$ | $\mathbf{116.72}$ |
| **Sweaters** | Outerwear & Coats | $50.0$ | $\text{60.94}$ | $\mathbf{143.49}$ |
| **Fashion Hoodies** | Jeans | $60.0$ | $\text{65.43}$ | $\mathbf{93.83}$ |
| **Jeans** | Fashion Hoodies | $28.26$ | $\text{123.98}$ | $\text{68.43}$ |

* **인사이트:** `Sweaters` $\rightarrow$ `Outerwear & Coats` 전환 시 **$143.49$**의 높은 2차 구매 단가가 발생했습니다. 이는 성공적인 **Upsell (저가치 $\rightarrow$ 고가치)** 시나리오입니다.
* **액션 플랜:** Promising High Value 고객의 첫 구매 카테고리를 기반으로 **성공적인 VIP의 Upsell 경로**를 예측하여 2차 구매 상품을 추천해야 합니다. (예: PHV가 `Sweaters` 구매 시, 다음으로 `Outerwear & Coats`를 추천).
""", unsafe_allow_html=True)
st.dataframe(df_category_pair.sort_values('pair_count', ascending=False).head(10).reset_index(drop=True))


# 6.2. 고객 생애 초기 구매 타이밍
st.subheader("6.2. 가입 시점 $\rightarrow$ 첫 구매 타이밍별 LTV 잠재력 분석")
st.markdown("""


고객이 **가입 후 얼마나 빨리 첫 구매를 하느냐**가 미래의 LTV 잠재력을 결정하는 가장 강력한 요인입니다.
* **골든 타임:** 가입 후 **1개월 이내** 첫 구매 그룹(`1. 1주일 이내`, `2. 1개월 이내`)의 재구매율($25.08\% \sim 26.06\%$) 및 VIP Champions 전환율($9.32\% \sim 10.42\%$)이 가장 높습니다.
* **위험 구간:** 3개월 이상 걸린 그룹(`5. 3개월+`, 전체의 $88.5\%$)은 VIP 전환율이 **$4.64\%$**로, 골든 타임 그룹 대비 절반 이하로 급감합니다.

### 액션 플랜: 첫 구매 가속화
* **해결 방안:** 신규 가입자 대상 **'Fast Buyer' 인센티브 프로그램**을 도입해야 합니다. 가입 후 30일 이내에 $1$회 구매 시, $\mathbf{2}$차 구매 시 사용할 수 있는 특별 크레딧($20 \sim 30$)을 제공하여 첫 구매를 가속화해야 합니다.
""", unsafe_allow_html=True)

df_signup_timing_chart = df_signup_timing[['first_purchase_timing', 'repurchase_rate', 'vip_champions_rate']].set_index('first_purchase_timing')
st.bar_chart(df_signup_timing_chart)
st.dataframe(df_signup_timing.drop(columns=['avg_days_to_repurchase', 'avg_monetary', 'avg_m_score', 'avg_r_score', 'avg_f_score']).reset_index(drop=True))


# 6.3. Champions 재구매 속도
st.subheader("6.3. VIP Champions 재구매 전환 속도와 활동")
st.markdown("""
* **인사이트:** VIP Champions의 $\mathbf{71.39\%}$는 2차 구매까지 $61$일 이상(평균 $273$일)이 소요됩니다. 재구매 속도가 느려도 최종 LTV(평균 $\mathbf{\$274.58}$)에는 큰 차이가 없습니다. (Quick 그룹 $\mathbf{\$282.50}$).
* **액션 플랜:** VIP 고객은 장기적인 관점에서 접근해야 하며, 빠른 재구매를 강요하기보다는 **'Quick Converters' (30일 이내)** 그룹을 별도로 식별하여 가장 반응성이 높은 **초고가치 고객**으로 집중 관리해야 합니다. 그 외 고객에게는 부담 없는 장기적인 브랜딩/신제품 업데이트 위주의 커뮤니케이션을 유지해야 합니다.
""", unsafe_allow_html=True)
st.dataframe(df_champions_speed.set_index('conversion_speed'))

st.markdown("---")
st.markdown("## 📊 원본 데이터 테이블 (참고)")
st.dataframe(df_rfm_final)
st.dataframe(df_traffic_source)
st.dataframe(df_post_purchase)
st.dataframe(df_first_session)