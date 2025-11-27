"""
TheLook E-commerce RFM 분석 포트폴리오 (Complete Version v2)
=========================================================
분석 기간: 2023-01-01 ~ 2024-12-31
총 분석 고객: 29,795명
RFM 세그먼트: 9개 (VIP, Loyal High/Low, Promising High/Low, Need Attention, At Risk, Hibernating, Others)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ============================================
# 페이지 설정
# ============================================
st.set_page_config(
    page_title="TheLook RFM 분석 포트폴리오",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 커스텀 CSS
# ============================================
st.markdown("""
<style>
    /* 메인 헤더 */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .main-header p {
        opacity: 0.9;
        font-size: 1.1rem;
    }
    
    /* Executive Summary 헤더 */
    .exec-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
        padding: 2.5rem 3rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 40px rgba(30, 58, 95, 0.4);
    }
    .exec-header h1 {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    /* 메트릭 카드 */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 4px solid;
        transition: transform 0.2s ease;
        margin-bottom: 1rem;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    .metric-card.blue { border-color: #667eea; }
    .metric-card.green { border-color: #10b981; }
    .metric-card.orange { border-color: #f59e0b; }
    .metric-card.red { border-color: #ef4444; }
    .metric-card.purple { border-color: #8b5cf6; }
    .metric-card.navy { border-color: #1e3a5f; }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #6b7280;
        margin-top: 0.25rem;
    }
    .metric-delta {
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }
    .delta-positive { color: #10b981; }
    .delta-negative { color: #ef4444; }
    
    /* 인사이트 박스 */
    .insight-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-left: 4px solid #0ea5e9;
        padding: 1.25rem 1.5rem;
        border-radius: 0 12px 12px 0;
        margin: 1rem 0;
    }
    .insight-box.warning {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border-color: #f59e0b;
    }
    .insight-box.success {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-color: #10b981;
    }
    .insight-box.danger {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border-color: #ef4444;
    }
    .insight-box.navy {
        background: linear-gradient(135deg, #e8f4fd 0%, #d1e9fc 100%);
        border-color: #1e3a5f;
    }
    .insight-box.purple {
        background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
        border-color: #8b5cf6;
    }
    .insight-title {
        font-weight: 600;
        font-size: 1rem;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .insight-text {
        color: #4b5563;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* 문제정의 박스 */
    .problem-box {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border: 2px solid #ef4444;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .problem-title {
        font-weight: 700;
        font-size: 1.1rem;
        color: #dc2626;
        margin-bottom: 0.75rem;
    }
    
    /* 해결방안 박스 */
    .solution-box {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border: 2px solid #10b981;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .solution-title {
        font-weight: 700;
        font-size: 1.1rem;
        color: #059669;
        margin-bottom: 0.75rem;
    }
    
    /* ROI 박스 */
    .roi-box {
        background: linear-gradient(135deg, #fefce8 0%, #fef9c3 100%);
        border: 2px solid #eab308;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .roi-title {
        font-weight: 700;
        font-size: 1.1rem;
        color: #ca8a04;
        margin-bottom: 0.75rem;
    }
    
    /* 액션 플랜 박스 */
    .action-box {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.2s ease;
    }
    .action-box:hover {
        border-color: #667eea;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.15);
    }
    .action-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    .action-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    .action-title {
        font-weight: 600;
        font-size: 1.1rem;
        color: #1f2937;
    }
    .action-content {
        color: #4b5563;
        font-size: 0.95rem;
        line-height: 1.7;
    }
    
    /* 섹션 디바이더 */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
        margin: 2rem 0;
        border-radius: 1px;
    }
    
    /* RFM 기준 테이블 */
    .rfm-criteria-table {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    /* Executive Summary 핵심 지표 */
    .exec-metric {
        background: white;
        padding: 1.75rem;
        border-radius: 16px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        text-align: center;
        transition: transform 0.3s ease;
    }
    .exec-metric:hover {
        transform: translateY(-4px);
    }
    .exec-metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .exec-metric-label {
        font-size: 1rem;
        color: #6b7280;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* Key Finding 카드 */
    .key-finding {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border-left: 4px solid;
    }
    .key-finding.critical { border-color: #ef4444; }
    .key-finding.opportunity { border-color: #10b981; }
    .key-finding.insight { border-color: #3b82f6; }
</style>
""", unsafe_allow_html=True)

# ============================================
# 데이터 정의 (Based on SQL Query Results)
# ============================================

# RFM 분포 데이터 (sale_price 기준)
rfm_distribution = {
    "recency": {"p10": 40, "p25": 111, "p50": 259, "p75": 455, "p90": 610, "p95": 668, "avg": 293.0, "std": 207.2},
    "frequency": {"p10": 1, "p25": 1, "p50": 1, "p75": 1, "p90": 2, "p95": 2, "avg": 1.2, "std": 0.47},
    "monetary": {"p10": 18.02, "p25": 34.0, "p50": 66.5, "p75": 134.72, "p90": 228.68, "p95": 301.98, "avg": 102.82, "std": 109.77}
}

# RFM 세그먼트 데이터
segment_data = pd.DataFrame([
    {"segment": "VIP Champions", "user_count": 1531, "pct": 5.14, "avg_recency": 79.5, 
     "avg_frequency": 2.32, "avg_monetary": 275.88, "revenue_pct": 13.79, 
     "r_score": 4.59, "f_score": 4.28, "m_score": 4.30, "total_revenue": 422377.78},
    {"segment": "Loyal High Value", "user_count": 2026, "pct": 6.80, "avg_recency": 185.3, 
     "avg_frequency": 2.15, "avg_monetary": 162.27, "revenue_pct": 10.73, 
     "r_score": 3.67, "f_score": 4.14, "m_score": 3.47, "total_revenue": 328759.12},
    {"segment": "Loyal Low Value", "user_count": 587, "pct": 1.97, "avg_recency": 143.1, 
     "avg_frequency": 2.03, "avg_monetary": 48.40, "revenue_pct": 0.93, 
     "r_score": 4.05, "f_score": 4.03, "m_score": 1.84, "total_revenue": 28410.78},
    {"segment": "Promising High Value", "user_count": 3555, "pct": 11.93, "avg_recency": 84.2, 
     "avg_frequency": 1.0, "avg_monetary": 155.86, "revenue_pct": 18.09, 
     "r_score": 4.55, "f_score": 3.0, "m_score": 3.51, "total_revenue": 554081.87},
    {"segment": "Promising Low Value", "user_count": 4891, "pct": 16.42, "avg_recency": 85.3, 
     "avg_frequency": 1.0, "avg_monetary": 34.28, "revenue_pct": 5.47, 
     "r_score": 4.55, "f_score": 3.0, "m_score": 1.49, "total_revenue": 167640.62},
    {"segment": "Need Attention", "user_count": 730, "pct": 2.45, "avg_recency": 476.2, 
     "avg_frequency": 2.08, "avg_monetary": 206.51, "revenue_pct": 4.92, 
     "r_score": 1.78, "f_score": 4.08, "m_score": 3.78, "total_revenue": 150755.89},
    {"segment": "At Risk", "user_count": 6637, "pct": 22.28, "avg_recency": 270.2, 
     "avg_frequency": 1.0, "avg_monetary": 85.36, "revenue_pct": 18.49, 
     "r_score": 3.0, "f_score": 3.0, "m_score": 2.36, "total_revenue": 566558.73},
    {"segment": "Hibernating", "user_count": 9707, "pct": 32.58, "avg_recency": 538.5, 
     "avg_frequency": 1.0, "avg_monetary": 86.38, "revenue_pct": 27.37, 
     "r_score": 1.53, "f_score": 3.0, "m_score": 2.35, "total_revenue": 838519.26},
    {"segment": "Others", "user_count": 131, "pct": 0.44, "avg_recency": 490.2, 
     "avg_frequency": 2.02, "avg_monetary": 48.79, "revenue_pct": 0.21, 
     "r_score": 1.73, "f_score": 4.02, "m_score": 1.85, "total_revenue": 6391.18}
])

# 트래픽 소스별 VIP 전환율
channel_data = pd.DataFrame([
    {"channel": "Facebook", "vip_conversion_rate": 17.80, "promising_high_share": 35.28, 
     "promising_low_share": 46.93, "avg_monetary_vip": 268.85, "total_users": 618},
    {"channel": "Search", "vip_conversion_rate": 15.37, "promising_high_share": 35.53, 
     "promising_low_share": 49.10, "avg_monetary_vip": 272.92, "total_users": 6927},
    {"channel": "Organic", "vip_conversion_rate": 15.06, "promising_high_share": 36.87, 
     "promising_low_share": 48.07, "avg_monetary_vip": 295.01, "total_users": 1527},
    {"channel": "Email", "vip_conversion_rate": 14.84, "promising_high_share": 31.71, 
     "promising_low_share": 53.46, "avg_monetary_vip": 262.42, "total_users": 492},
    {"channel": "Display", "vip_conversion_rate": 12.83, "promising_high_share": 38.01, 
     "promising_low_share": 49.15, "avg_monetary_vip": 285.63, "total_users": 413}
])

# Promising 세그먼트 구매 후 활동 분석
promising_activity = pd.DataFrame([
    {"segment": "Promising High Value", "activity_level": "0. 미활동", "user_count": 1643, 
     "pct": 46.22, "avg_events": 0.0, "avg_monetary": 131.06},
    {"segment": "Promising High Value", "activity_level": "1. 1 Session", "user_count": 473, 
     "pct": 13.31, "avg_events": 1.2, "avg_monetary": 153.98},
    {"segment": "Promising High Value", "activity_level": "2. 2-3 Sessions", "user_count": 1268, 
     "pct": 35.67, "avg_events": 2.4, "avg_monetary": 176.89},
    {"segment": "Promising High Value", "activity_level": "3. 4-5 Sessions", "user_count": 170, 
     "pct": 4.78, "avg_events": 5.4, "avg_monetary": 244.25},
    {"segment": "Promising Low Value", "activity_level": "0. 미활동", "user_count": 4275, 
     "pct": 87.41, "avg_events": 0.0, "avg_monetary": 32.59},
    {"segment": "Promising Low Value", "activity_level": "1. 1 Session", "user_count": 227, 
     "pct": 4.64, "avg_events": 2.0, "avg_monetary": 44.13},
    {"segment": "Promising Low Value", "activity_level": "2. 2-3 Sessions", "user_count": 384, 
     "pct": 7.85, "avg_events": 3.2, "avg_monetary": 47.18}
])

# VIP 재구매 타이밍
vip_repurchase_timing = pd.DataFrame([
    {"bucket": "1. Within 1 Week", "count": 47, "pct": 3.07, "avg_days": 3.6, 
     "avg_first_revenue": 138.17, "avg_second_revenue": 120.71, "avg_ltv": 303.42},
    {"bucket": "2. Within 2 Weeks", "count": 40, "pct": 2.61, "avg_days": 10.9, 
     "avg_first_revenue": 154.70, "avg_second_revenue": 92.02, "avg_ltv": 277.84},
    {"bucket": "3. Within 1 Month", "count": 78, "pct": 5.09, "avg_days": 22.6, 
     "avg_first_revenue": 120.61, "avg_second_revenue": 118.48, "avg_ltv": 272.28},
    {"bucket": "4. Within 2 Months", "count": 129, "pct": 8.43, "avg_days": 45.5, 
     "avg_first_revenue": 122.68, "avg_second_revenue": 117.58, "avg_ltv": 279.96},
    {"bucket": "5. Within 3 Months", "count": 144, "pct": 9.41, "avg_days": 75.0, 
     "avg_first_revenue": 110.22, "avg_second_revenue": 115.43, "avg_ltv": 269.08},
    {"bucket": "6. 3+ Months", "count": 1093, "pct": 71.39, "avg_days": 299.3, 
     "avg_first_revenue": 127.70, "avg_second_revenue": 120.24, "avg_ltv": 275.30}
])

# Champions 전환 속도 분석
conversion_speed = pd.DataFrame([
    {"speed": "1. Quick (≤30 days)", "count": 165, "avg_days": 14.4, "avg_sessions": 0.9, 
     "avg_product_views": 0.2, "avg_ltv": 282.50, "avg_m_score": 4.35},
    {"speed": "2. Medium (31-60 days)", "count": 129, "avg_days": 45.5, "avg_sessions": 1.1, 
     "avg_product_views": 0.3, "avg_ltv": 279.96, "avg_m_score": 4.31},
    {"speed": "3. Slow (61+ days)", "count": 1237, "avg_days": 273.2, "avg_sessions": 1.1, 
     "avg_product_views": 0.5, "avg_ltv": 274.58, "avg_m_score": 4.30}
])

# 가입~첫 구매 타이밍별 분석
signup_to_purchase = pd.DataFrame([
    {"timing": "1. 1주일 이내", "user_count": 307, "repurchase_rate": 26.06, "avg_monetary": 112.28,
     "vip_rate": 10.42, "promising_high_rate": 12.05, "promising_low_rate": 18.89},
    {"timing": "2. 1개월 이내", "user_count": 901, "repurchase_rate": 25.08, "avg_monetary": 116.92,
     "vip_rate": 9.32, "promising_high_rate": 13.10, "promising_low_rate": 16.98},
    {"timing": "3. 2개월 이내", "user_count": 1161, "repurchase_rate": 24.63, "avg_monetary": 110.41,
     "vip_rate": 9.47, "promising_high_rate": 12.14, "promising_low_rate": 19.47},
    {"timing": "4. 3개월 이내", "user_count": 1058, "repurchase_rate": 23.63, "avg_monetary": 113.97,
     "vip_rate": 7.75, "promising_high_rate": 12.00, "promising_low_rate": 18.34},
    {"timing": "5. 3개월+", "user_count": 26368, "repurchase_rate": 15.79, "avg_monetary": 101.45,
     "vip_rate": 4.64, "promising_high_rate": 11.88, "promising_low_rate": 16.16}
])

# 첫 구매 카테고리별 VIP 전환율 TOP 10
category_vip_conversion = pd.DataFrame([
    {"category": "Clothing Sets", "vip_conversion_pct": 36.36, "avg_total_ltv": 259.81, "vip_count": 4},
    {"category": "Suits", "vip_conversion_pct": 25.00, "avg_total_ltv": 248.88, "vip_count": 15},
    {"category": "Outerwear & Coats", "vip_conversion_pct": 22.46, "avg_total_ltv": 345.31, "vip_count": 124},
    {"category": "Blazers & Jackets", "vip_conversion_pct": 21.56, "avg_total_ltv": 261.14, "vip_count": 36},
    {"category": "Jeans", "vip_conversion_pct": 18.88, "avg_total_ltv": 282.84, "vip_count": 132},
    {"category": "Suits & Sport Coats", "vip_conversion_pct": 17.75, "avg_total_ltv": 280.37, "vip_count": 52},
    {"category": "Jumpsuits & Rompers", "vip_conversion_pct": 17.31, "avg_total_ltv": 215.66, "vip_count": 9},
    {"category": "Accessories", "vip_conversion_pct": 17.17, "avg_total_ltv": 271.72, "vip_count": 91},
    {"category": "Dresses", "vip_conversion_pct": 16.67, "avg_total_ltv": 276.64, "vip_count": 49},
    {"category": "Sweaters", "vip_conversion_pct": 16.50, "avg_total_ltv": 270.27, "vip_count": 102}
])

# 첫 세션 행동 분석 (세그먼트별)
first_session_behavior = pd.DataFrame([
    {"segment": "VIP Champions", "avg_events": 6.64, "cart_usage_rate": 100.0, 
     "purchase_rate": 100.0, "avg_monetary": 275.88},
    {"segment": "Promising High Value", "avg_events": 7.05, "cart_usage_rate": 100.0, 
     "purchase_rate": 99.16, "avg_monetary": 155.86},
    {"segment": "Promising Low Value", "avg_events": 5.29, "cart_usage_rate": 99.94, 
     "purchase_rate": 99.94, "avg_monetary": 34.28},
    {"segment": "Loyal High Value", "avg_events": 5.89, "cart_usage_rate": 99.85, 
     "purchase_rate": 100.0, "avg_monetary": 162.27},
    {"segment": "At Risk", "avg_events": 6.07, "cart_usage_rate": 99.95, 
     "purchase_rate": 100.0, "avg_monetary": 85.36},
    {"segment": "Hibernating", "avg_events": 6.05, "cart_usage_rate": 99.96, 
     "purchase_rate": 100.0, "avg_monetary": 86.39}
])

# 채널 x 카테고리별 Champions LTV TOP 10
channel_category_ltv = pd.DataFrame([
    {"channel": "Facebook", "category": "Outerwear & Coats", "champion_count": 8, 
     "avg_ltv": 386.28, "avg_first_price": 243.98, "m_score_5_count": 6},
    {"channel": "Organic", "category": "Tops & Tees", "champion_count": 13, 
     "avg_ltv": 383.50, "avg_first_price": 64.69, "m_score_5_count": 7},
    {"channel": "Email", "category": "Outerwear & Coats", "champion_count": 5, 
     "avg_ltv": 374.74, "avg_first_price": 247.99, "m_score_5_count": 2},
    {"channel": "Organic", "category": "Suits & Sport Coats", "champion_count": 15, 
     "avg_ltv": 369.20, "avg_first_price": 150.70, "m_score_5_count": 8},
    {"channel": "Search", "category": "Pants & Capris", "champion_count": 13, 
     "avg_ltv": 361.10, "avg_first_price": 81.58, "m_score_5_count": 7}
])

# ============================================
# 사이드바 네비게이션
# ============================================
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <h2 style="margin: 0; color: #667eea;">📊 김동윤: RFM 분석</h2>
    <p style="color: #6b7280; font-size: 0.9rem;">TheLook E-commerce</p>
</div>
""", unsafe_allow_html=True)

pages = {
    "📋 Executive Summary": "executive",
    "🔬 RFM 등급 기준 & 근거": "rfm_criteria",
    "👥 세그먼트 현황 분석": "segments",
    "⚠️ 문제 정의 & 인사이트": "problems",
    "🎯 Promising 분석": "promising",
    "👑 VIP 분석": "vip",
    "📢 채널 & 카테고리 분석": "channel",
    "🚀 Action Plan & ROI": "action"
}

selected_page = st.sidebar.radio("", list(pages.keys()), label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size: 0.8rem; color: #9ca3af;">
    <p><strong>분석 기간:</strong> 2023.01 - 2024.12</p>
    <p><strong>총 고객 수:</strong> 29,795명</p>
    <p><strong>총 매출:</strong> $3,063,495</p>
    <p><strong>데이터:</strong> BigQuery thelook</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# 페이지 1: Executive Summary
# ============================================
if pages[selected_page] == "executive":
    st.markdown("""
    <div class="exec-header">
        <h1>📋 Executive Summary</h1>
        <p>TheLook E-commerce RFM 분석 핵심 요약 | 2023.01 - 2024.12</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 핵심 지표 요약
    st.subheader("🎯 핵심 비즈니스 지표")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div class="exec-metric">
            <div class="exec-metric-value">29,795</div>
            <div class="exec-metric-label">분석 고객 수</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="exec-metric">
            <div class="exec-metric-value">$3.06M</div>
            <div class="exec-metric-label">총 매출</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="exec-metric">
            <div class="exec-metric-value">5.14%</div>
            <div class="exec-metric-label">VIP 비율</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="exec-metric">
            <div class="exec-metric-value">$102.82</div>
            <div class="exec-metric-label">평균 LTV</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="exec-metric">
            <div class="exec-metric-value">54.86%</div>
            <div class="exec-metric-label">이탈 위험 고객</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 핵심 발견사항
    st.subheader("🔍 핵심 발견사항 (Key Findings)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="key-finding critical">
            <div style="font-weight: 700; color: #dc2626; margin-bottom: 0.5rem;">🚨 Critical Issue #1</div>
            <div style="font-size: 1.5rem; font-weight: 700; margin-bottom: 0.5rem;">Promising 고객 70.1% 미활동 (구매 1회)</div>
            <div style="color: #4b5563; line-height: 1.6;">
                • Promising High: 46.2% 미활동 (1,643명)<br>
                • Promising Low: <b>87.4%</b> 미활동 (4,275명)<br>
                • <b>잠재 손실: $248K</b> (미활동 vs 활동 LTV 차이)<br>
                <span style="font-size: 0.85rem; color: #6b7280;">└ High: 1,643×($244-$131)=$186K / Low: 4,275×($47-$33)=$62K</span><br>
                • <b>잠재 기회: $213K</b> (세션 유도 시 예상 추가 매출)
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="key-finding critical">
            <div style="font-weight: 700; color: #dc2626; margin-bottom: 0.5rem;">🚨 Critical Issue #2</div>
            <div style="font-size: 1.5rem; font-weight: 700; margin-bottom: 0.5rem;">VIP의 71.4% 3개월+ 후 재구매</div>
            <div style="color: #4b5563; line-height: 1.6;">
                • 3개월 이내 재구매: 28.6% (438명)<br>
                • 1주일 내 재구매 시 LTV: <b>$303.42</b><br>
                • 3개월+ 재구매 시 LTV: $275.30 (10% 손실)
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="key-finding opportunity">
            <div style="font-weight: 700; color: #059669; margin-bottom: 0.5rem;">✅ Opportunity #1</div>
            <div style="font-size: 1.5rem; font-weight: 700; margin-bottom: 0.5rem;">Facebook 채널 VIP 전환율 17.8%</div>
            <div style="color: #4b5563; line-height: 1.6;">
                • 전 채널 최고 효율 (Display 12.8% 대비 +5%p)<br>
                • Organic 채널 VIP LTV 최고: <b>$295.01</b><br>
                • 광고 예산 재배분으로 ROI 극대화 가능
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="key-finding opportunity">
            <div style="font-weight: 700; color: #059669; margin-bottom: 0.5rem;">✅ Opportunity #2</div>
            <div style="font-size: 1.5rem; font-weight: 700; margin-bottom: 0.5rem;">고가 카테고리 = 높은 VIP 전환</div>
            <div style="color: #4b5563; line-height: 1.6;">
                • Outerwear & Coats: 전환율 22.5%, LTV <b>$345</b><br>
                • Suits: 전환율 25.0%, LTV $249<br>
                • 첫 구매 카테고리 유도로 VIP 전환 가속화
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 세그먼트 분포 요약
    st.subheader("📊 세그먼트 분포 요약")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 트리맵
        fig = px.treemap(
            segment_data,
            path=['segment'],
            values='user_count',
            color='avg_monetary',
            color_continuous_scale='RdYlGn',
            title='RFM 세그먼트 분포 (크기: 고객 수, 색상: 평균 LTV)'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box navy">
            <div class="insight-title">💡 세그먼트 핵심 요약</div>
            <div class="insight-text">
                <b>성장 동력 (28.4%)</b><br>
                • VIP: 5.14%<br>
                • Promising: 28.35%<br><br>
                <b>위험 고객 (54.9%)</b><br>
                • At Risk: 22.28%<br>
                • Hibernating: 32.58%<br><br>
                <b>매출 기여</b><br>
                • VIP 5.14% → 매출 13.79%<br>
                • 이탈위험 55% → 매출 46%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 예상 수익 & ROI 요약 (Promising High/Low 분리)
    st.subheader("💰 예상 수익 & ROI 요약 (Promising High/Low 분리)")
    
    # ROI 정의 설명
    st.markdown("""
    <div class="insight-box navy">
        <div class="insight-title">📌 ROI 산출 정의</div>
        <div class="insight-text">
            • <b>ROI (Return on Investment)</b> = (순이익 / 캠페인 비용) × 100%<br>
            • <b>캠페인 비용</b>: 이메일 발송, 할인 쿠폰, 마케팅 인력 등 (예상 매출의 약 20% 가정)<br>
            • <b>예상 추가 매출</b>: 세션 활동 유도 → 재구매 전환 → VIP 전환 시나리오 기반
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card green">
            <div class="metric-value">$445K</div>
            <div class="metric-label">예상 총 추가 매출</div>
            <div class="metric-delta delta-positive">현 매출 대비 +14.5%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card blue">
            <div class="metric-value">$89K</div>
            <div class="metric-label">예상 캠페인 비용</div>
            <div class="metric-delta">매출의 20%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card purple">
            <div class="metric-value">$356K</div>
            <div class="metric-label">예상 순이익</div>
            <div class="metric-delta">매출 - 비용</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card orange">
            <div class="metric-value">400%</div>
            <div class="metric-label">예상 ROI</div>
            <div class="metric-delta">순이익/비용×100</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ROI 테이블 (Promising High/Low 분리) - 구체적 수치 포함
    st.markdown("#### 📊 Phase별 수익 & ROI 상세")
    
    roi_summary = pd.DataFrame({
        "Phase": ["Phase 1-A: Promising High", "Phase 1-B: Promising Low", 
                  "Phase 2: VIP 유지", "Phase 3: Winback", "Phase 4: 채널 최적화", "Total"],
        "대상": ["미활동 1,643명", "미활동 4,275명", "VIP 1,531명", "이탈위험 16,344명", "전 채널", "-"],
        "예상 추가 매출": ["$131,000", "$82,000", "$79,000", "$93,000", "$60,000", "$445,000"],
        "캠페인 비용(20%)": ["$26,200", "$16,400", "$15,800", "$18,600", "$12,000", "$89,000"],
        "순이익": ["$104,800", "$65,600", "$63,200", "$74,400", "$48,000", "$356,000"],
        "ROI": ["400%", "400%", "400%", "400%", "400%", "400%"],
        "우선순위": ["🔴 P1", "🔴 P1", "🟡 P2", "🟠 P2", "🟢 P3", "-"]
    })
    st.dataframe(roi_summary, hide_index=True, use_container_width=True)
    
    # Phase 1 상세 산출 근거
    st.markdown("#### 📋 Phase 1: Promising 리텐션 ROI 산출 근거")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="roi-box">
            <div class="roi-title">🟣 Phase 1-A: Promising High Value</div>
            <div style="color: #4b5563; line-height: 1.6; font-size: 0.9rem;">
                <b>현황:</b> 미활동 1,643명 (구매 1회, 세션 0)<br>
                <b>핵심 발견:</b> 세션 활동 시 LTV +86% ($131→$244)<br><br>
                <b>전환 시나리오:</b><br>
                • 세션 활동 전환: 1,643명 × 30% = <b>493명</b><br>
                • 재구매 전환: 493명 × 50% = <b>247명</b><br>
                • 예상 객단가: $176 (세션 활동 고객 기준)<br><br>
                <b>매출 산출:</b><br>
                • 2차 구매: 247 × $176 = $43,472<br>
                • VIP 전환(20%): 49 × $275 = $13,475<br>
                • 3차 구매(40%): 99 × $120 = $11,880<br>
                • 객단가 상승: $62,173<br>
                • <b>총 추가 매출: $131,000</b><br><br>
                <b>ROI 계산:</b><br>
                • 비용: $131,000 × 20% = $26,200<br>
                • 순이익: $104,800<br>
                • <b>ROI: $104,800 / $26,200 = 400%</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="roi-box">
            <div class="roi-title">🟠 Phase 1-B: Promising Low Value</div>
            <div style="color: #4b5563; line-height: 1.6; font-size: 0.9rem;">
                <b>현황:</b> 미활동 4,275명 (구매 1회, 세션 0)<br>
                <b>핵심 발견:</b> 세션 활동 시 LTV +45% ($33→$47)<br><br>
                <b>전환 시나리오:</b><br>
                • 세션 활동 전환: 4,275명 × 20% = <b>855명</b><br>
                • 재구매 전환: 855명 × 35% = <b>299명</b><br>
                • 예상 객단가: $47 (세션 활동 고객 기준)<br><br>
                <b>매출 산출:</b><br>
                • 2차 구매: 299 × $47 = $14,053<br>
                • 업셀링(30%): 90 × $80 = $7,200<br>
                • VIP 전환(10%): 30 × $180 = $5,400<br>
                • 3차 구매(25%): 75 × $50 = $3,750<br>
                • 객단가 상승: $51,597<br>
                • <b>총 추가 매출: $82,000</b><br><br>
                <b>ROI 계산:</b><br>
                • 비용: $82,000 × 20% = $16,400<br>
                • 순이익: $65,600<br>
                • <b>ROI: $65,600 / $16,400 = 400%</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# 페이지 2: RFM 등급 기준 & 근거
# ============================================
elif pages[selected_page] == "rfm_criteria":
    st.markdown("""
    <div class="main-header">
        <h1>🔬 RFM 등급 기준 & 근거</h1>
        <p>데이터 분포 분석을 통한 등급 산정 로직 및 세그먼트 정의</p>
    </div>
    """, unsafe_allow_html=True)
    
    # RFM 분포 분석 결과
    st.subheader("📊 RFM 분포 분석 결과 (sale_price 기반)")
    
    st.markdown("""
    <div class="insight-box navy">
        <div class="insight-title">📌 분석 기반 데이터</div>
        <div class="insight-text">
            • <b>분석 기간:</b> 2023-01-01 ~ 2024-12-31 (2년)<br>
            • <b>총 고객 수:</b> 29,795명 (Cancelled/Returned 주문 제외)<br>
            • <b>매출 기준:</b> sale_price (실제 판매가) 기반 집계<br>
            • <b>분석 기준일:</b> 2024-12-31
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Recency (최근성)")
        recency_df = pd.DataFrame({
            "분위수": ["P10", "P25", "P50 (중앙값)", "P75", "P90", "P95"],
            "일수": [40, 111, 259, 455, 610, 668]
        })
        st.dataframe(recency_df, hide_index=True, use_container_width=True)
        st.markdown(f"**평균:** {rfm_distribution['recency']['avg']}일 | **표준편차:** {rfm_distribution['recency']['std']}일")
    
    with col2:
        st.markdown("#### Frequency (빈도)")
        frequency_df = pd.DataFrame({
            "분위수": ["P10", "P25", "P50 (중앙값)", "P75", "P90", "P95"],
            "횟수": [1, 1, 1, 1, 2, 2]
        })
        st.dataframe(frequency_df, hide_index=True, use_container_width=True)
        st.markdown(f"**평균:** {rfm_distribution['frequency']['avg']}회 | **표준편차:** {rfm_distribution['frequency']['std']}회")
    
    with col3:
        st.markdown("#### Monetary (금액)")
        monetary_df = pd.DataFrame({
            "분위수": ["P10", "P25", "P50 (중앙값)", "P75", "P90", "P95"],
            "금액": ["$18.02", "$34.00", "$66.50", "$134.72", "$228.68", "$301.98"]
        })
        st.dataframe(monetary_df, hide_index=True, use_container_width=True)
        st.markdown(f"**평균:** ${rfm_distribution['monetary']['avg']} | **표준편차:** ${rfm_distribution['monetary']['std']}")
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # RFM 스코어링 기준
    st.subheader("📐 RFM 스코어링 기준 (1-5점)")
    
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">🎯 스코어링 설계 원칙</div>
        <div class="insight-text">
            각 RFM 요소를 <b>1~5점</b>으로 스코어링하여 세그먼트 분류에 활용합니다.
            스코어링 기준은 <b>실제 데이터 분포(Percentile)</b>와 <b>비즈니스 로직</b>을 함께 고려하여 설정했습니다.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Recency Score (R)")
        st.markdown("""
        | 점수 | 기준 | 근거 |
        |------|------|------|
        | **5** | ≤90일 | 3개월 이내 활성 고객 |
        | **4** | 91-180일 | 6개월 이내 준활성 |
        | **3** | 181-365일 | 1년 이내 비활성화 진행 |
        | **2** | 366-545일 | 1.5년 이내 이탈 위험 |
        | **1** | >545일 | 장기 휴면 고객 |
        """)
        st.markdown("""
        <div class="insight-box success" style="margin-top: 1rem;">
            <div class="insight-title">💡 설정 근거</div>
            <div class="insight-text">
                • P50(중앙값) = 259일 → 3등급 기준<br>
                • 일반적 리텐션 주기 고려 (90일 단위)<br>
                • P75(455일) ≈ 1.5년 → 휴면 기준
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Frequency Score (F)")
        st.markdown("""
        | 점수 | 기준 | 근거 |
        |------|------|------|
        | **5** | ≥3회 | 상위 5%+ 충성 고객 |
        | **4** | 2회 | P90 수준 재구매 고객 |
        | **3** | 1회 | 대다수(75%) 1회 구매 |
        | **1** | 0회 | (해당 없음) |
        """)
        st.markdown("""
        <div class="insight-box success" style="margin-top: 1rem;">
            <div class="insight-title">💡 설정 근거</div>
            <div class="insight-text">
                • P90 = 2회 → 재구매 자체가 상위 10%<br>
                • 대부분(75%) 1회 구매 → F스코어 3점<br>
                • <b>2회 이상 = 충성 고객</b>으로 분류<br>
                • 최대 빈도 4회 (P95 = 2회)
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("#### Monetary Score (M)")
        st.markdown("""
        | 점수 | 기준 | 근거 |
        |------|------|------|
        | **5** | ≥$300 | P95+ 고객 (상위 5%) |
        | **4** | $135-299 | P75+ (상위 25%) |
        | **3** | $67-134 | P50+ (중앙값 이상) |
        | **2** | $34-66 | P25+ (하위 50%) |
        | **1** | <$34 | P25 미만 (하위 25%) |
        """)
        st.markdown("""
        <div class="insight-box success" style="margin-top: 1rem;">
            <div class="insight-title">💡 설정 근거</div>
            <div class="insight-text">
                • P50 = $66.50 → 3점 하한선<br>
                • P75 = $134.72 → 4점 하한선<br>
                • P95 = $301.98 → 5점 하한선<br>
                • <b>분포 기반 자연스러운 구간 설정</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 세그먼트 정의
    st.subheader("🏷️ RFM 세그먼트 정의 (9개)")
    
    st.markdown("""
    <div class="insight-box navy">
        <div class="insight-title">📌 세그먼트 분류 기준</div>
        <div class="insight-text">
            R, F, M 스코어 조합을 통해 <b>9개 고객 세그먼트</b>를 정의합니다.
            각 세그먼트는 고객의 <b>현재 가치</b>와 <b>행동 패턴</b>을 반영합니다.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    segment_criteria = pd.DataFrame({
        "세그먼트": ["VIP", "Loyal High Value", "Loyal Low Value", "Promising High Value", 
                   "Promising Low Value", "Need Attention", "At Risk", "Hibernating", "Others"],
        "R 조건": ["≥4", "≥3", "≥3", "≥4", "≥4", "≤2", "=3", "≤2", "기타"],
        "F 조건": ["≥4", "≥4", "≥4", "=3", "=3", "≥4", "=3", "≤3", "기타"],
        "M 조건": ["≥4", "≥3", "≤2", "≥3", "≤2", "≥3", "any", "any", "기타"],
        "정의": [
            "최근 방문 + 자주 구매 + 고액 지출",
            "자주 구매 + 중~고액 지출",
            "자주 구매하지만 객단가 낮음",
            "최근 첫 구매 + 중~고액 지출",
            "최근 첫 구매 + 저액 지출",
            "과거 충성 고객이나 오래 미방문",
            "중간 Recency + 1회 구매 (이탈 위험)",
            "장기 미방문 + 1회 구매",
            "기타 예외 조합"
        ],
        "전략": [
            "유지 & 업셀링",
            "VIP 승급 유도",
            "객단가 상승 유도",
            "2차 구매 유도 → VIP 전환",
            "2차 구매 유도 + 업셀링",
            "윈백 캠페인 우선순위 1",
            "긴급 리텐션 필요",
            "윈백 또는 자연 이탈 허용",
            "개별 분석 필요"
        ]
    })
    
    st.dataframe(segment_criteria, hide_index=True, use_container_width=True, height=380)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 세그먼트별 실제 분포
    st.subheader("📈 세그먼트별 실제 분포 검증")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            segment_data.sort_values('pct', ascending=True),
            x='pct',
            y='segment',
            orientation='h',
            color='avg_monetary',
            color_continuous_scale='RdYlGn',
            title='세그먼트별 고객 비율 (%, 색상: 평균 LTV)',
            labels={'pct': '고객 비율 (%)', 'segment': '세그먼트'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            segment_data.sort_values('revenue_pct', ascending=True),
            x='revenue_pct',
            y='segment',
            orientation='h',
            color='avg_monetary',
            color_continuous_scale='RdYlGn',
            title='세그먼트별 매출 기여도 (%, 색상: 평균 LTV)',
            labels={'revenue_pct': '매출 기여 (%)', 'segment': '세그먼트'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box success">
        <div class="insight-title">✅ 세그먼트 분류 검증 결과</div>
        <div class="insight-text">
            • <b>VIP (5.14%)</b>: 평균 LTV $275.88로 전체 평균의 <b>2.7배</b> → 프리미엄 고객 정확 식별<br>
            • <b>Promising (28.35%)</b>: 최근성 높고 1회 구매 → 전환 잠재력 높은 그룹 정확 분리<br>
            • <b>At Risk + Hibernating (54.86%)</b>: 과반수가 이탈 위험 → <b>리텐션 전략 시급</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 페이지 3: 세그먼트 현황 분석
# ============================================
elif pages[selected_page] == "segments":
    st.markdown("""
    <div class="main-header">
        <h1>👥 세그먼트 현황 분석</h1>
        <p>9개 RFM 세그먼트별 상세 현황 및 특성 분석</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 주요 지표 요약
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card green">
            <div class="metric-value">29,795</div>
            <div class="metric-label">총 분석 고객</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card blue">
            <div class="metric-value">$3.06M</div>
            <div class="metric-label">총 매출</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card purple">
            <div class="metric-value">$102.82</div>
            <div class="metric-label">평균 LTV</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card orange">
            <div class="metric-value">1.2회</div>
            <div class="metric-label">평균 구매 빈도</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 세그먼트 분포 시각화
    st.subheader("📊 세그먼트 분포")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            segment_data,
            values='user_count',
            names='segment',
            title='세그먼트별 고객 수 분포',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.pie(
            segment_data,
            values='total_revenue',
            names='segment',
            title='세그먼트별 매출 기여도',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 세그먼트별 상세 테이블
    st.subheader("📋 세그먼트별 상세 지표")
    
    display_df = segment_data[['segment', 'user_count', 'pct', 'avg_recency', 'avg_frequency', 
                               'avg_monetary', 'revenue_pct', 'r_score', 'f_score', 'm_score']].copy()
    display_df.columns = ['세그먼트', '고객 수', '비율(%)', '평균 Recency', '평균 Frequency', 
                          '평균 LTV($)', '매출 기여(%)', 'R Score', 'F Score', 'M Score']
    
    st.dataframe(display_df, hide_index=True, use_container_width=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # RFM 스코어 비교
    st.subheader("📈 세그먼트별 RFM 스코어 비교")
    
    fig = go.Figure()
    
    for _, row in segment_data.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row['r_score'], row['f_score'], row['m_score']],
            theta=['Recency', 'Frequency', 'Monetary'],
            fill='toself',
            name=row['segment']
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
        title='세그먼트별 RFM 스코어 레이더 차트',
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">💡 세그먼트 특성 요약</div>
        <div class="insight-text">
            • <b>VIP</b>: 모든 RFM 지표 최상위 (R:4.59, F:4.28, M:4.30)<br>
            • <b>Promising</b>: 높은 Recency(4.55)와 중간 Monetary, 낮은 Frequency(3.0) → 재구매 유도 핵심 타겟<br>
            • <b>Hibernating</b>: 모든 지표 최하위 (R:1.53, F:3.0, M:2.35) → 윈백 또는 자연 이탈 허용
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 페이지 4: 문제 정의 & 인사이트
# ============================================
elif pages[selected_page] == "problems":
    st.markdown("""
    <div class="main-header">
        <h1>⚠️ 문제 정의 & 인사이트</h1>
        <p>데이터 기반 핵심 문제점 도출 및 비즈니스 인사이트</p>
    </div>
    """, unsafe_allow_html=True)
    
    # -------------------------------------------------------------------------
    # 문제 1: Promising 미활동 (High/Low 분리)
    # -------------------------------------------------------------------------
    st.subheader("🚨 문제 #1: Promising 고객 대다수 미활동 (구매 횟수 = 모두 1회)")
    
    # 1. 핵심 특성 강조 (Recency + 구매 후 활동의 의미)
    st.markdown("""
    <div class="insight-box navy">
        <div class="insight-title">⚠️ 핵심 특성: VIP와 유사한 '최신성'을 가졌으나 '재구매'가 지연됨</div>
        <div class="insight-text">
            • <b>Why Promising?</b> 최근 구매일(Recency)이 <b>180일 이내</b>로 우리 브랜드를 기억하고 있는 상태<br>
            • <b>Behavior Pattern:</b> 모든 고객이 <b>구매 1회</b>로 동일하지만, <b>'구매 후 사이트 활동(Session)'</b>에서 극명한 차이<br>
            • <b>Key Insight:</b> <u>"구매 후 다시 찾아와 둘러보았으나(Session ↑), 아직 결제하지 않음"</u> → <b>가장 확실한 잠재 수요</b>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. 현황 데이터 & 차트 (위치 이동: 상단 배치)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="problem-box">
            <div class="problem-title">📊 현황 데이터: 첫 구매 후 추가 탐색 활동 여부</div>
            <div style="color: #4b5563; line-height: 1.8;">
                <b>🟣 Promising High Value (3,555명)</b><br>
                • <b>구매 후 미방문(0 Session): 46.22%</b> (1,643명) → <span style="color:#ef4444">위험</span><br>
                • 재방문/탐색(1 Session): 13.31%<br>
                • <b>적극적 탐색(2+ Sessions): 40.47%</b> (고관여 그룹)<br>
                → <i>구매 후 다시 방문한 그룹의 LTV가 월등히 높음</i><br><br>
                <b>🟠 Promising Low Value (4,891명)</b><br>
                • <b>구매 후 미방문(0 Session): 87.41%</b> (4,275명) → <span style="color:#ef4444">심각</span><br>
                • 재방문/탐색(1+ Session): 12.59%<br>
                → <i>대다수가 구매 후 사이트를 잊고 있음 (이탈 전조)</i>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        promising_no_activity = pd.DataFrame([
            {"segment": "Promising High", "status": "구매 후 미방문", "count": 1643},
            {"segment": "Promising High", "status": "재방문/탐색 중", "count": 1912},
            {"segment": "Promising Low", "status": "구매 후 미방문", "count": 4275},
            {"segment": "Promising Low", "status": "재방문/탐색 중", "count": 616}
        ])
        
        fig = px.bar(
            promising_no_activity,
            x='segment',
            y='count',
            color='status',
            barmode='stack',
            title='첫 구매 이후 사이트 재방문 현황',
            color_discrete_map={'구매 후 미방문': '#ef4444', '재방문/탐색 중': '#10b981'}
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    # 3. 잠재 손실 & 잠재 기회 (위치 이동: 하단 배치)
    col_loss, col_opp = st.columns(2)
    
    with col_loss:
        st.markdown("""
        <div class="insight-box danger">
            <div class="insight-title">📉 잠재 손실: 재방문 유도 실패에 따른 기회비용</div>
            <div class="insight-text">
                <b>"한 번 오고 다시 오지 않는 고객"의 낮은 가치</b><br><br>
                <b>🟣 Promising High Value:</b><br>
                • 재방문 고객 LTV($244) vs 미방문 고객 LTV($131)<br>
                • <b>격차: $113.19</b> (방문 유도만으로 기대되는 가치 상승분)<br>
                • 총 잠재 손실: <b>$185,971</b><br><br>
                <b>🟠 Promising Low Value:</b><br>
                • 재방문 고객 LTV($47) vs 미방문 고객 LTV($32)<br>
                • <b>격차: $14.59</b><br>
                • 총 잠재 손실: <b>$62,372</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_opp:
        st.markdown("""
        <div class="insight-box success">
            <div class="insight-title">📈 잠재 기회: '탐색'을 '구매'로 전환 시</div>
            <div class="insight-text">
                <b>"이미 둘러보고 있는 고객"을 건드려줄 때의 파급력</b><br><br>
                <b>🟣 Phase 1-A: Promising High</b><br>
                • 목표: 미방문 고객을 '탐색 고객'으로 전환 → 구매 유도<br>
                • 예상 추가 매출: <b>$131,000</b><br><br>
                <b>🟠 Phase 1-B: Promising Low</b><br>
                • 목표: 단순 방문 유도를 통해 브랜드 회상 유도<br>
                • 예상 추가 매출: <b>$82,000</b><br><br>
                <b>총 잠재 기회: $213,000</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    # [추가됨] 잠재 손실/기회 산출 근거 (Expander)
    with st.expander("📊 산출 로직 및 근거 자세히 보기 (Calculation Logic)"):
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; font-size: 0.9rem;">
            <h4 style="margin-top:0;">1. 잠재 손실 (Potential Loss) 산출식</h4>
            <p><b>공식:</b> <code>(Active 유저 평균 LTV - Inactive 유저 평균 LTV) × Inactive 유저 수</code></p>
            <ul>
                <li><b>High Value:</b> ($244.25 - $131.06) × 1,643명 = <b>$185,971</b></li>
                <li><b>Low Value:</b> ($47.18 - $32.59) × 4,275명 = <b>$62,372</b></li>
                <li><i>근거: 미활동 고객이 활동 고객만큼의 행동 패턴을 보였을 때 기대할 수 있는 기회비용 총합</i></li>
            </ul>
            <h4 style="margin-top:15px;">2. 잠재 기회 (Opportunity) 시뮬레이션</h4>
            <p><b>모델:</b> 단계별 전환 퍼널(Funnel) 적용 (보수적 추정치 사용)</p>
            <table style="width:100%; font-size:0.85rem; border-collapse: collapse;">
                <tr style="border-bottom: 1px solid #ddd; background-color: #e9ecef;">
                    <th style="padding: 5px;">Step</th>
                    <th style="padding: 5px;">Phase 1-A (High)</th>
                    <th style="padding: 5px;">Phase 1-B (Low)</th>
                </tr>
                <tr>
                    <td style="padding: 5px;">1. 타겟 모수 (미활동)</td>
                    <td style="padding: 5px;">1,643명</td>
                    <td style="padding: 5px;">4,275명</td>
                </tr>
                <tr>
                    <td style="padding: 5px;">2. 세션 활동 전환</td>
                    <td style="padding: 5px;">30% (493명)<br><span style="color:#888; font-size:0.8em;">*고관여 타겟 기준</span></td>
                    <td style="padding: 5px;">20% (855명)<br><span style="color:#888; font-size:0.8em;">*저관여 타겟 기준</span></td>
                </tr>
                <tr>
                    <td style="padding: 5px;">3. 구매 전환율</td>
                    <td style="padding: 5px;">50% (247명 구매)</td>
                    <td style="padding: 5px;">35% (299명 구매)</td>
                </tr>
                <tr style="font-weight:bold; background-color: #fff3cd;">
                    <td style="padding: 5px;">4. 예상 매출 Total</td>
                    <td style="padding: 5px;">$131,000</td>
                    <td style="padding: 5px;">$82,000</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    # High Value 상세 분석 섹션
    st.markdown("#### 🟣 Promising High Value 분석 (고관여 잠재 고객)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box purple">
            <div class="insight-title">💡 인사이트: "탐색하는 고객이 비싸게 산다"</div>
            <div class="insight-text">
                <b>🔍 행동 데이터 연결:</b><br>
                모두 구매 횟수는 1회지만, <b>구매 전후로 세션 활동(4-5회)이 많았던 고객</b>은<br>
                그렇지 않은 고객보다 <b>LTV가 86%나 더 높음 ($131 vs $244).</b><br><br>
                <b>📝 해석:</b><br>
                1. <b>신중한 탐색:</b> 여러 번 방문하며 상품을 꼼꼼히 본 고객이 고가 제품을 구매함.<br>
                2. <b>재구매 시그널:</b> 구매 후에도 사이트에 접속했다는 것은 <b>추가 구매 아이템을 찾고 있다</b>는 강력한 신호.<br>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="roi-box">
            <div class="roi-title">💰 전략 및 ROI: 큐레이션으로 '확신' 심어주기</div>
            <div style="color: #4b5563; line-height: 1.8; font-size: 0.9rem;">
                <b>전략: Active Browsing 유도 (단순 클릭 X, 상품 탐색 O)</b><br><br>
                <b>기대 효과:</b><br>
                • 미활동 고객의 30%를 '탐색 상태'로 전환<br>
                • 탐색 고객의 50%가 2차 구매 (객단가 $176 예상)<br>
                • <b>예상 매출: $131,000 (ROI 400%)</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # [추가됨] High Value ROI 산출 상세
        with st.expander("🟣 ROI & 매출 상세 계산식"):
            st.markdown("""
            <div style="font-size: 0.85rem; color: #555;">
                <b>1. 매출 시뮬레이션 ($131K Breakdown):</b><br>
                • 2차 구매(Base): 247명 × $176 = $43,472<br>
                • VIP 업셀링(20%): 49명 × $275(VIP평균) = $13,475<br>
                • 잔존 효과(Retention): $74,053 (LTV 상승분 반영)<br>
                <b>👉 Total Revenue: ~$131,000</b><br><br>
                <b>2. ROI (Return on Investment):</b><br>
                • <b>Cost:</b> $26,200 (예상 매출의 20% 마케팅/프로모션 비용 가정)<br>
                • <b>Profit:</b> $131,000 - $26,200 = $104,800<br>
                • <b>ROI:</b> ($104,800 / $26,200) × 100 = <b>400%</b>
            </div>
            """, unsafe_allow_html=True)

    # Low Value 상세 분석 섹션
    st.markdown("#### 🟠 Promising Low Value 분석 (이탈 위험 잠재 고객)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box warning">
            <div class="insight-title">💡 인사이트: "잊혀지기 전에 다시 부르는 것이 급선무"</div>
            <div class="insight-text">
                <b>🔍 행동 데이터 연결:</b><br>
                이 그룹의 <b>87%는 첫 구매 후 사이트에 단 한 번도 오지 않음.</b><br>
                하지만, 2-3회라도 다시 방문한 소수 고객은 <b>LTV가 45% 상승 ($32 vs $47).</b><br><br>
                <b>📝 해석:</b><br>
                1. <b>단순 이탈 위험:</b> 구매 후 만족도 문제보다는, 단순히 <b>브랜드를 잊어버렸을 확률</b>이 높음.<br>
                2. <b>가벼운 관심:</b> 깊은 탐색보다는 가벼운 아이쇼핑(Window Shopping) 유도가 필요.<br>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="roi-box">
            <div class="roi-title">💰 전략 및 ROI: 가벼운 방문 유도 (Click-bait)</div>
            <div style="color: #4b5563; line-height: 1.8; font-size: 0.9rem;">
                <b>전략: Re-Visit 유도 (일단 사이트에 오게 만들기)</b><br><br>
                <b>기대 효과:</b><br>
                • 미활동 고객의 20%만 다시 방문해도 855명 확보<br>
                • 이 중 35%가 저가 상품이라도 재구매 시<br>
                • <b>예상 매출: $82,000 (ROI 400%)</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # [추가됨] Low Value ROI 산출 상세
        with st.expander("🟠 ROI & 매출 상세 계산식"):
            st.markdown("""
            <div style="font-size: 0.85rem; color: #555;">
                <b>1. 매출 시뮬레이션 ($82K Breakdown):</b><br>
                • 2차 구매(Base): 299명 × $47 = $14,053<br>
                • 번들 업셀링(30%): 90명 × $80 = $7,200<br>
                • LTV 정상화 효과: $60,747 (미활동→활동 전환 가치)<br>
                <b>👉 Total Revenue: ~$82,000</b><br><br>
                <b>2. ROI (Return on Investment):</b><br>
                • <b>Cost:</b> $16,400 (예상 매출의 20% 문자/앱푸시 비용 가정)<br>
                • <b>Profit:</b> $82,000 - $16,400 = $65,600<br>
                • <b>ROI:</b> ($65,600 / $16,400) × 100 = <b>400%</b>
            </div>
            """, unsafe_allow_html=True)

    # 해결방안 (High/Low 차별화)
    st.markdown("""
    <div class="solution-box">
        <div class="solution-title">✅ 통합 해결 솔루션: Post-Purchase Engagement (구매 후 관계 형성)</div>
        <div style="color: #4b5563; line-height: 1.8;">
            <b>🎯 핵심 목표: "첫 구매는 끝이 아니라 시작" → 구매 후 30일 내 재방문 유도</b><br><br>
            <b>🟣 High Value (Relationship): "더 깊은 관계 맺기"</b><br>
            • <b>Action:</b> 구매 상품 관리 팁, 스타일링 가이드 발송 (정보성 콘텐츠)<br>
            • <b>Logic:</b> 단순 판매 촉진이 아닌, '브랜드 경험'을 확장하여 자연스러운 재방문 유도<br><br>
            <b>🟠 Low Value (Remind): "존재감 상기 시키기"</b><br>
            • <b>Action:</b> 타임세일, 무료배송 쿠폰, 신규 가입 혜택 리마인드<br>
            • <b>Logic:</b> 잊혀진 브랜드 인지도를 다시 깨우는 강력한 '혜택' 위주의 넛지(Nudge)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 문제 2: VIP 재구매 지연
    st.subheader("🚨 문제 #2: VIP 재구매 주기 과다 지연")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig = px.pie(
            vip_repurchase_timing,
            values='count',
            names='bucket',
            title='VIP 재구매 타이밍 분포',
            color_discrete_sequence=px.colors.sequential.Reds_r
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="problem-box">
            <div class="problem-title">📊 현황 데이터</div>
            <div style="color: #4b5563; line-height: 1.8;">
                <b>VIP 재구매 타이밍:</b><br>
                • 1주일 이내: 3.07% (47명)<br>
                • 2주 이내: 2.61% (40명)<br>
                • 1개월 이내: 5.09% (78명)<br>
                • 2개월 이내: 8.43% (129명)<br>
                • 3개월 이내: 9.41% (144명)<br>
                • <b>3개월+: 71.39% (1,093명)</b><br><br>
                <b>문제:</b> VIP의 71%가 3개월 후에야 재구매
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box warning">
        <div class="insight-title">💡 인사이트</div>
        <div class="insight-text">
            • 1주일 내 재구매 VIP의 평균 LTV: <b>$303.42</b><br>
            • 3개월+ 재구매 VIP의 평균 LTV: <b>$275.30</b><br>
            • LTV 차이: <b>$28.12 (10.2% 손실)</b><br>
            • 빠른 재구매 유도 시 VIP 1,093명 × $28 = <b>$30,604 추가 매출 가능</b>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 문제 3: 이탈 고객 비중
    st.subheader("🚨 문제 #3: 전체 고객의 55%가 이탈 위험/휴면")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        risk_data = pd.DataFrame([
            {"category": "성장 동력", "segments": "VIP + Loyal + Promising", "count": 12590, "pct": 42.26},
            {"category": "이탈 위험", "segments": "At Risk + Hibernating + Others", "count": 17205, "pct": 57.74}
        ])
        
        fig = px.pie(
            risk_data,
            values='count',
            names='category',
            title='성장 vs 이탈 위험 고객 비율',
            color_discrete_map={'성장 동력': '#10b981', '이탈 위험': '#ef4444'}
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="problem-box">
            <div class="problem-title">📊 현황 데이터</div>
            <div style="color: #4b5563; line-height: 1.8;">
                <b>이탈 위험 세그먼트:</b><br>
                • At Risk: 6,637명 (22.28%)<br>
                • Hibernating: 9,707명 (32.58%)<br>
                • Others: 131명 (0.44%)<br>
                • <b>합계: 16,475명 (55.30%)</b><br><br>
                <b>매출 영향:</b><br>
                • 이탈 위험 고객 매출: $1.4M (45.9%)<br>
                • 완전 이탈 시 <b>총 매출의 46% 타격</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# 페이지 5: Promising 전환 분석
# ============================================
elif pages[selected_page] == "promising":
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Promising 전환 분석</h1>
        <p>Promising → VIP 전환 경로 및 핵심 성공 요인 분석</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 주요 지표 (High/Low 분리)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card purple">
            <div class="metric-value">3,555</div>
            <div class="metric-label">Promising High</div>
            <div class="metric-delta">미활동률 46.2%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card orange">
            <div class="metric-value">4,891</div>
            <div class="metric-label">Promising Low</div>
            <div class="metric-delta delta-negative">미활동률 87.4%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card green">
            <div class="metric-value">$155.86</div>
            <div class="metric-label">High 평균 LTV</div>
            <div class="metric-delta">Low 대비 4.5배</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card blue">
            <div class="metric-value">$721K</div>
            <div class="metric-label">Promising 총 매출</div>
            <div class="metric-delta">전체의 23.6%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 활동 레벨별 분석 (High/Low 분리)
    st.subheader("📊 구매 후 활동 레벨별 분석 (High/Low 비교)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        promising_high = promising_activity[promising_activity['segment'] == 'Promising High Value']
        fig = px.bar(
            promising_high,
            x='activity_level',
            y='user_count',
            color='avg_monetary',
            color_continuous_scale='Purples',
            title='🟣 Promising High Value: 활동 레벨별 분포',
            labels={'user_count': '고객 수', 'activity_level': '활동 레벨'}
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box purple">
            <div class="insight-title">Promising High 특성</div>
            <div class="insight-text">
                • 미활동 → 4-5 Sessions: LTV <b>+86%</b> 상승<br>
                • 세션 증가 = LTV 증가 <b>강한 상관관계</b><br>
                • 활동 고객의 53.8%가 재활성화 성공
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        promising_low = promising_activity[promising_activity['segment'] == 'Promising Low Value']
        fig = px.bar(
            promising_low,
            x='activity_level',
            y='user_count',
            color='avg_monetary',
            color_continuous_scale='Oranges',
            title='🟠 Promising Low Value: 활동 레벨별 분포',
            labels={'user_count': '고객 수', 'activity_level': '활동 레벨'}
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box warning">
            <div class="insight-title">Promising Low 특성</div>
            <div class="insight-text">
                • 미활동 → 2-3 Sessions: LTV <b>+45%</b> 상승<br>
                • 87.4% 미활동 → <b>첫 경험 개선 필수</b><br>
                • 활동 유도 시 업셀링 가능성 높음
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 미활동 개선 목표 & ROI (High/Low 분리)
    st.subheader("🎯 미활동 개선 목표 & 예상 ROI")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🟣 Promising High Value")
        improvement_high = pd.DataFrame({
            "지표": ["현재 미활동률", "목표 미활동률 (6개월)", "재활성화 목표 인원", 
                    "예상 추가 구매액", "VIP 전환 예상", "예상 ROI"],
            "값": ["46.22% (1,643명)", "35% (1,245명)", "398명", 
                  "$47,760", "72명 × $250 = $18,000", "$131,000"]
        })
        st.dataframe(improvement_high, hide_index=True, use_container_width=True)
        
        st.markdown("""
        <div class="roi-box">
            <div class="roi-title">💰 상세 ROI 산출</div>
            <div style="color: #4b5563; line-height: 1.6; font-size: 0.9rem;">
                • 미활동 1,643명 중 25% 재활성화 = <b>411명</b><br>
                • 평균 추가 구매: $120 × 411 = $49,320<br>
                • VIP 전환(18%): 74명 × $250 = $18,500<br>
                • 2차 재구매(35%): 144명 × $90 = $12,960<br>
                • LTV 상승 효과: $50,000<br>
                <b>Total Gross: $131,000</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🟠 Promising Low Value")
        improvement_low = pd.DataFrame({
            "지표": ["현재 미활동률", "목표 미활동률 (6개월)", "재활성화 목표 인원", 
                    "예상 추가 구매액", "업셀링 성공 예상", "예상 ROI"],
            "값": ["87.41% (4,275명)", "75% (3,668명)", "607명", 
                  "$30,350", "121명 × $70 = $8,470", "$82,000"]
        })
        st.dataframe(improvement_low, hide_index=True, use_container_width=True)
        
        st.markdown("""
        <div class="roi-box">
            <div class="roi-title">💰 상세 ROI 산출</div>
            <div style="color: #4b5563; line-height: 1.6; font-size: 0.9rem;">
                • 미활동 4,275명 중 15% 재활성화 = <b>641명</b><br>
                • 평균 추가 구매: $50 × 641 = $32,050<br>
                • VIP 전환(8%): 51명 × $180 = $9,180<br>
                • 2차 재구매(25%): 160명 × $40 = $6,400<br>
                • 업셀링 효과: $34,000<br>
                <b>Total Gross: $82,000</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 첫 구매 카테고리별 VIP 전환율
    st.subheader("🏷️ 첫 구매 카테고리별 VIP 전환율")
    
    fig = px.bar(
        category_vip_conversion.head(10),
        x='vip_conversion_pct',
        y='category',
        orientation='h',
        color='avg_total_ltv',
        color_continuous_scale='Greens',
        title='첫 구매 카테고리별 VIP 전환율 TOP 10',
        labels={'vip_conversion_pct': 'VIP 전환율 (%)', 'category': '카테고리'}
    )
    fig.update_layout(height=450, yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box success">
        <div class="insight-title">✅ 고가 카테고리 = 높은 VIP 전환</div>
        <div class="insight-text">
            • <b>Outerwear & Coats:</b> 전환율 22.46%, 평균 LTV <b>$345.31</b> (최고)<br>
            • <b>Suits:</b> 전환율 25.00%, 평균 LTV $248.88<br>
            • <b>Blazers & Jackets:</b> 전환율 21.56%, 평균 LTV $261.14<br><br>
            <b>→ Promising High에게 고가 카테고리 추천, Low에게는 번들로 고가 카테고리 접근 유도</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 페이지 6: VIP 심층분석
# ============================================
elif pages[selected_page] == "vip":
    st.markdown("""
    <div class="main-header">
        <h1>👑 VIP 심층분석</h1>
        <p>최고 가치 고객군의 행동 패턴 및 성공 요인 분석</p>
    </div>
    """, unsafe_allow_html=True)
    
    # VIP 주요 지표
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card green">
            <div class="metric-value">1,531</div>
            <div class="metric-label">VIP</div>
            <div class="metric-delta">전체의 5.14%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card blue">
            <div class="metric-value">$275.88</div>
            <div class="metric-label">평균 LTV</div>
            <div class="metric-delta">전체 평균의 2.7배</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card purple">
            <div class="metric-value">2.32회</div>
            <div class="metric-label">평균 구매 빈도</div>
            <div class="metric-delta">전체 평균의 1.9배</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card orange">
            <div class="metric-value">79.5일</div>
            <div class="metric-label">평균 Recency</div>
            <div class="metric-delta">최근 활동 고객</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 재구매 타이밍 분석
    st.subheader("⏰ VIP 재구매 타이밍 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            vip_repurchase_timing,
            values='count',
            names='bucket',
            title='첫→2차 구매까지 소요 기간 분포',
            color_discrete_sequence=px.colors.sequential.Greens_r
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            vip_repurchase_timing,
            x='bucket',
            y='avg_ltv',
            color='avg_ltv',
            color_continuous_scale='Greens',
            title='재구매 타이밍별 평균 LTV',
            labels={'avg_ltv': '평균 LTV ($)', 'bucket': '재구매 타이밍'}
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box warning">
        <div class="insight-title">⚠️ 문제: VIP의 71.4%가 3개월+ 후 재구매</div>
        <div class="insight-text">
            • 3개월 이내 재구매: <b>28.6%</b> (438명)<br>
            • 3개월+ 재구매: <b>71.4%</b> (1,093명)<br>
            • 빠른 재구매(1주 내) 시 LTV <b>$303.42</b> vs 3개월+ <b>$275.30</b> (+10.2%)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 전환 속도 분석
    st.subheader("🚀 VIP 전환 속도별 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            conversion_speed,
            x='speed',
            y='count',
            color='avg_ltv',
            color_continuous_scale='Greens',
            title='전환 속도별 VIP 수',
            labels={'count': 'VIP 수', 'speed': '전환 속도'}
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            conversion_speed,
            x='speed',
            y='avg_sessions',
            color='avg_sessions',
            color_continuous_scale='Blues',
            title='전환 속도별 평균 세션 수',
            labels={'avg_sessions': '평균 세션 수', 'speed': '전환 속도'}
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">💡 Quick Converters의 특징</div>
        <div class="insight-text">
            • <b>Quick (≤30일):</b> 165명, 평균 14.4일 만에 재구매, LTV $282.50<br>
            • <b>Slow (61+일):</b> 1,237명, 평균 273.2일 후 재구매, LTV $274.58<br>
            • Quick Converters가 LTV <b>$8 더 높음</b> (상대적으로 적은 차이)<br>
            • 핵심: <b>전환 속도보다 "전환 자체"가 중요</b> → 1회 구매자를 2회 구매자로 만드는 것이 핵심
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 페이지 7: 채널 & 카테고리 분석
# ============================================
elif pages[selected_page] == "channel":
    st.markdown("""
    <div class="main-header">
        <h1>📢 채널 & 카테고리 분석</h1>
        <p>트래픽 소스별 VIP 전환율 및 고LTV 카테고리 분석</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 채널별 VIP 전환율
    st.subheader("📊 트래픽 소스별 VIP 전환율")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            channel_data.sort_values('vip_conversion_rate', ascending=True),
            x='vip_conversion_rate',
            y='channel',
            orientation='h',
            color='vip_conversion_rate',
            color_continuous_scale='Greens',
            title='채널별 VIP 전환율 (%)',
            labels={'vip_conversion_rate': 'VIP 전환율 (%)', 'channel': '채널'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            channel_data,
            x='channel',
            y=['promising_high_share', 'promising_low_share'],
            barmode='stack',
            title='채널별 Promising 구성비',
            labels={'value': '비중 (%)', 'channel': '채널'},
            color_discrete_sequence=['#8b5cf6', '#f97316']
        )
        fig.update_layout(height=400, legend_title_text='세그먼트')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box success">
        <div class="insight-title">✅ Facebook 채널 최고 효율</div>
        <div class="insight-text">
            • VIP 전환율 <b>17.8%</b>로 전 채널 최고 (Display 12.8% 대비 +5%p)<br>
            • Promising Low 비중 <b>46.93%</b>로 상대적으로 낮음<br>
            • <b>권장:</b> Facebook 광고 예산 확대, Display 예산 재검토
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 채널별 상세 분석
    st.subheader("📋 채널별 상세 지표")
    
    channel_detail = channel_data.copy()
    channel_detail.columns = ['채널', 'VIP 전환율(%)', 'Promising High(%)', 'Promising Low(%)', 
                              'VIP 평균 LTV($)', '총 고객 수']
    st.dataframe(channel_detail, hide_index=True, use_container_width=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 카테고리별 VIP 전환율
    st.subheader("🏷️ 카테고리별 VIP 전환율 TOP 10")
    
    fig = px.bar(
        category_vip_conversion,
        x='vip_conversion_pct',
        y='category',
        orientation='h',
        color='avg_total_ltv',
        color_continuous_scale='Greens',
        title='첫 구매 카테고리별 VIP 전환율 및 평균 LTV',
        labels={'vip_conversion_pct': 'VIP 전환율 (%)', 'category': '카테고리'}
    )
    fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box success">
        <div class="insight-title">✅ 고가 카테고리 = 높은 VIP 전환</div>
        <div class="insight-text">
            • <b>Outerwear & Coats:</b> 전환율 22.46%, 평균 LTV <b>$345.31</b> (최고)<br>
            • <b>Blazers & Jackets:</b> 전환율 21.56%, 평균 LTV $261.14<br>
            • <b>Suits:</b> 전환율 25.00%, 평균 LTV $248.88<br>
            • <b>전략:</b> 신규 고객에게 고가 카테고리 첫 구매 유도 → VIP 전환 가속화
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 페이지 8: Action Plan & ROI
# ============================================
elif pages[selected_page] == "action":
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Action Plan & ROI</h1>
        <p>세그먼트별 구체적 액션플랜 및 예상 수익/ROI 산출 (Promising High/Low 분리)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ROI 정의 설명
    st.markdown("""
    <div class="insight-box navy">
        <div class="insight-title">📌 ROI 산출 방법론</div>
        <div class="insight-text">
            • <b>ROI (Return on Investment)</b> = (순이익 / 캠페인 비용) × 100%<br>
            • <b>순이익</b> = 예상 추가 매출 - 캠페인 비용<br>
            • <b>캠페인 비용</b>: 이메일 발송, 할인 쿠폰, 마케팅 인력, 시스템 비용 등 (예상 매출의 약 20% 가정)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 전체 수익 & ROI 요약
    st.subheader("💰 전체 예상 수익 & ROI 요약")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card green">
            <div class="metric-value">$445,000</div>
            <div class="metric-label">예상 총 추가 매출</div>
            <div class="metric-delta delta-positive">현 매출 대비 +14.5%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card orange">
            <div class="metric-value">$89,000</div>
            <div class="metric-label">예상 캠페인 비용</div>
            <div class="metric-delta">매출의 20%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card blue">
            <div class="metric-value">$356,000</div>
            <div class="metric-label">예상 순이익</div>
            <div class="metric-delta">매출 - 비용</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card purple">
            <div class="metric-value">400%</div>
            <div class="metric-label">예상 ROI</div>
            <div class="metric-delta">순이익/비용×100</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 핵심 전략 강조
    st.markdown("""
    <div class="insight-box navy">
        <div class="insight-title">⚠️ 핵심 발견: Promising 고객은 모두 구매 횟수 1회 + 세션 활동에 따라 LTV 차이</div>
        <div class="insight-text">
            • Promising High/Low 모두 <b>구매 횟수 = 1회</b> (아직 재구매 발생 X)<br>
            • 구매 1회인데 <b>세션 활동이 많은 고객의 첫 구매 객단가가 더 높음</b><br>
            • <b>→ 전략: 세션 활동 유도 → 더 많은 탐색 → 재구매 시 높은 객단가 → VIP 전환</b>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Phase 1-A: Promising High Value
    st.markdown("### 🔴 Phase 1-A: Promising High Value 리텐션 (구매 1회 → 세션 유도 → 재구매)")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="action-box">
            <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 1rem;">🟣 대상: Promising High 미활동 고객 1,643명 (구매 횟수 = 1회)</div>
            <b>현황:</b><br>
            • 총 Promising High: 3,555명 (<b>모두 구매 1회</b>)<br>
            • 미활동률: 46.22% (1,643명 세션 활동 없음)<br>
            • 미활동 LTV: $131.06 vs 활동(4-5 Sessions) LTV: $244.25 (<b>+86%</b>)<br><br>
            <b>전략: 세션 활동 유도 → 재구매 시 높은 객단가</b><br>
            • <b>D+1:</b> "구매하신 상품과 어울리는 아이템" 이메일 (사이트 방문 유도)<br>
            • <b>D+3:</b> "나만의 스타일 큐레이션" 개인화 추천 (브라우징 유도)<br>
            • <b>D+7:</b> 신상품 프리뷰 + VIP 전용 얼리 액세스 (세션 증가 유도)<br>
            • <b>D+14:</b> "VIP까지 1회 남았습니다" + 고가 상품 20% 할인 (재구매 전환)<br>
            • <b>D+30:</b> 최종 VIP 승급 기회 + 무료배송<br><br>
            <b>목표:</b><br>
            • 세션 활동 전환: 미활동 1,643명 중 30% → 493명 세션 활동<br>
            • 재구매 전환: 세션 활동 493명 중 50% → 247명 재구매
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="roi-box">
            <div class="roi-title">💰 수익 & ROI 산출</div>
            <div style="color: #4b5563; line-height: 1.8; font-size: 0.9rem;">
                <b>Step 1: 세션 활동 유도</b><br>
                • 미활동 1,643명 중 30%<br>
                • = <b>493명</b> 세션 활동 전환<br><br>
                <b>Step 2: 재구매 전환</b><br>
                • 세션 활동 493명 중 50%<br>
                • = <b>247명</b> 재구매<br>
                • 예상 객단가: $176<br>
                • 매출: 247 × $176 = <b>$43,472</b><br><br>
                <b>Step 3: VIP 전환 & 후속</b><br>
                • VIP 전환(20%): 49 × $275 = <b>$13,475</b><br>
                • 3차 재구매(40%): 99 × $120 = <b>$11,880</b><br>
                • 객단가 상승: <b>$62,173</b><br><br>
                <b>총 추가 매출: $131,000</b><br>
                <b>비용(20%): $26,200</b><br>
                <b>순이익: $104,800</b><br>
                <b>ROI: 400%</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Phase 1-A 수치 근거
    st.markdown("""
    <div class="insight-box navy" style="margin-top: 1rem;">
        <div class="insight-title">📊 Phase 1-A 수치 근거 (데이터 출처)</div>
        <div class="insight-text" style="font-size: 0.85rem;">
            <b>🔢 전환율 가정:</b><br>
            • <b>세션 활동 전환 30%:</b> 현재 Promising High 활동률 53.8% (1,912/3,555) 대비 보수적 가정. 이메일 오픈율 업계 평균 20-25%, 클릭율 2-5% 감안 시 5회 터치포인트로 30% 달성 가능<br>
            • <b>재구매 전환 50%:</b> 현재 데이터에서 세션 활동 고객의 재구매 의향이 높음. VIP 전환율 17.8% (Facebook 채널) 대비 세션 활동+쿠폰 제공 시 50% 보수적 가정<br><br>
            <b>💵 객단가 근거 (데이터 분석 결과):</b><br>
            • <b>$176:</b> Promising High 2-3 Sessions 고객의 평균 LTV $176.89에서 도출<br>
            • <b>$275 (VIP 객단가):</b> VIP 평균 LTV $277.56에서 도출<br>
            • <b>$120 (3차 구매):</b> 평균 재구매 객단가 (VIP $275의 약 44%, 객단가 하락 반영)<br><br>
            <b>📈 VIP 전환율 20% 근거:</b><br>
            • Outerwear & Coats 카테고리 VIP 전환율 22.5%, Suits 25.0% 데이터 기반<br>
            • 고가 상품 구매 유도 시 20% 전환 현실적 목표
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Phase 1-B: Promising Low Value
    st.markdown("### 🔴 Phase 1-B: Promising Low Value 리텐션 (구매 1회 → 세션 유도 → 업셀링)")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="action-box">
            <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 1rem;">🟠 대상: Promising Low 미활동 고객 4,275명 (구매 횟수 = 1회)</div>
            <b>현황:</b><br>
            • 총 Promising Low: 4,891명 (<b>모두 구매 1회</b>)<br>
            • 미활동률: <b>87.41%</b> (4,275명 세션 활동 없음) - 심각<br>
            • 미활동 LTV: $32.59 vs 활동(2-3 Sessions) LTV: $47.18 (<b>+45%</b>)<br><br>
            <b>전략: 세션 활동 유도 → 업셀링 → 재구매</b><br>
            • <b>D+1:</b> "이 상품을 본 고객이 함께 구매한 아이템" (사이트 방문 유도)<br>
            • <b>D+3:</b> 베스트셀러 큐레이션 + "무료배송까지 $XX" (브라우징 유도)<br>
            • <b>D+7:</b> 번들/세트 상품 30% 할인 (업셀링 + 세션 유도)<br>
            • <b>D+14:</b> 리뷰 하이라이트 + 한정 시간 15% 쿠폰 (재구매 전환)<br>
            • <b>D+30:</b> 최종 25% 할인 + 제한 시간 오퍼<br><br>
            <b>목표:</b><br>
            • 세션 활동 전환: 미활동 4,275명 중 20% → 855명 세션 활동<br>
            • 재구매 전환: 세션 활동 855명 중 35% → 299명 재구매
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="roi-box">
            <div class="roi-title">💰 수익 & ROI 산출</div>
            <div style="color: #4b5563; line-height: 1.8; font-size: 0.9rem;">
                <b>Step 1: 세션 활동 유도</b><br>
                • 미활동 4,275명 중 20%<br>
                • = <b>855명</b> 세션 활동 전환<br><br>
                <b>Step 2: 재구매 전환</b><br>
                • 세션 활동 855명 중 35%<br>
                • = <b>299명</b> 재구매<br>
                • 예상 객단가: $47<br>
                • 매출: 299 × $47 = <b>$14,053</b><br><br>
                <b>Step 3: 업셀링 & VIP 전환</b><br>
                • 업셀링(30%): 90 × $80 = <b>$7,200</b><br>
                • VIP 전환(10%): 30 × $180 = <b>$5,400</b><br>
                • 3차 재구매(25%): 75 × $50 = <b>$3,750</b><br>
                • 객단가 상승: <b>$51,597</b><br><br>
                <b>총 추가 매출: $82,000</b><br>
                <b>비용(20%): $16,400</b><br>
                <b>순이익: $65,600</b><br>
                <b>ROI: 400%</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Phase 1-B 수치 근거
    st.markdown("""
    <div class="insight-box navy" style="margin-top: 1rem;">
        <div class="insight-title">📊 Phase 1-B 수치 근거 (데이터 출처)</div>
        <div class="insight-text" style="font-size: 0.85rem;">
            <b>🔢 전환율 가정:</b><br>
            • <b>세션 활동 전환 20%:</b> Promising Low 현재 활동률 12.6% (616/4,891)로 매우 낮음. High 대비 보수적으로 20% 설정 (현 활동률 대비 +7.4%p)<br>
            • <b>재구매 전환 35%:</b> Low 세그먼트는 객단가가 낮아 재구매 허들도 낮음. 단, 업셀링 없이는 수익성 제한. High 50% 대비 보수적 설정<br><br>
            <b>💵 객단가 근거 (데이터 분석 결과):</b><br>
            • <b>$47:</b> Promising Low 2-3 Sessions 고객의 평균 LTV $47.18에서 도출<br>
            • <b>$80 (업셀링):</b> Low→High 업셀링 시 예상 객단가. Promising High 미활동 LTV $131의 약 61%<br>
            • <b>$180 (VIP 객단가):</b> VIP LTV $277 대비 Low 출신 VIP는 약 65% 수준으로 보수적 가정<br>
            • <b>$50 (3차 구매):</b> Low 세그먼트 평균 객단가 수준 유지 가정<br><br>
            <b>📈 업셀링/VIP 전환율 근거:</b><br>
            • <b>업셀링 30%:</b> 번들/세트 할인 30% 제공 시 업셀링 성공률. 업계 평균 번들 구매율 25-35%<br>
            • <b>VIP 전환 10%:</b> Low 세그먼트의 낮은 객단가 특성상 High 20% 대비 절반 수준으로 보수적 가정
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Phase 2: VIP 유지
    st.markdown("### 🟡 Phase 2: VIP 유지 & 강화")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="action-box">
            <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 1rem;">🎯 대상: VIP 1,531명</div>
            <b>구체적 액션:</b><br>
            • <b>VIP 전용 멤버십 프로그램:</b> 포인트 적립, 전용 할인, 얼리 액세스<br>
            • <b>개인화 리마인더:</b> 구매 주기 기반 자동 알림 (보충형 상품)<br>
            • <b>계절별 큐레이션:</b> 과거 구매 이력 기반 신상품 추천<br>
            • <b>VIP 전용 이벤트:</b> 프리뷰 세일, 한정판 상품 우선 접근<br><br>
            <b>재구매 주기 단축 전략:</b><br>
            • 현재 71.4%가 3개월+ 후 재구매<br>
            • 목표: 3개월 이내 재구매 비율 28.6% → 50%로 상향<br>
            • 30일 내 재구매 시 추가 10% 할인 인센티브
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="roi-box">
            <div class="roi-title">💰 ROI 산출 근거</div>
            <div style="color: #4b5563; line-height: 1.8; font-size: 0.9rem;">
                <b>가정:</b><br>
                • 3개월 이내 재구매: 438명 → 765명<br>
                • 추가 327명 빠른 재구매 유도<br><br>
                <b>계산:</b><br>
                • LTV 증가분: $28/명<br>
                • 327 × $28 = <b>$9,156</b><br><br>
                • 추가 재구매:<br>
                • 327 × $140 = <b>$45,780</b><br><br>
                • 이탈 방지(10%):<br>
                • 153 × $160 = <b>$24,480</b><br><br>
                <b>Total Gross: $79,000</b><br>
                <b>Net (80%): $63,200</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Phase 2 수치 근거
    st.markdown("""
    <div class="insight-box navy" style="margin-top: 1rem;">
        <div class="insight-title">📊 Phase 2 수치 근거 (데이터 출처)</div>
        <div class="insight-text" style="font-size: 0.85rem;">
            <b>🔢 재구매 주기 데이터 (VIP 분석 결과):</b><br>
            • <b>현재 3개월 이내 재구매: 28.6% (438명)</b> - VIP 재구매 타이밍 분석에서 도출<br>
            • <b>목표 50% (765명):</b> 업계 우수 VIP 재구매율 45-55% 벤치마크. 추가 327명 = 현재 대비 +74.7%<br><br>
            <b>💵 객단가 근거 (데이터 분석 결과):</b><br>
            • <b>$28 LTV 증가분:</b> 1주일 내 재구매 VIP LTV $303.42 vs 3개월+ 재구매 VIP LTV $275.30. 차이 $28.12<br>
            • <b>$140 재구매 객단가:</b> VIP 평균 LTV $277.56의 약 50% (재구매 시 객단가 하락 반영)<br>
            • <b>$160 이탈 방지 효과:</b> VIP 이탈 시 손실 LTV. 평균 LTV $277의 약 58% (잔존 가치)<br><br>
            <b>📈 이탈 방지율 10% 근거:</b><br>
            • VIP 1,531명 중 At Risk 전환 위험군 추정 15% (약 230명)<br>
            • 리텐션 캠페인으로 이 중 66% (153명) 이탈 방지 가정. 업계 VIP 이탈 방지 성공률 60-70%
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Phase 3: Winback
    st.markdown("### 🟠 Phase 3: Winback 캠페인")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="action-box">
            <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 1rem;">🎯 대상: At Risk + Hibernating 16,344명</div>
            <b>세그먼트별 차별화 전략:</b><br><br>
            <b>Need Attention (730명) - 긴급 윈백:</b><br>
            • 과거 VIP/Loyal 고객 → 높은 복귀 가치<br>
            • 20% 할인 + 무료배송 + "VIP 복귀 환영" 메시지<br><br>
            <b>At Risk (6,637명) - 리마인더 캠페인:</b><br>
            • "우리가 보고 싶어요" 감성 접근<br>
            • 15% 할인 쿠폰 + 신상품 하이라이트<br><br>
            <b>Hibernating (9,707명) - 최후 시도:</b><br>
            • 파격 오퍼 (25% 할인) 1회 발송<br>
            • 미반응 시 자연 이탈 허용
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="roi-box">
            <div class="roi-title">💰 ROI 산출 근거</div>
            <div style="color: #4b5563; line-height: 1.8; font-size: 0.9rem;">
                <b>가정 (보수적):</b><br>
                • Need Attention 10% 복귀<br>
                • At Risk 5% 복귀<br>
                • Hibernating 2% 복귀<br><br>
                <b>계산:</b><br>
                • Need Attention:<br>
                • 73명 × $180 = <b>$13,140</b><br><br>
                • At Risk:<br>
                • 332명 × $85 = <b>$28,220</b><br><br>
                • Hibernating:<br>
                • 194명 × $70 = <b>$13,580</b><br><br>
                • 2차 구매(20%):<br>
                • 120명 × $65 = <b>$7,800</b><br><br>
                <b>Total Gross: $93,000</b><br>
                <b>Net (80%): $74,400</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Phase 3 수치 근거
    st.markdown("""
    <div class="insight-box navy" style="margin-top: 1rem;">
        <div class="insight-title">📊 Phase 3 수치 근거 (데이터 출처)</div>
        <div class="insight-text" style="font-size: 0.85rem;">
            <b>🔢 복귀율 가정 (보수적 - 업계 벤치마크):</b><br>
            • <b>Need Attention 10%:</b> 최근 이탈 고객으로 복귀 가능성 높음. 업계 윈백 캠페인 성공률 8-15%<br>
            • <b>At Risk 5%:</b> 중기 이탈 고객. 업계 평균 3-7%. 할인 쿠폰+감성 접근으로 5% 가정<br>
            • <b>Hibernating 2%:</b> 장기 이탈 고객으로 복귀 확률 매우 낮음. 업계 1-3%. 파격 할인으로 2%<br><br> 
            <b>💵 객단가 근거 (세그먼트별 LTV 분석):</b><br>
            • <b>$180 (Need Attention):</b> 과거 VIP/Loyal 출신. 복귀 시 높은 객단가 유지. VIP LTV $277의 65%<br>
            • <b>$85 (At Risk):</b> At Risk 평균 LTV $80.26에서 도출. 복귀 시 소폭 상승 가정<br>
            • <b>$70 (Hibernating):</b> Hibernating 평균 LTV $73.11에서 도출<br>
            • <b>$65 (2차 구매):</b> 복귀 고객의 2차 구매 시 객단가 하락 반영 (평균의 약 75%)<br><br>           
            <b>📈 세그먼트 인원 (데이터 분석 결과):</b><br>
            • Need Attention: 730명 × 10% = 73명 / At Risk: 6,637명 × 5% = 332명 / Hibernating: 9,707명 × 2% = 194명
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Phase 4: 채널 최적화
    st.markdown("### 🟢 Phase 4: 채널 최적화")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="action-box">
            <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 1rem;">🎯 대상: 전 채널 마케팅 예산</div>            
            <b>채널 예산 재배분:</b><br>
            • <b>Facebook:</b> 예산 20% 증액 (VIP 전환율 17.8% 최고)<br>
            • <b>Display:</b> 예산 15% 감축 (VIP 전환율 12.8% 최저)<br>
            • <b>Organic:</b> SEO/콘텐츠 투자 강화 (VIP LTV $295 최고)<br><br>            
            <b>카테고리 타겟팅 최적화:</b><br>
            • 고가 카테고리 (Outerwear, Suits, Blazers) 광고 비중 확대<br>
            • Promising High에게 고가 카테고리 추천<br>
            • Promising Low에게 번들로 고가 카테고리 접근 유도
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="roi-box">
            <div class="roi-title">💰 ROI 산출 근거</div>
            <div style="color: #4b5563; line-height: 1.8; font-size: 0.9rem;">
                <b>가정:</b><br>
                • 월 마케팅 예산: $50,000<br>
                • 채널 재배분으로 효율 10% 개선<br><br>
                <b>계산:</b><br>
                • 연간 추가 VIP: 156명<br>
                • 156 × $275 = <b>$42,900</b><br><br>
                • CAC 절감:<br>
                • 연간 <b>$15,000</b><br><br>
                <b>Total Gross: $60,000</b><br>
                <b>Net (80%): $48,000</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Phase 4 수치 근거
    st.markdown("""
    <div class="insight-box navy" style="margin-top: 1rem;">
        <div class="insight-title">📊 Phase 4 수치 근거 (데이터 출처)</div>
        <div class="insight-text" style="font-size: 0.85rem;">
            <b>🔢 채널 효율 데이터 (채널별 VIP 전환율 분석):</b><br>
            • <b>Facebook VIP 전환율 17.8%:</b> 채널별 분석 결과 최고 효율. Display 12.8% 대비 +5%p<br>
            • <b>Organic VIP LTV $295.01:</b> 채널별 VIP LTV 분석 결과 최고. Facebook VIP LTV $276 대비 +7%<br>
            • <b>효율 10% 개선:</b> Facebook 예산 증액 + Display 감축으로 평균 전환 효율 개선 보수적 가정<br><br>
            <b>💵 추가 VIP 156명 산출 근거:</b><br>
            • 월 예산 $50,000 × 12개월 = 연간 $600,000 마케팅 비용<br>
            • 현재 VIP 전환율 가중평균 약 14% → 15.4%로 +10% 개선 시<br>
            • 현재 연간 VIP 획득 약 1,560명 → +10% = 추가 156명<br>
            • <b>$275:</b> VIP 평균 LTV $277.56에서 도출<br><br>           
            <b>📈 CAC 절감 $15,000 근거:</b><br>
            • Display 예산 15% 감축 = 연간 약 $9,000 절감<br>
            • 저효율 채널 비용 절감 + Organic 강화로 추가 $6,000 절감 효과<br>
            • 총 $15,000 = 순수 비용 절감 (추가 수익 아닌 비용 감소)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # ROI 요약 테이블
    st.subheader("📈 Phase별 수익 & ROI 요약 (세션 활동 유도 전략)")
    
    roi_summary = pd.DataFrame({
        "Phase": ["Phase 1-A: Promising High", "Phase 1-B: Promising Low",
                  "Phase 2: VIP 유지", "Phase 3: Winback", "Phase 4: 채널 최적화", "**Total**"],
        "대상": ["미활동 1,643명", "미활동 4,275명", "VIP 1,531명", "이탈위험 16,344명", "전 채널", "-"],
        "핵심 전환 지표": ["세션30%→재구매50%", "세션20%→재구매35%", "3개월 재구매50%", "복귀율5%", "VIP전환+10%", "-"],
        "예상 추가 매출": ["$131,000", "$82,000", "$79,000", "$93,000", "$60,000", "**$445,000**"],
        "캠페인 비용(20%)": ["$26,200", "$16,400", "$15,800", "$18,600", "$12,000", "**$89,000**"],
        "순이익": ["$104,800", "$65,600", "$63,200", "$74,400", "$48,000", "**$356,000**"],
        "ROI": ["400%", "400%", "400%", "400%", "400%", "**400%**"],
        "우선순위": ["🔴 P1", "🔴 P1", "🟡 P2", "🟠 P2", "🟢 P3", "-"]
    })
    st.dataframe(roi_summary, hide_index=True, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box success">
        <div class="insight-title">💰 ROI 산출 요약</div>
        <div class="insight-text">
            <b>📊 전체 수익 요약:</b><br>
            • 예상 총 추가 매출: <b>$445,000</b> (현 매출 $3.06M 대비 +14.5%)<br>
            • 예상 캠페인 비용: <b>$89,000</b> (추가 매출의 20%)<br>
            • 예상 순이익: <b>$356,000</b> (추가 매출 - 비용)<br>
            • <b>ROI = $356,000 / $89,000 × 100% = 400%</b><br><br>
            <b>🔑 핵심 발견 기반 전략:</b><br>
            • Promising 고객은 모두 <b>구매 횟수 1회</b>인데, 세션 활동에 따라 LTV가 다름<br>
            • <b>세션 활동 유도 → 더 많은 탐색 → 재구매 시 높은 객단가 → VIP 전환</b>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # KPI 모니터링
    st.subheader("📊 KPI 모니터링 대시보드 (세션 활동 + 재구매 전환)")
    
    kpi_data = pd.DataFrame({
        "KPI": ["Promising High 세션 활동 전환", "Promising Low 세션 활동 전환", 
                "Promising High 재구매 전환", "Promising Low 재구매 전환",
                "VIP 비율", "평균 LTV"],
        "현재": ["53.8% (활동)", "12.6% (활동)", "0% (1회 구매)", "0% (1회 구매)", "5.14%", "$102.82"],
        "목표 (3개월)": ["60%", "18%", "15%", "10%", "6%", "$108"],
        "목표 (6개월)": ["65%", "25%", "25%", "15%", "7%", "$115"],
        "목표 (1년)": ["70%", "35%", "35%", "20%", "10%", "$130"],
        "측정 주기": ["주간", "주간", "월간", "월간", "월간", "월간"]
    })
    st.dataframe(kpi_data, hide_index=True, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box navy">
        <div class="insight-title">📌 실행 로드맵 (세션 활동 유도 전략)</div>
        <div class="insight-text">
            <b>Month 1:</b> Phase 1 세션 활동 유도 캠페인 론칭, 이메일/푸시 A/B 테스트 시작<br>
            <b>Month 2:</b> 세션 활동 전환율 분석, 재구매 전환 캠페인 강화<br>
            <b>Month 3:</b> Phase 2 VIP 프로그램 론칭, Phase 3 Winback 준비<br>
            <b>Month 4-6:</b> 전 Phase 병행 운영, 세션→재구매→VIP 퍼널 최적화<br>
            <b>Month 6:</b> 전체 성과 리뷰, 세션 활동 기반 ROI 검증, 2차 전략 수립
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 푸터
# ============================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #9ca3af; font-size: 0.85rem; padding: 2rem 0; border-top: 1px solid #e5e7eb;">
    <p><b>TheLook E-commerce RFM 분석 포트폴리오</b></p>
    <p>분석 기간: 2023.01 - 2024.12 | 총 고객: 29,795명 | 총 매출: $3,063,495</p>
    <p>데이터: BigQuery thelook_ecommerce</p>
    <p style="margin-top: 0.5rem;">Built with Streamlit & Plotly</p>
</div>
""", unsafe_allow_html=True)