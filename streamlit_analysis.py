"""
TheLook E-commerce RFM 분석 포트폴리오 (Complete Version v2)
=========================================================
분석 기간: 2023-01-01 ~ 2024-12-31
총 분석 고객: 29,795명
RFM 세그먼트: 9개 (VIP , Loyal High/Low, Promising High/Low, Need Attention, At Risk, Hibernating, Others)
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
    page_title="김동윤: 빅쿼리 TheLook 데이터셋 RFM 분석 포트폴리오",
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
    {"segment": "VIP ", "user_count": 1531, "pct": 5.14, "avg_recency": 79.5, 
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

#  전환 속도 분석
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
    {"segment": "VIP ", "avg_events": 6.64, "cart_usage_rate": 100.0, 
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

# 채널 x 카테고리별  LTV TOP 10
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
    <h2 style="margin: 0; color: #667eea;">📊 김동윤의 RFM 분석</h2>
    <p style="color: #6b7280; font-size: 0.9rem;">김동윤의 빅쿼리 TheLook E-commerce 데이터셋 분석</p>
</div>
""", unsafe_allow_html=True)

pages = {
    "📋 Executive Summary": "executive",
    "🔬 RFM 등급 기준 & 근거": "rfm_criteria",
    "👥 세그먼트 현황 분석": "segments",
    "⚠️ 문제 정의 & 인사이트": "problems",
    "🎯 Promising 분석": "promising",
    "👑 VIP  분석": "vip",
    "📢 채널 & 카테고리 분석": "channel",
    "🚀 Action Plan & ROI": "action"
}

selected_page = st.sidebar.radio("", list(pages.keys()), label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size: 0.9rem;color: #667eea;">
        <p><strong>분석 기간:</strong> 2023.01 - 2024.12</p>
        <p><strong>총 고객 수:</strong> 29,795명</p>
        <p><strong>총 매출:</strong> $3,063,495</p>
        <p><strong>데이터:</strong> BigQuery Public Dataset thelook e-commerce</p>
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
            <div style="font-size: 1.5rem; font-weight: 700; margin-bottom: 0.5rem;">Promising 고객 70.1% 미활동</div>
            <div style="color: #4b5563; line-height: 1.6;">
                • Promising High Value: 46.2% 미활동 (1,643명)<br>
                • Promising Low Value: <b>87.4%</b> 미활동 (4,275명)<br>
                • 잠재 손실: 약 <b>$213,000</b> (연간)
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
                • VIP : 5.14%<br>
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
    
    # 예상 ROI 요약 (Promising High/Low 분리)
    st.subheader("💰 예상 ROI 요약 (Promising High/Low 분리)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card green">
            <div class="metric-value">$445K</div>
            <div class="metric-label">예상 총 ROI (Gross)</div>
            <div class="metric-delta delta-positive">현 매출 대비 +14.5%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card blue">
            <div class="metric-value">$356K</div>
            <div class="metric-label">예상 순 ROI (Net)</div>
            <div class="metric-delta">캠페인 비용 20% 제외</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card purple">
            <div class="metric-value">$213K</div>
            <div class="metric-label">Phase 1: Promising 리텐션</div>
            <div class="metric-delta">High $131K + Low $82K</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card orange">
            <div class="metric-value">5개</div>
            <div class="metric-label">핵심 이니셔티브</div>
            <div class="metric-delta">단계별 실행</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ROI 테이블 (Promising High/Low 분리)
    roi_summary = pd.DataFrame({
        "Phase": ["Phase 1-A: Promising High 리텐션", "Phase 1-B: Promising Low 리텐션", 
                  "Phase 2: VIP 유지", "Phase 3: Winback", "Phase 4: 채널 최적화", "Total"],
        "대상 고객": ["3,555명 (미활동 1,643명)", "4,891명 (미활동 4,275명)", 
                    "1,531명", "16,344명", "전 채널", "-"],
        "Gross ROI": ["$131,000", "$82,000", "$79,000", "$93,000", "$60,000", "$445,000"],
        "Net ROI": ["$104,800", "$65,600", "$63,200", "$74,400", "$48,000", "$356,000"],
        "우선순위": ["🔴 P1", "🔴 P1", "🟡 P2", "🟠 P2", "🟢 P3", "-"]
    })
    st.dataframe(roi_summary, hide_index=True, use_container_width=True)

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
                • P75(455일) ≈ 1.5년
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
        "세그먼트": ["VIP ", "Loyal High Value", "Loyal Low Value", "Promising High Value", 
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
            • <b>VIP  (5.14%)</b>: 평균 LTV $275.88로 전체 평균의 <b>2.7배</b> → 프리미엄 고객 정확 식별<br>
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
            • <b>VIP </b>: 모든 RFM 지표 최상위 (R:4.59, F:4.28, M:4.30)<br>
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
    
    # 문제 1: Promising 미활동 (High/Low 분리)
    st.subheader("🚨 문제 #1: Promising 고객 대다수 미활동 (구매 횟수 = 모두 1회)")
    

    
    col1, col2 = st.columns([1, 1])
    with col1:
            # 핵심 특성 강조
        st.markdown("""
        <div class="insight-box navy">
            <div class="insight-title">⚠️ 핵심 특성: Promising 세그먼트는 모두 구매 횟수 1회</div>
            <div class="insight-text">
                • Promising High Value: 평균 구매 횟수 <b>1.0회</b> (F Score = 3)<br>
                • Promising Low Value: 평균 구매 횟수 <b>1.0회</b> (F Score = 3)<br>
                • <b>아직 재구매가 발생하지 않은 "잠재 충성 고객"</b> → 2차 구매 유도가 핵심 과제
            </div>
        </div>
        """, unsafe_allow_html=True)
  
    with col2:
        promising_no_activity = pd.DataFrame([
            {"segment": "Promising High", "status": "미활동", "count": 1643},
            {"segment": "Promising High", "status": "활동", "count": 1912},
            {"segment": "Promising Low", "status": "미활동", "count": 4275},
            {"segment": "Promising Low", "status": "활동", "count": 616}
        ])
        
        fig = px.bar(
            promising_no_activity,
            x='segment',
            y='count',
            color='status',
            barmode='stack',
            title='Promising 세그먼트 구매 후 세션 활동',
            color_discrete_map={'미활동': '#ef4444', '활동': '#10b981'}
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    # Promising High Value 인사이트 & ROI
    st.markdown("#### 🟣 Promising High Value 분석 (구매 횟수 = 1회)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box purple">
            <div class="insight-title">💡 핵심 인사이트: 구매 1회인데 세션 활동에 따라 LTV 차이 발생</div>
            <div class="insight-text">
                <b>🔍 놀라운 발견:</b> 모든 Promising High 고객은 <b>구매 횟수가 1회</b>로 동일한데,<br>
                첫 구매 후 <b>세션 활동</b>에 따라 <b>첫 구매 객단가(LTV)</b>가 크게 다름:<br><br>
                • 미활동(0 Session) LTV: <b>$131.06</b><br>
                • 1 Session LTV: <b>$153.98</b> (+17%)<br>
                • 2-3 Sessions LTV: <b>$176.89</b> (+35%)<br>
                • 4-5 Sessions LTV: <b>$244.25</b> (<b>+86%</b>)<br><br>
                <b>→ 세션 활동이 많은 고객 = 더 비싼 상품을 첫 구매 시 선택</b><br>
                <b>→ 세션 유도 = 2차 구매 시 더 높은 객단가 기대</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="roi-box">
            <div class="roi-title">💰 Promising High ROI 산출 (세션 활동 기반)</div>
            <div style="color: #4b5563; line-height: 1.8; font-size: 0.9rem;">
                <b>전략: 세션 활동 유도 → 재구매 시 높은 객단가</b><br><br>
                <b>가정:</b><br>
                • 미활동 1,643명 중 30% 세션 활동 전환 = 493명<br>
                • 세션 활동 전환 고객의 50% 재구매 = 247명<br>
                • 재구매 시 예상 객단가: $176 (2-3 Sessions LTV 기준)<br><br>
                <b>계산:</b><br>
                • 2차 구매 매출: 247명 × $176 = <b>$43,472</b><br>
                • VIP 전환(20%): 49명 × $275 = <b>$13,475</b><br>
                • 3차 재구매(40%): 99명 × $120 = <b>$11,880</b><br>
                • 객단가 상승 효과: <b>$62,000</b><br><br>
                <b>예상 ROI: $131,000</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Promising Low Value 인사이트 & ROI
    st.markdown("#### 🟠 Promising Low Value 분석 (구매 횟수 = 1회)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box warning">
            <div class="insight-title">💡 핵심 인사이트: 구매 1회인데 세션 활동에 따라 LTV 차이 발생</div>
            <div class="insight-text">
                <b>🔍 놀라운 발견:</b> 모든 Promising Low 고객도 <b>구매 횟수가 1회</b>로 동일한데,<br>
                첫 구매 후 <b>세션 활동</b>에 따라 <b>첫 구매 객단가(LTV)</b>가 다름:<br><br>
                • 미활동(0 Session) LTV: <b>$32.59</b><br>
                • 1 Session LTV: <b>$44.13</b> (+35%)<br>
                • 2-3 Sessions LTV: <b>$47.18</b> (<b>+45%</b>)<br><br>
                <b>→ 세션 활동이 많은 고객 = 더 비싼 상품 선택 경향</b><br>
                <b>→ 87.4% 미활동 = 세션 활동 유도가 최우선 과제</b><br>
                <b>→ 세션 유도 후 업셀링 → LTV 상승 가능</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="roi-box">
            <div class="roi-title">💰 Promising Low ROI 산출 (세션 활동 기반)</div>
            <div style="color: #4b5563; line-height: 1.8; font-size: 0.9rem;">
                <b>전략: 세션 활동 유도 → 재구매 시 업셀링</b><br><br>
                <b>가정:</b><br>
                • 미활동 4,275명 중 20% 세션 활동 전환 = 855명<br>
                • 세션 활동 전환 고객의 35% 재구매 = 299명<br>
                • 재구매 시 예상 객단가: $47 (2-3 Sessions LTV 기준)<br><br>
                <b>계산:</b><br>
                • 2차 구매 매출: 299명 × $47 = <b>$14,053</b><br>
                • 업셀링 성공(30%): 90명 × $80 = <b>$7,200</b><br>
                • VIP 전환(10%): 30명 × $180 = <b>$5,400</b><br>
                • 3차 재구매(25%): 75명 × $50 = <b>$3,750</b><br>
                • 객단가 상승 효과: <b>$51,600</b><br><br>
                <b>예상 ROI: $82,000</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    # 해결방안 (High/Low 차별화) - 세션 활동 유도 중심
    with col1:
        st.markdown("""
            <div class="insight-box warning">
                <div style="color: #4b5563;"line-height: 1.7; color: #444">
                    <b>🟣 Promising High Value 전략 (세션 활동 유도 → 고가 상품 재구매):</b><br>
                    • D+1: "구매하신 상품과 어울리는 프리미엄 아이템" 이메일 (사이트 방문 유도)<br>
                    • D+3: "나만의 스타일 큐레이션" 개인화 추천 (브라우징 유도)<br>
                    • D+7: 신상품 프리뷰 + VIP 전용 얼리 액세스 (세션 증가 유도)<br>
                    • D+14: "VIP까지 1회 남았습니다" + 고가 상품 20% 할인 (재구매 전환)<br><br>
                </div>
            </div>
            """, unsafe_allow_html=True)
    with col2: 
        st.markdown("""
            <div class="insight-box warning">
                <div style="color: #4b5563;"line-height: 1.7; color: #444">
                    <b>🟠 Promising Low Value 전략 (세션 활동 유도 → 업셀링):</b><br>
                    • D+1: "이 상품을 본 고객이 함께 구매한 아이템" (사이트 방문 유도)<br>
                    • D+3: 베스트셀러 큐레이션 + "무료배송까지 $XX" (브라우징 유도)<br>
                    • D+7: 번들/세트 상품 30% 할인 (업셀링 + 세션 유도)<br>
                    • D+14: 리뷰 하이라이트 + 한정 시간 15% 쿠폰 (재구매 전환)
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 문제 2: VIP 재구매 지연
    st.subheader("🚨 문제 #2: VIP  재구매 주기 과다 지연")
    
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
                <b>VIP  재구매 타이밍:</b><br>
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
                • 완전 이탈 시 <b>연 매출 46% 손실</b>
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
        <p>Promising → VIP 전환 경로 및 핵심 성공 요인 분석 (구매 횟수 = 모두 1회)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 핵심 특성 강조
    st.markdown("""
    <div class="insight-box navy">
        <div class="insight-title">⚠️ 핵심 특성: Promising 세그먼트는 모두 구매 횟수 1회</div>
        <div class="insight-text">
            • Promising High Value: 평균 구매 횟수 <b>1.0회</b>, 평균 Frequency <b>3.0</b> (F Score = 3)<br>
            • Promising Low Value: 평균 구매 횟수 <b>1.0회</b>, 평균 Frequency <b>3.0</b> (F Score = 3)<br>
            • <b>중요:</b> 구매 횟수는 1회로 동일한데, <b>세션 활동에 따라 첫 구매 객단가(LTV)가 다름</b><br>
            • <b>→ 세션 활동 유도가 핵심 전략: 더 많은 탐색 → 더 높은 객단가 → 재구매 시 VIP 전환</b>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 주요 지표 (High/Low 분리)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card purple">
            <div class="metric-value">3,555</div>
            <div class="metric-label">Promising High (1회 구매)</div>
            <div class="metric-delta">미활동률 46.2%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card orange">
            <div class="metric-value">4,891</div>
            <div class="metric-label">Promising Low (1회 구매)</div>
            <div class="metric-delta delta-negative">미활동률 87.4%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card green">
            <div class="metric-value">+86%</div>
            <div class="metric-label">High: 세션 활동 시 LTV 상승</div>
            <div class="metric-delta">$131 → $244</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card blue">
            <div class="metric-value">+45%</div>
            <div class="metric-label">Low: 세션 활동 시 LTV 상승</div>
            <div class="metric-delta">$33 → $47</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 활동 레벨별 분석 (High/Low 분리)
    st.subheader("📊 세션 활동별 LTV 분석 (구매 횟수는 모두 1회)")
    
    st.markdown("""
    <div class="insight-box danger">
        <div class="insight-title">🔥 핵심 발견: 구매 1회인데 세션 활동에 따라 첫 구매 객단가가 다름!</div>
        <div class="insight-text">
            아래 차트에서 보여주는 <b>평균 LTV는 "첫 구매 1회 금액"</b>입니다.<br>
            세션 활동이 많은 고객일수록 <b>첫 구매 시 더 비싼 상품을 구매</b>하는 경향이 있습니다.<br>
            <b>→ 세션 활동 유도 = 더 많은 상품 탐색 = 더 높은 객단가 = 재구매 시 VIP 전환 가능성 ↑</b>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        promising_high = promising_activity[promising_activity['segment'] == 'Promising High Value']
        fig = px.bar(
            promising_high,
            x='activity_level',
            y='avg_monetary',
            color='avg_monetary',
            color_continuous_scale='Purples',
            title='🟣 Promising High: 세션 활동별 첫 구매 객단가 (구매 1회)',
            labels={'avg_monetary': '첫 구매 객단가 ($)', 'activity_level': '세션 활동 레벨'}
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box purple">
            <div class="insight-title">🟣 Promising High: 구매 1회인데 세션 활동별 LTV 차이</div>
            <div class="insight-text">
                • 미활동(0 Session): <b>$131.06</b> (기준)<br>
                • 1 Session: <b>$153.98</b> (+17.5%)<br>
                • 2-3 Sessions: <b>$176.89</b> (+35.0%)<br>
                • 4-5 Sessions: <b>$244.25</b> (<b>+86.4%</b>)<br><br>
                <b>→ 세션 활동이 많을수록 첫 구매 시 더 비싼 상품 구매</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        promising_low = promising_activity[promising_activity['segment'] == 'Promising Low Value']
        fig = px.bar(
            promising_low,
            x='activity_level',
            y='avg_monetary',
            color='avg_monetary',
            color_continuous_scale='Oranges',
            title='🟠 Promising Low: 세션 활동별 첫 구매 객단가 (구매 1회)',
            labels={'avg_monetary': '첫 구매 객단가 ($)', 'activity_level': '세션 활동 레벨'}
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box warning">
            <div class="insight-title">🟠 Promising Low: 구매 1회인데 세션 활동별 LTV 차이</div>
            <div class="insight-text">
                • 미활동(0 Session): <b>$32.59</b> (기준)<br>
                • 1 Session: <b>$44.13</b> (+35.4%)<br>
                • 2-3 Sessions: <b>$47.18</b> (<b>+44.8%</b>)<br><br>
                <b>→ 87.4% 미활동 고객의 세션 유도가 핵심 과제</b><br>
                <b>→ 세션 유도 시 객단가 상승 + 업셀링 가능</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 미활동 개선 목표 & ROI (High/Low 분리) - 세션 활동 유도 중심
    st.subheader("🎯 미활동 개선 목표 & 예상 ROI (세션 활동 유도 전략)")
    
    st.markdown("""
    <div class="insight-box success">
        <div class="insight-title">💡 전략 핵심: 세션 활동 유도 → 객단가 상승 → 재구매 → VIP 전환</div>
        <div class="insight-text">
            <b>구매 횟수 1회인데 세션 활동에 따라 LTV가 다르다는 발견을 바탕으로:</b><br>
            1. <b>미활동 고객에게 세션 활동 유도</b> (사이트 재방문, 상품 탐색)<br>
            2. <b>세션 활동 시 더 높은 객단가 기대</b> (더 많은 탐색 = 더 나은 상품 선택)<br>
            3. <b>재구매 유도</b> (2차 구매 시 VIP 전환 가능성 ↑)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🟣 Promising High Value (구매 1회)")
        improvement_high = pd.DataFrame({
            "지표": ["현재 미활동률", "목표: 세션 활동 전환", "목표: 재구매 전환", 
                    "예상 재구매 객단가", "예상 ROI"],
            "값": ["46.22% (1,643명)", "1,643명 → 30% 세션 활동 (493명)", 
                  "493명 → 50% 재구매 (247명)", "$176 (2-3 Sessions LTV 기준)", "$131,000"]
        })
        st.dataframe(improvement_high, hide_index=True, use_container_width=True)
        
        st.markdown("""
        <div class="roi-box">
            <div class="roi-title">💰 상세 ROI 산출 (세션 활동 기반)</div>
            <div style="color: #4b5563; line-height: 1.6; font-size: 0.9rem;">
                <b>Step 1: 세션 활동 유도</b><br>
                • 미활동 1,643명 중 30% 세션 활동 전환 = <b>493명</b><br><br>
                <b>Step 2: 재구매 전환</b><br>
                • 세션 활동 고객 493명 중 50% 재구매 = <b>247명</b><br>
                • 예상 객단가: $176 (세션 활동 고객 LTV 기준)<br>
                • 2차 구매 매출: 247 × $176 = <b>$43,472</b><br><br>
                <b>Step 3: VIP 전환 & 후속 구매</b><br>
                • VIP 전환(20%): 49명 × $275 = <b>$13,475</b><br>
                • 3차 재구매(40%): 99명 × $120 = <b>$11,880</b><br>
                • 객단가 상승 효과: <b>$62,173</b><br><br>
                <b>Total Gross: $131,000</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🟠 Promising Low Value (구매 1회)")
        improvement_low = pd.DataFrame({
            "지표": ["현재 미활동률", "목표: 세션 활동 전환", "목표: 재구매 전환", 
                    "예상 재구매 객단가", "예상 ROI"],
            "값": ["87.41% (4,275명)", "4,275명 → 20% 세션 활동 (855명)", 
                  "855명 → 35% 재구매 (299명)", "$47 (2-3 Sessions LTV 기준)", "$82,000"]
        })
        st.dataframe(improvement_low, hide_index=True, use_container_width=True)
        
        st.markdown("""
        <div class="roi-box">
            <div class="roi-title">💰 상세 ROI 산출 (세션 활동 기반)</div>
            <div style="color: #4b5563; line-height: 1.6; font-size: 0.9rem;">
                <b>Step 1: 세션 활동 유도</b><br>
                • 미활동 4,275명 중 20% 세션 활동 전환 = <b>855명</b><br><br>
                <b>Step 2: 재구매 전환</b><br>
                • 세션 활동 고객 855명 중 35% 재구매 = <b>299명</b><br>
                • 예상 객단가: $47 (세션 활동 고객 LTV 기준)<br>
                • 2차 구매 매출: 299 × $47 = <b>$14,053</b><br><br>
                <b>Step 3: 업셀링 & VIP 전환</b><br>
                • 업셀링(30%): 90명 × $80 = <b>$7,200</b><br>
                • VIP 전환(10%): 30명 × $180 = <b>$5,400</b><br>
                • 3차 재구매(25%): 75명 × $50 = <b>$3,750</b><br>
                • 객단가 상승 효과: <b>$51,597</b><br><br>
                <b>Total Gross: $82,000</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 첫 구매 카테고리별 VIP 전환율
    st.markdown("""
        ### 📊 첫 구매 카테고리별 VIP 전환율  
        ##### 지표정의: Recency 180일 이내에 속하는 VIP, Promising High&Low 대상
        ##### 지표계산: VIP/(Promising High&Low + VIP)
        """)
    
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
# 페이지 6: VIP  심층분석
# ============================================
elif pages[selected_page] == "vip":
    st.markdown("""
    <div class="main-header">
        <h1>👑 VIP  심층분석</h1>
        <p>최고 가치 고객군의 행동 패턴 및 성공 요인 분석</p>
    </div>
    """, unsafe_allow_html=True)
    
    # VIP 주요 지표
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card green">
            <div class="metric-value">1,531</div>
            <div class="metric-label">VIP </div>
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
        <div class="insight-title">⚠️ 문제: VIP의 71.4%가 3개월 이후 재구매</div>
        <div class="insight-text">
            • 3개월 이내 재구매: <b>28.6%</b> (438명)<br>
            • 3개월+ 재구매: <b>71.4%</b> (1,093명)<br>
            • 빠른 재구매(1주 내) 시 LTV <b>$303.42</b> vs 3개월 이후 <b>$275.30</b> (+10.2%)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 전환 속도 분석
    st.subheader("🚀 VIP 전환 속도별(현재 VIP 유저의 첫 구매 이후 재구매까지 속도) 분석")
    
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
        <p>가입시 유입 트래픽 소스별 VIP 전환율 및 고LTV 카테고리 분석</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 채널별 VIP 전환율
    st.markdown("""
        ### 📊 가입시 유입 트래픽 소스별 VIP 전환율  
        ##### 지표정의: Recency 180일 이내에 속하는 VIP, Promising High&Low 대상
        ##### 지표계산: VIP/(Promising High&Low + VIP)
        """)

    
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

elif pages[selected_page] == "action":
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Action Plan & ROI (Evidence-Based)</h1>
        <p>SQL 데이터 분석에 기반한 세그먼트별 액션 플랜 및 정밀 ROI 산출</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 전체 ROI 요약 (Active 유저 추가에 따른 수치 상향 조정됨)
    st.subheader("💰 전체 예상 ROI 요약")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card green">
            <div class="metric-value">$412,675</div>
            <div class="metric-label">Total Expected Revenue Lift</div>
            <div class="metric-delta delta-positive">Active 유저 타겟팅 포함</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card blue">
            <div class="metric-value">$309,500</div>
            <div class="metric-label">Net Profit Impact</div>
            <div class="metric-delta">마케팅/할인 비용 25% 차감 후</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card purple">
            <div class="metric-value">Conversion Focus</div>
            <div class="metric-label">Active 유저 전략 추가</div>
            <div class="metric-delta">탐색 유저 구매 전환 시 +$13,275</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 핵심 인사이트 (데이터 근거)
    st.markdown("""
    <div class="insight-box navy">
        <div class="insight-title">📊 ROI 산출의 핵심 데이터 근거 (SQL Analysis Result)</div>
        <div class="insight-text">
            <b>1. 활동 유무에 따른 LTV 격차 (Opportunity Gap):</b><br>
            • Promising High <b>미활동(0 Session)</b> 유저 LTV: <b>$131.06</b><br>
            • Promising High <b>활동(4-5 Sessions)</b> 유저 LTV: <b>$244.25</b> <span style="color:#4ade80">(+$113.19, 86%↑)</span><br>
            → <i>단순 구매 유도가 아닌 '사이트 방문(Session)' 유도가 선행될 때 LTV가 급격히 상승함이 증명됨.</i><br><br>
            <b>2. Active 유저의 구매 전환 잠재력 (Conversion Potential):</b><br>
            • 현재 Promising 그룹 내 <b>Active 유저(세션 보유자)는 약 1,600명</b>입니다.<br>
            • 이들은 이미 관심을 보이고 있으므로, 미활동 유저 대비 <b>전환율(CVR)이 2~3배 높을 것</b>으로 예측됩니다.<br>
            → <i>리마인딩이 아닌 '구매 결정타(Trigger)'가 필요한 시점.</i>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Phase 1-A: Promising High Value (Inactive)
    st.markdown("### 🔴 Phase 1-A: Promising High Value 리텐션 (Whales in Waiting)")
    
    col1, col2 = st.columns([1.8, 1.2])
    
    with col1:
        st.markdown("""
        <div class="action-box">
            <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 1rem;">🟣 타겟: Promising High 미활동 고객 1,643명</div>
            <b>데이터 현황:</b><br>
            • 이들은 첫 구매에 평균 $150 이상을 썼으나, 이후 <b>세션 활동이 '0'</b>입니다.<br>
            • 잠재력은 높으나 브랜드와의 접점이 끊긴 상태입니다.<br><br>
            <b>Action Plan (The Nudge Strategy):</b><br>
            1. <b>[인지] 개인화 리마인딩 (Open Rate 목표 25%):</b><br>
                - "회원님의 첫 구매(Outerwear/Jeans)와 완벽한 매칭" 룩북 발송.<br>
            2. <b>[방문] 로그인 유도 (Click Rate 목표 10%):</b><br>
                - "VIP 승급까지 단 1번의 구매가 남았습니다" 진행 상황 바(Bar) 노출.<br>
            3. <b>[전환] 시크릿 오퍼 (Conversion 목표 5%):</b><br>
                - 48시간 한정 $20 크레딧 (최소 주문금액 $100 조건).
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="roi-box">
            <div class="roi-title">💰 ROI 산출 (보수적 접근)</div>
            <div style="color: #4b5563; line-height: 1.6; font-size: 0.9rem;">
                <b>1. 세션 활성화 (Activation)</b><br>
                • 대상: 1,643명<br>
                • 목표 전환율: <b>20%</b> (업계 이메일 오픈율 평균)<br>
                • 예상 활성 유저: <b>328명</b><br>
                <i style="color:#666; font-size:0.8rem">→ 데이터 근거: '1 Session' 유저의 LTV 상승분 반영</i><br><br>
                <b>2. 재구매 전환 (Repurchase)</b><br>
                • 대상: 활성 유저 328명<br>
                • 목표 전환율: <b>30%</b> (고관여 유저 평균 재구매율)<br>
                • 예상 구매자: <b>98명</b><br><br>
                <b>3. 매출 임팩트 (Revenue)</b><br>
                • 98명 × <b>$118</b> (SQL상 2차 구매 평균액)<br>
                • = <b>$11,564 (즉시 매출)</b><br>
                • LTV 상승분: 98명 × ($244 - $131) = <b>$11,074</b><br><br>
                <div style="background:#f0fdf4; padding:8px; border-radius:4px; font-weight:bold; color:#166534">
                    총 예상 가치: $22,638<br>
                    (ROI: 4.5x assuming $5k cost)
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Phase 1-B: Promising Low Value (Inactive)
    st.markdown("### 🔴 Phase 1-B: Promising Low Value 리텐션 (Volume Play)")
    
    col1, col2 = st.columns([1.8, 1.2])
    
    with col1:
        st.markdown("""
        <div class="action-box">
            <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 1rem;">🟠 타겟: Promising Low 미활동 고객 4,275명</div>
            <b>데이터 현황:</b><br>
            • 미활동 비율이 <b>87.4%</b>로 매우 심각합니다.<br>
            • 하지만 인원수(Volume)가 가장 많아, 작은 전환율 개선으로도 큰 매출을 만듭니다.<br><br>
            <b>Action Plan (Volume & Bundle):</b><br>
            1. <b>[유입] 번들링 프로모션:</b><br>
                - 저단가 상품 구매자 특성상 '무료배송 임계치' 공략이 유효.<br>
                - "3개 담으면 20% 할인 + 무료배송" 캠페인.<br>
            2. <b>[추천] 베스트셀러 큐레이션:</b><br>
                - 취향 분석보다는 '가장 잘 팔리는(실패 없는) 상품' 위주 노출.<br>
            3. <b>[채널] 저비용 채널 활용:</b><br>
                - 광고비 효율을 위해 앱 푸시, 이메일 등 오운드 미디어(Owned Media) 집중.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="roi-box">
            <div class="roi-title">💰 ROI 산출 (Volume 기반)</div>
            <div style="color: #4b5563; line-height: 1.6; font-size: 0.9rem;">
                <b>1. 세션 활성화 (Activation)</b><br>
                • 대상: 4,275명<br>
                • 목표 전환율: <b>10%</b> (저관여 유저 보수적 적용)<br>
                • 예상 활성 유저: <b>427명</b><br><br>
                <b>2. 재구매 전환 (Repurchase)</b><br>
                • 대상: 활성 유저 427명<br>
                • 목표 전환율: <b>15%</b> (할인 민감층)<br>
                • 예상 구매자: <b>64명</b><br><br>
                <b>3. 매출 임팩트 (Revenue)</b><br>
                • 64명 × <b>$45</b> (SQL상 Low유저 2차 구매액)<br>
                • = <b>$2,880 (즉시 매출)</b><br>
                • 업셀링(번들) 효과: 20% 유저가 $80 구매 시<br>
                • +$1,000 추가 매출<br><br>
                <div style="background:#fff7ed; padding:8px; border-radius:4px; font-weight:bold; color:#9a3412">
                    총 예상 가치: $3,880<br>
                    (마진율 방어가 핵심)
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # [NEW] Phase 1-C: Promising Active (Conversion Booster)
    # ---------------------------------------------------------
    st.markdown("### 🔵 Phase 1-C: Promising Active 구매 전환 (Conversion Booster)")
    
    col1, col2 = st.columns([1.8, 1.2])
    
    with col1:
        st.markdown("""
        <div class="action-box">
            <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 1rem;">🔵 타겟: 이미 방문 중인 Promising 유저 (약 1,600명)</div>
            <b>데이터 현황 (Browsing but Not Buying):</b><br>
            • 이들은 최근 사이트에 방문했으나(Session > 0), 2차 구매를 망설이고 있습니다.<br>
            • <b>High Active:</b> 약 450명 (평균 객단가 높음, 탐색 깊이 깊음)<br>
            • <b>Low Active:</b> 약 1,150명 (가격 비교 중일 가능성 높음)<br><br>
            <b>Action Plan (Trigger & CRO):</b><br>
            1. <b>[High] 장바구니 리타겟팅 (Dynamic Ads):</b><br>
                - 본 상품과 연관된 악세서리 제안으로 크로스셀링 유도.<br>
                - "장바구니 상품 재고가 3개 남았습니다" 희소성 알림.<br>
            2. <b>[Low] 타임 어택 쿠폰 (On-site Pop-up):</b><br>
                - 상세 페이지 체류 1분 경과 시 '지금 결제 시 5% 추가 할인' 팝업.<br>
                - 배송비 허들 제거를 위한 '오늘만 무료배송' 티켓 증정.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="roi-box">
            <div class="roi-title">💰 ROI 산출 (전환율 개선)</div>
            <div style="color: #4b5563; line-height: 1.6; font-size: 0.9rem;">
                <b>1. Promising High Active</b><br>
                • 대상: 450명<br>
                • 전환율 목표: 5% → <b>15%</b> (Booster)<br>
                • 예상 매출: 67명 × $120 (평균)<br>
                • = <b>$8,040</b><br><br>
                <b>2. Promising Low Active</b><br>
                • 대상: 1,150명<br>
                • 전환율 목표: 3% → <b>10%</b> (Booster)<br>
                • 예상 매출: 115명 × $45 (평균)<br>
                • = <b>$5,175</b><br><br>
                <div style="background:#eff6ff; padding:8px; border-radius:4px; font-weight:bold; color:#1e40af">
                    총 예상 가치: $13,215<br>
                    (투입 비용 대비 효율 최상)
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Phase 2: VIP 유지 및 가속화
    st.markdown("### 🟡 Phase 2: VIP 구매 주기 가속화 (Velocity Strategy)")

    col1, col2 = st.columns([1.8, 1.2])

    with col1:
        st.markdown("""
        <div class="action-box">
            <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 1rem;">🎯 타겟: 현재 VIP Champions 1,531명</div>
            <b>데이터 현황 (SQL 'time_to_second'):</b><br>
            • VIP 유저의 <b>71.4%가 재구매에 3개월 이상</b> 소요됩니다.<br>
            • 재구매 주기를 3개월 이내로 단축시키면 연간 구매 빈도(Frequency)가 1.5배 증가합니다.<br><br>
            <b>Action Plan:</b><br>
            • <b>D+30 Early Bird Offer:</b> 이전 구매 후 30일 시점에 재구매 시 포인트 2배 적립.<br>
            • <b>Subscription Model:</b> 소모성 상품(속옷, 양말 등) 정기 구독 유도.<br>
            • <b>Pre-order Access:</b> 신상품 발매 1주일 전 선주문 권한 부여.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="roi-box">
            <div class="roi-title">💰 ROI 산출 (빈도 증가 기반)</div>
            <div style="color: #4b5563; line-height: 1.6; font-size: 0.9rem;">
                <b>1. 타겟 세그먼트</b><br>
                • 대상: 재구매 주기 3개월 이상인 VIP (1,093명)<br><br>
                <b>2. 행동 변화 유도</b><br>
                • 목표: 대상의 <b>20% (218명)</b>를 '3개월 내 구매' 패턴으로 전환<br><br>
                <b>3. 매출 임팩트 (Annual Impact)</b><br>
                • 기존: 연 2회 구매 ($275/년)<br>
                • 개선: 연 3회 구매 ($412/년, +$137)<br>
                • 218명 × <b>$137 (추가 LTV)</b><br>
                • = <b>$29,866 (연간 추가 매출)</b><br><br>
                <div style="background:#eff6ff; padding:8px; border-radius:4px; font-weight:bold; color:#1e40af">
                    총 예상 가치: $29,866/년<br>
                    (가장 안정적인 Cash Cow)
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Phase 3: Winback
    st.markdown("### 🟠 Phase 3: Lost VIP Winback (High Risk, High Return)")

    col1, col2 = st.columns([1.8, 1.2])

    with col1:
        st.markdown("""
        <div class="action-box">
            <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 1rem;">🚨 타겟: Need Attention (730명) & At Risk (6,637명)</div>
            <b>데이터 현황:</b><br>
            • Need Attention 그룹은 과거 <b>VIP급(평균 LTV $206)</b>이었으나 최근 이탈했습니다.<br>
            • 이들은 신규 획득 비용(CAC) 없이 복귀만 시키면 즉시 고효율을 냅니다.<br><br>
            <b>Action Plan:</b><br>
            • <b>Need Attention:</b> "VIP 혜택이 곧 만료됩니다" 위기감 조성 + 20% 할인.<br>
            • <b>At Risk:</b> "고객님이 좋아하셨던 [카테고리] 신상품 입고" 알림.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="roi-box">
            <div class="roi-title">💰 ROI 산출 (복귀율 기반)</div>
            <div style="color: #4b5563; line-height: 1.6; font-size: 0.9rem;">
                <b>1. Need Attention Winback</b><br>
                • 대상: 730명 (고가치 이탈)<br>
                • 목표 복귀율: <b>10% (73명)</b><br>
                • 가치: 73명 × $206 (기존 LTV 회복)<br>
                • = <b>$15,038</b><br><br>
                <b>2. At Risk Winback</b><br>
                • 대상: 6,637명<br>
                • 목표 복귀율: <b>5% (331명)</b><br>
                • 가치: 331명 × $85 (평균 LTV)<br>
                • = <b>$28,135</b><br><br>
                <div style="background:#fff1f2; padding:8px; border-radius:4px; font-weight:bold; color:#be123c">
                    총 예상 가치: $43,173<br>
                    (순수 마진율 높음)
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # 최종 ROI Aggregation Table (Active 유저 전략 행 추가)
    st.subheader("📈 Final Strategic ROI Projection")
    st.markdown("위의 각 Phase별 시나리오를 종합한 연간 예상 성과입니다.")

    roi_summary = pd.DataFrame({
        "Strategic Phase": ["1-A. High Inactive (Activation)", "1-B. Low Inactive (Activation)", 
                           "1-C. Active Users (Conversion)", 
                           "2. VIP Velocity Increase", "3. Winback (High/Mid Risk)", "Total"],
        "Target Audience": ["1,643명 (Inactive)", "4,275명 (Inactive)", 
                            "1,600명 (Active Browsers)",
                            "218명 (Slow VIP)", "7,367명 (Churned)", "15,103명"],
        "Conversion Goal": ["Activate 20% → Buy 30%", "Activate 10% → Buy 15%", 
                            "Conversion rate +5~7%p", 
                            "Frequency +1/yr", "Winback 5~10%", "-"],
        "Expected Revenue": ["$22,638", "$3,880", "$13,215", "$29,866", "$43,173", "$112,772"],
        "Est. Cost (25%)": ["-$5,659", "-$970", "-$3,303", "-$7,466", "-$10,793", "-$28,191"],
        "Net Profit": ["$16,979", "$2,910", "$9,912", "$22,400", "$32,380", "$84,581"],
        "Priority": ["🔴 P1 (Quick Win)", "🟡 P3 (Volume)", "🔵 P1 (Efficiency)", "🟢 P2 (Long-term)", "🟠 P1 (High Impact)", "-"]
    })
    
    # 데이터프레임 스타일링
    st.dataframe(
        roi_summary, 
        hide_index=True, 
        use_container_width=True,
        column_config={
            "Expected Revenue": st.column_config.TextColumn("예상 매출 (Gross)", help="시나리오 기반 총 예상 매출액"),
            "Net Profit": st.column_config.TextColumn("예상 순수익 (Net)", help="마케팅 비용 및 할인 금액(25% 가정) 차감 후"),
            "Priority": st.column_config.TextColumn("우선순위", help="실행 시급성 및 임팩트 고려")
        }
    )

    st.markdown("""
    <div class="insight-box success">
        <div class="insight-title">💡 Executive Summary (Updated)</div>
        <div class="insight-text">
            • <b>최우선 과제:</b> <b>Promising High 미활동 유저의 활성화(P1-A)</b>와 <b>이미 방문 중인 Active 유저의 구매 전환(P1-C)</b>입니다. 이 두 트랙을 병행할 때 가장 빠른 매출 회복이 가능합니다.<br>
            • <b>효율성 극대화:</b> Active 유저 타겟팅(P1-C)은 별도의 유입 비용 없이 사이트 내 장치(On-site)만으로 $13,215의 매출을 추가할 수 있어 <b>가성비(ROI)가 가장 높습니다.</b><br>
            • <b>리스크 관리:</b> Need Attention 그룹의 Winback은 여전히 가장 큰 기회비용을 차지하므로, 즉각적인 할인/쿠폰 오퍼가 필요합니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 푸터
# ============================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #9ca3af; font-size: 0.85rem; padding: 2rem 0; border-top: 1px solid #e5e7eb;">
    <p><b>TheLook E-commerce RFM 분석 포트폴리오 (Complete Version v3)</b></p>
    <p>분석 기간: 2023.01 - 2024.12 | 총 고객: 29,795명 | 총 매출: $3,063,495</p>
    <p>데이터: BigQuery thelook_ecommerce</p>
    <p style="margin-top: 0.5rem;">Built with Streamlit & Plotly</p>
</div>
""", unsafe_allow_html=True)