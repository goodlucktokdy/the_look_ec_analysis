"""
TheLook E-commerce RFM 분석 포트폴리오 (Updated)
=====================================
분석 기간: 2023-01-01 ~ 2024-12-31
총 분석 고객: 29,795명
RFM 세그먼트: 9개 (VIP Champions, Loyal High/Low, Promising High/Low, Need Attention, At Risk, Hibernating, Others)
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
    
    /* 메트릭 카드 */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 4px solid;
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    .metric-card.blue { border-color: #667eea; }
    .metric-card.green { border-color: #10b981; }
    .metric-card.orange { border-color: #f59e0b; }
    .metric-card.red { border-color: #ef4444; }
    .metric-card.purple { border-color: #8b5cf6; }
    
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
    
    /* 세그먼트 카드 */
    .segment-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border-top: 4px solid;
    }
    .segment-vip { border-color: #10b981; }
    .segment-loyal-high { border-color: #3b82f6; }
    .segment-loyal-low { border-color: #60a5fa; }
    .segment-promising-high { border-color: #8b5cf6; }
    .segment-promising-low { border-color: #a78bfa; }
    .segment-attention { border-color: #f59e0b; }
    .segment-risk { border-color: #f97316; }
    .segment-hibernating { border-color: #6b7280; }
    
    /* 섹션 디바이더 */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
        margin: 2rem 0;
        border-radius: 1px;
    }
    
    /* 프로세스 플로우 */
    .process-flow {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 2rem 0;
        flex-wrap: wrap;
        gap: 1rem;
    }
    .process-step {
        flex: 1;
        min-width: 120px;
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    .process-number {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 0.75rem;
        font-weight: 600;
    }
    .process-label {
        font-size: 0.85rem;
        color: #4b5563;
        font-weight: 500;
    }
    
    /* 테이블 스타일 */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
    }
    .styled-table th {
        background: #f8fafc;
        padding: 12px 16px;
        text-align: left;
        font-weight: 600;
        color: #374151;
        border-bottom: 2px solid #e5e7eb;
    }
    .styled-table td {
        padding: 12px 16px;
        border-bottom: 1px solid #f3f4f6;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 데이터 정의 (Updated based on new SQL results)
# ============================================

# RFM 세그먼트 데이터 (새 기준)
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

# 채널별 VIP 전환율 데이터
channel_data = pd.DataFrame([
    {"channel": "Facebook", "vip_conversion_rate": 17.80, "promising_high": 218, "promising_low": 290, 
     "vip_count": 110, "avg_monetary_vip": 268.85, "promising_high_share": 35.28, "promising_low_share": 46.93},
    {"channel": "Search", "vip_conversion_rate": 15.37, "promising_high": 2461, "promising_low": 3401,
     "vip_count": 1065, "avg_monetary_vip": 272.92, "promising_high_share": 35.53, "promising_low_share": 49.10},
    {"channel": "Organic", "vip_conversion_rate": 15.06, "promising_high": 563, "promising_low": 734,
     "vip_count": 230, "avg_monetary_vip": 295.01, "promising_high_share": 36.87, "promising_low_share": 48.07},
    {"channel": "Email", "vip_conversion_rate": 14.84, "promising_high": 156, "promising_low": 263,
     "vip_count": 73, "avg_monetary_vip": 262.42, "promising_high_share": 31.71, "promising_low_share": 53.46},
    {"channel": "Display", "vip_conversion_rate": 12.83, "promising_high": 157, "promising_low": 203,
     "vip_count": 53, "avg_monetary_vip": 285.63, "promising_high_share": 38.01, "promising_low_share": 49.15}
])

# 첫 구매 타이밍별 재구매율 및 VIP 전환율
timing_data = pd.DataFrame([
    {"timing": "1주일 이내", "user_count": 307, "repurchase_rate": 26.06, 
     "vip_rate": 10.42, "promising_high_rate": 12.05, "promising_low_rate": 18.89, "avg_monetary": 112.28},
    {"timing": "1개월 이내", "user_count": 901, "repurchase_rate": 25.08, 
     "vip_rate": 9.32, "promising_high_rate": 13.10, "promising_low_rate": 16.98, "avg_monetary": 116.92},
    {"timing": "2개월 이내", "user_count": 1161, "repurchase_rate": 24.63, 
     "vip_rate": 9.47, "promising_high_rate": 12.14, "promising_low_rate": 19.47, "avg_monetary": 110.41},
    {"timing": "3개월 이내", "user_count": 1058, "repurchase_rate": 23.63, 
     "vip_rate": 7.75, "promising_high_rate": 12.00, "promising_low_rate": 18.34, "avg_monetary": 113.97},
    {"timing": "3개월+", "user_count": 26368, "repurchase_rate": 15.79, 
     "vip_rate": 4.64, "promising_high_rate": 11.88, "promising_low_rate": 16.16, "avg_monetary": 101.45}
])

# Promising 구매 후 활동 데이터
promising_high_activity = pd.DataFrame([
    {"activity": "0. No Activity", "user_count": 1643, "pct": 46.22, "avg_monetary": 131.06},
    {"activity": "1. 1 Session", "user_count": 473, "pct": 13.31, "avg_monetary": 153.98},
    {"activity": "2. 2-3 Sessions", "user_count": 1268, "pct": 35.67, "avg_monetary": 176.89},
    {"activity": "3. 4-5 Sessions", "user_count": 170, "pct": 4.78, "avg_monetary": 244.25}
])

promising_low_activity = pd.DataFrame([
    {"activity": "0. No Activity", "user_count": 4275, "pct": 87.41, "avg_monetary": 32.59},
    {"activity": "1. 1 Session", "user_count": 227, "pct": 4.64, "avg_monetary": 44.13},
    {"activity": "2. 2-3 Sessions", "user_count": 384, "pct": 7.85, "avg_monetary": 47.18},
    {"activity": "3. 4-5 Sessions", "user_count": 5, "pct": 0.10, "avg_monetary": 35.21}
])

# VIP 재구매 타이밍
vip_repurchase_timing = pd.DataFrame([
    {"bucket": "1. Within 1 Week", "count": 47, "pct": 3.07, "avg_days": 3.6, "avg_ltv": 303.42},
    {"bucket": "2. Within 2 Weeks", "count": 40, "pct": 2.61, "avg_days": 10.9, "avg_ltv": 277.84},
    {"bucket": "3. Within 1 Month", "count": 78, "pct": 5.09, "avg_days": 22.6, "avg_ltv": 272.28},
    {"bucket": "4. Within 2 Months", "count": 129, "pct": 8.43, "avg_days": 45.5, "avg_ltv": 279.96},
    {"bucket": "5. Within 3 Months", "count": 144, "pct": 9.41, "avg_days": 75.0, "avg_ltv": 269.08},
    {"bucket": "6. 3+ Months", "count": 1093, "pct": 71.39, "avg_days": 299.3, "avg_ltv": 275.30}
])

# VIP 전환 속도별 분석
conversion_speed_data = pd.DataFrame([
    {"conversion_speed": "1. Quick (≤30 days)", "champions_count": 165, "avg_days": 14.4, 
     "avg_sessions": 0.9, "avg_ltv": 282.50, "avg_m_score": 4.35},
    {"conversion_speed": "2. Medium (31-60 days)", "champions_count": 129, "avg_days": 45.5,
     "avg_sessions": 1.1, "avg_ltv": 279.96, "avg_m_score": 4.31},
    {"conversion_speed": "3. Slow (61+ days)", "champions_count": 1237, "avg_days": 273.2,
     "avg_sessions": 1.1, "avg_ltv": 274.58, "avg_m_score": 4.30}
])

# 카테고리별 VIP 전환율 TOP 10
category_vip_conversion = pd.DataFrame([
    {"category": "Clothing Sets", "vip_conversion_pct": 36.36, "avg_first_item_price": 94.00, "avg_total_ltv": 259.81},
    {"category": "Suits", "vip_conversion_pct": 25.00, "avg_first_item_price": 139.13, "avg_total_ltv": 248.88},
    {"category": "Outerwear & Coats", "vip_conversion_pct": 22.46, "avg_first_item_price": 177.41, "avg_total_ltv": 345.31},
    {"category": "Blazers & Jackets", "vip_conversion_pct": 21.56, "avg_first_item_price": 135.05, "avg_total_ltv": 261.14},
    {"category": "Jeans", "vip_conversion_pct": 18.88, "avg_first_item_price": 115.87, "avg_total_ltv": 282.84},
    {"category": "Suits & Sport Coats", "vip_conversion_pct": 17.75, "avg_first_item_price": 123.26, "avg_total_ltv": 280.37},
    {"category": "Jumpsuits & Rompers", "vip_conversion_pct": 17.31, "avg_first_item_price": 47.09, "avg_total_ltv": 215.66},
    {"category": "Accessories", "vip_conversion_pct": 17.17, "avg_first_item_price": 59.15, "avg_total_ltv": 271.72},
    {"category": "Dresses", "vip_conversion_pct": 16.67, "avg_first_item_price": 100.75, "avg_total_ltv": 276.64},
    {"category": "Sweaters", "vip_conversion_pct": 16.50, "avg_first_item_price": 88.76, "avg_total_ltv": 270.27}
])

# ============================================
# 사이드바 네비게이션
# ============================================
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem 0 2rem;">
    <h2 style="color: #667eea; margin-bottom: 0.5rem;">📊 RFM Analysis</h2>
    <p style="color: #6b7280; font-size: 0.9rem;">TheLook E-commerce</p>
</div>
""", unsafe_allow_html=True)

pages = {
    "🏠 Executive Summary": "executive",
    "📐 RFM 등급 설계 & 근거": "rfm_design",
    "👥 세그먼트 분석": "segment",
    "🌱 Promising 전환 분석": "promising",
    "🏆 VIP Champions 분석": "vip",
    "📢 채널 & 카테고리 분석": "channel",
    "🚀 Action Plan & ROI": "action"
}

selected_page = st.sidebar.radio("", list(pages.keys()))

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="padding: 1rem; background: #f8fafc; border-radius: 8px;">
    <p style="font-size: 0.85rem; color: #6b7280; margin-bottom: 0.5rem;">📅 분석 기간</p>
    <p style="font-weight: 600; color: #1f2937;">2023.01 - 2024.12</p>
    <p style="font-size: 0.85rem; color: #6b7280; margin: 1rem 0 0.5rem;">👥 총 고객 수</p>
    <p style="font-weight: 600; color: #1f2937;">29,795명</p>
    <p style="font-size: 0.85rem; color: #6b7280; margin: 1rem 0 0.5rem;">💰 총 매출</p>
    <p style="font-weight: 600; color: #1f2937;">$3,063,495</p>
    <p style="font-size: 0.85rem; color: #6b7280; margin: 1rem 0 0.5rem;">🎯 세그먼트 수</p>
    <p style="font-weight: 600; color: #1f2937;">9개 (신규 기준)</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# 페이지 1: Executive Summary
# ============================================
if pages[selected_page] == "executive":
    st.markdown("""
    <div class="main-header">
        <h1>🏠 Executive Summary</h1>
        <p>TheLook E-commerce RFM 기반 고객 세그먼트 분석 및 전략 제안</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 핵심 지표
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div class="metric-card blue">
            <div class="metric-value">29,795</div>
            <div class="metric-label">분석 고객 수</div>
            <div class="metric-delta delta-positive">2년간 구매 고객</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card green">
            <div class="metric-value">$3.06M</div>
            <div class="metric-label">총 매출</div>
            <div class="metric-delta">sale_price 기준</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card purple">
            <div class="metric-value">5.14%</div>
            <div class="metric-label">VIP Champions</div>
            <div class="metric-delta delta-positive">1,531명 / 매출 13.8%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card orange">
            <div class="metric-value">28.35%</div>
            <div class="metric-label">Promising 전체</div>
            <div class="metric-delta">High 12% + Low 16%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="metric-card red">
            <div class="metric-value">54.86%</div>
            <div class="metric-label">위험군 비중</div>
            <div class="metric-delta delta-negative">At Risk + Hibernating</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 핵심 발견사항
    st.subheader("🔍 핵심 발견사항")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box danger">
            <div class="insight-title">🚨 Critical: Promising Low의 87% 무활동</div>
            <div class="insight-text">
                Promising Low Value 고객 <b>4,891명</b> 중 <b>87.4%(4,275명)</b>이 
                첫 구매 후 어떠한 활동도 없음. 평균 LTV $34.28로 업셀 여지가 큼.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-box warning">
            <div class="insight-title">⚡ Facebook 채널 VIP 전환율 최고 (17.8%)</div>
            <div class="insight-text">
                Facebook 채널의 VIP 전환율 <b>17.8%</b>로 전 채널 중 최고.<br>
                Display(12.8%) 대비 <b>+5%p</b> 높은 전환율 → 채널 투자 재검토 필요.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box success">
            <div class="insight-title">✅ 고가 카테고리 = 높은 VIP 전환</div>
            <div class="insight-text">
                Outerwear & Coats 첫 구매 시 VIP 전환율 <b>22.46%</b>, 평균 LTV <b>$345</b>.<br>
                고가 상품 첫 구매 유도 → VIP 전환 가속화 가능.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-box">
            <div class="insight-title">📊 빠른 재구매 = 높은 LTV</div>
            <div class="insight-text">
                1주 내 재구매 VIP의 평균 LTV는 <b>$303.42</b>,<br>
                3개월+ 재구매 대비 <b>+10.2%</b> 높음. 조기 재구매 유도 필수.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 세그먼트 개요
    st.subheader("👥 고객 세그먼트 분포")
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        fig = px.treemap(
            segment_data,
            path=['segment'],
            values='user_count',
            color='avg_monetary',
            color_continuous_scale='RdYlGn',
            title='세그먼트별 고객 분포 및 평균 LTV'
        )
        fig.update_layout(height=450, margin=dict(t=50, l=0, r=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.pie(
            segment_data,
            values='revenue_pct',
            names='segment',
            title='세그먼트별 매출 기여도',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(height=450)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 우선순위 액션 요약
    st.subheader("🎯 우선순위 액션 요약")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="action-box">
            <div class="action-header">
                <div class="action-icon" style="background: #fee2e2; color: #ef4444;">🔥</div>
                <div class="action-title">P1: Promising 재구매 유도</div>
            </div>
            <div class="action-content">
                <p><b>대상:</b> 8,446명 (Promising High + Low)</p>
                <p><b>목표:</b> 무활동률 87%→60%</p>
                <p><b>예상 ROI:</b> +$180,000/년</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="action-box">
            <div class="action-header">
                <div class="action-icon" style="background: #fef3c7; color: #f59e0b;">⚠️</div>
                <div class="action-title">P2: At Risk 윈백</div>
            </div>
            <div class="action-content">
                <p><b>대상:</b> 6,637명 (22.28%)</p>
                <p><b>목표:</b> 15% 재활성화</p>
                <p><b>예상 ROI:</b> +$85,000/년</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="action-box">
            <div class="action-header">
                <div class="action-icon" style="background: #dbeafe; color: #3b82f6;">📢</div>
                <div class="action-title">P3: Facebook 채널 강화</div>
            </div>
            <div class="action-content">
                <p><b>현황:</b> VIP 전환율 17.8% 최고</p>
                <p><b>목표:</b> 채널 비중 2배 확대</p>
                <p><b>예상 ROI:</b> +$60,000/년</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# 페이지 2: RFM 등급 설계 & 근거
# ============================================
elif pages[selected_page] == "rfm_design":
    st.markdown("""
    <div class="main-header">
        <h1>📐 RFM 등급 설계 & 근거</h1>
        <p>데이터 분포 기반 RFM 스코어링 기준 및 9개 세그먼트 정의 로직</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 데이터 분포 요약
    st.subheader("📊 데이터 분포 분석 (sale_price 기반)")
    
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">💡 분석 기준</div>
        <div class="insight-text">
            Monetary는 <code>orders.num_of_item</code>이 아닌 <code>order_items.sale_price</code>의 
            <b>실제 매출 합계</b>를 사용하여 정확한 고객 가치를 측정했습니다.
            Cancelled, Returned 상태의 주문은 제외했습니다.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="segment-card segment-vip">
            <h4>📅 Recency (최근성)</h4>
            <table class="styled-table" style="margin-top: 1rem;">
                <tr><td>P10</td><td style="text-align:right;"><b>40일</b></td></tr>
                <tr><td>P25</td><td style="text-align:right;"><b>111일</b></td></tr>
                <tr><td>P50 (중앙값)</td><td style="text-align:right;"><b>259일</b></td></tr>
                <tr><td>P75</td><td style="text-align:right;"><b>455일</b></td></tr>
                <tr><td>P90 / P95</td><td style="text-align:right;"><b>610 / 668일</b></td></tr>
                <tr><td>평균 ± 표준편차</td><td style="text-align:right;"><b>293 ± 207일</b></td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="segment-card segment-loyal-high">
            <h4>🔄 Frequency (빈도)</h4>
            <table class="styled-table" style="margin-top: 1rem;">
                <tr><td>P10 ~ P75</td><td style="text-align:right;"><b>1회</b></td></tr>
                <tr><td>P90</td><td style="text-align:right;"><b>2회</b></td></tr>
                <tr><td>P95</td><td style="text-align:right;"><b>2회</b></td></tr>
                <tr><td>최대값</td><td style="text-align:right;"><b>4회</b></td></tr>
                <tr><td>평균 ± 표준편차</td><td style="text-align:right;"><b>1.2 ± 0.47회</b></td></tr>
                <tr><td style="color:#ef4444;">⚠️ 75% 고객</td><td style="text-align:right;"><b>1회 구매</b></td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="segment-card segment-promising-high">
            <h4>💰 Monetary (금액)</h4>
            <table class="styled-table" style="margin-top: 1rem;">
                <tr><td>P10</td><td style="text-align:right;"><b>$18.02</b></td></tr>
                <tr><td>P25</td><td style="text-align:right;"><b>$34.00</b></td></tr>
                <tr><td>P50 (중앙값)</td><td style="text-align:right;"><b>$66.50</b></td></tr>
                <tr><td>P75</td><td style="text-align:right;"><b>$134.72</b></td></tr>
                <tr><td>P90 / P95</td><td style="text-align:right;"><b>$228 / $302</b></td></tr>
                <tr><td>평균 ± 표준편차</td><td style="text-align:right;"><b>$102.82 ± $109.77</b></td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # RFM 스코어 기준
    st.subheader("🎯 RFM 스코어 기준 설정 근거")
    
    st.markdown("""
    <div class="insight-box success">
        <div class="insight-title">💡 스코어링 설계 원칙</div>
        <div class="insight-text">
            <b>1. Recency:</b> 비즈니스 관점의 활동 주기 (90일/180일/365일/545일) 기준으로 5단계 분류<br>
            <b>2. Frequency:</b> 데이터 특성상 75%가 1회 구매 → 2회=재구매 성공, 3회+=충성으로 단순화<br>
            <b>3. Monetary:</b> 분위수 기반 5단계 (P25=$34, P50=$67, P75=$135, P95=$300)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Recency Score")
        r_score_data = pd.DataFrame({
            "점수": [5, 4, 3, 2, 1],
            "기준": ["≤ 90일", "91-180일", "181-365일", "366-545일", "> 545일"],
            "의미": ["활성", "관심", "관망", "이탈위험", "휴면"],
            "비즈니스 로직": ["3개월내 활동", "6개월내 활동", "1년내 활동", "1.5년내 활동", "장기미방문"]
        })
        st.dataframe(r_score_data, hide_index=True, use_container_width=True)
    
    with col2:
        st.markdown("#### Frequency Score")
        f_score_data = pd.DataFrame({
            "점수": [5, 4, 3, 1],
            "기준": ["≥ 3회", "2회", "1회", "0회"],
            "의미": ["충성", "재구매", "신규", "없음"],
            "비즈니스 로직": ["상위 5%", "P90 수준", "대다수(75%)", "미구매"]
        })
        st.dataframe(f_score_data, hide_index=True, use_container_width=True)
    
    with col3:
        st.markdown("#### Monetary Score")
        m_score_data = pd.DataFrame({
            "점수": [5, 4, 3, 2, 1],
            "기준": ["≥ $300", "$135-299", "$67-134", "$34-66", "< $34"],
            "백분위": ["P95+", "P75-P95", "P50-P75", "P25-P50", "P25 미만"],
            "의미": ["VIP", "고가치", "중간", "저가치", "저액"]
        })
        st.dataframe(m_score_data, hide_index=True, use_container_width=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 9개 세그먼트 정의
    st.subheader("👥 9개 세그먼트 정의 로직")
    
    st.code("""
-- RFM 세그먼트 정의 SQL (새 기준)
CASE 
  -- 1) VIP Champions : 최근 + 자주 + 고액
  WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'VIP Champions'
  
  -- 2) Loyal High Value : 자주 + 중~고액
  WHEN r_score >= 3 AND f_score >= 4 AND m_score >= 3 THEN 'Loyal High Value'
  
  -- 3) Loyal Low Value : 자주 사지만 객단가 낮은 단골
  WHEN r_score >= 3 AND f_score >= 4 AND m_score <= 2 THEN 'Loyal Low Value'
  
  -- 4) Promising High Value : 최근 1회 + 중~고액
  WHEN r_score >= 4 AND f_score = 3 AND m_score >= 3 THEN 'Promising High Value'
  
  -- 5) Promising Low Value : 최근 1회 + 저액
  WHEN r_score >= 4 AND f_score = 3 AND m_score <= 2 THEN 'Promising Low Value'
  
  -- 6) Need Attention : 오래 안 오지만 과거에 자주 + 고액
  WHEN r_score <= 2 AND f_score >= 4 AND m_score >= 3 THEN 'Need Attention'
  
  -- 7) At Risk : 이탈 위험 (재구매 X, 최근성 중간)
  WHEN r_score = 3 AND f_score = 3 THEN 'At Risk'
  
  -- 8) Hibernating : 장기 휴면 + 낮은 빈도
  WHEN r_score <= 2 AND f_score <= 3 THEN 'Hibernating'
  
  ELSE 'Others'
END AS customer_segment
    """, language="sql")
    
    st.markdown("#### 세그먼트 정의 매트릭스 (R × F × M)")
    
    matrix_explanation = pd.DataFrame({
        "세그먼트": ["VIP Champions", "Loyal High Value", "Loyal Low Value", "Promising High Value", 
                   "Promising Low Value", "Need Attention", "At Risk", "Hibernating", "Others"],
        "R 조건": ["≥4", "≥3", "≥3", "≥4", "≥4", "≤2", "=3", "≤2", "기타"],
        "F 조건": ["≥4", "≥4", "≥4", "=3", "=3", "≥4", "=3", "≤3", "기타"],
        "M 조건": ["≥4", "≥3", "≤2", "≥3", "≤2", "≥3", "-", "-", "기타"],
        "핵심 특성": ["최상위 고객", "단골+고액", "단골+저액", "신규+고액", "신규+저액", "이탈 고가치", "이탈 위험", "장기 휴면", "예외"],
        "전략": ["VIP 혜택", "유지", "업셀", "재구매 유도", "활성화+업셀", "윈백 우선", "긴급 윈백", "재활성화", "모니터링"]
    })
    st.dataframe(matrix_explanation, hide_index=True, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box warning">
        <div class="insight-title">💡 세그먼트 분리 근거: Promising High vs Low</div>
        <div class="insight-text">
            기존 단일 'Promising' 세그먼트를 <b>M Score 기준</b>으로 분리한 이유:<br>
            • Promising High: 평균 LTV <b>$155.86</b>, 무활동률 <b>46.2%</b> → 재구매만 유도하면 VIP 가능<br>
            • Promising Low: 평균 LTV <b>$34.28</b>, 무활동률 <b>87.4%</b> → 업셀 + 활성화 동시 필요<br>
            → <b>전혀 다른 CRM 전략 필요</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 페이지 3: 세그먼트 분석
# ============================================
elif pages[selected_page] == "segment":
    st.markdown("""
    <div class="main-header">
        <h1>👥 세그먼트 분석</h1>
        <p>9개 고객 세그먼트의 특성, 규모, 매출 기여도 분석</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 세그먼트 개요 시각화
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            segment_data.sort_values('user_count', ascending=True),
            x='user_count',
            y='segment',
            orientation='h',
            color='avg_monetary',
            color_continuous_scale='RdYlGn',
            title='세그먼트별 고객 수 (색상: 평균 LTV)'
        )
        fig.update_layout(height=500, yaxis_title="", xaxis_title="고객 수")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            segment_data.sort_values('revenue_pct', ascending=True),
            x='revenue_pct',
            y='segment',
            orientation='h',
            color='revenue_pct',
            color_continuous_scale='Blues',
            title='세그먼트별 매출 기여도 (%)'
        )
        fig.update_layout(height=500, yaxis_title="", xaxis_title="매출 기여도 (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 세그먼트 상세 테이블
    st.subheader("📋 세그먼트 상세 비교")
    
    display_df = segment_data[['segment', 'user_count', 'pct', 'avg_recency', 'avg_frequency', 
                               'avg_monetary', 'revenue_pct', 'total_revenue']].copy()
    display_df.columns = ['세그먼트', '고객수', '비중(%)', '평균 Recency(일)', '평균 Frequency', 
                          '평균 LTV($)', '매출기여(%)', '총매출($)']
    display_df['총매출($)'] = display_df['총매출($)'].apply(lambda x: f"${x:,.0f}")
    display_df['평균 LTV($)'] = display_df['평균 LTV($)'].apply(lambda x: f"${x:.2f}")
    
    st.dataframe(display_df, hide_index=True, use_container_width=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 인사이트
    st.subheader("💡 핵심 인사이트")
    
    st.markdown("""
    <div class="insight-box danger">
        <div class="insight-title">🚨 문제: 위험군이 전체의 54.86%</div>
        <div class="insight-text">
            At Risk(22.28%) + Hibernating(32.58%) = <b>54.86%</b>의 고객이 이탈 위험 상태.<br>
            이들의 매출 기여도는 <b>45.86%</b>로, 이탈 시 연간 <b>$1.4M</b> 손실 가능성.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="insight-box success">
            <div class="insight-title">✅ 기회: Promising 28.35%가 VIP 후보</div>
            <div class="insight-text">
                Promising High(11.93%) + Low(16.42%) = <b>8,446명</b>이 최근 활동 고객.<br>
                적절한 리텐션 전략으로 VIP 전환 시 <b>+$200,000</b> 추가 매출 가능.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="insight-box warning">
            <div class="insight-title">⚡ 주목: VIP 5.14%가 매출 13.79% 기여</div>
            <div class="insight-text">
                VIP Champions의 평균 LTV <b>$275.88</b>은 전체 평균 대비 <b>2.7배</b>.<br>
                VIP 비중 1%p 증가 시 연간 <b>+$82,000</b> 매출 증가 기대.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# 페이지 4: Promising 전환 분석
# ============================================
elif pages[selected_page] == "promising":
    st.markdown("""
    <div class="main-header">
        <h1>🌱 Promising 전환 분석</h1>
        <p>Promising High/Low Value 고객의 행동 패턴 및 VIP 전환 요인 분석</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Promising High vs Low 비교
    st.subheader("📊 Promising High vs Low 비교")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card purple">
            <div class="metric-value">3,555명</div>
            <div class="metric-label">Promising High Value</div>
            <div class="metric-delta">평균 LTV $155.86</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card orange">
            <div class="metric-value">4,891명</div>
            <div class="metric-label">Promising Low Value</div>
            <div class="metric-delta">평균 LTV $34.28</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card red">
            <div class="metric-value">4.5배</div>
            <div class="metric-label">LTV 격차</div>
            <div class="metric-delta">$155.86 vs $34.28</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 구매 후 활동 분석
    st.subheader("🔍 구매 후 활동 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Promising High Value")
        fig = px.bar(
            promising_high_activity,
            x='activity',
            y='pct',
            color='avg_monetary',
            color_continuous_scale='Greens',
            title='구매 후 활동 수준별 분포 (High Value)',
            labels={'pct': '비중 (%)', 'activity': '활동 수준'}
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box">
            <div class="insight-title">💡 High Value 인사이트</div>
            <div class="insight-text">
                • 무활동 비율: <b>46.22%</b> (상대적으로 낮음)<br>
                • 2-3 Sessions 유저: <b>35.67%</b> → 활발한 편<br>
                • 4-5 Sessions 시 LTV <b>$244.25</b> (무활동 대비 1.86배)
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Promising Low Value")
        fig = px.bar(
            promising_low_activity,
            x='activity',
            y='pct',
            color='avg_monetary',
            color_continuous_scale='Oranges',
            title='구매 후 활동 수준별 분포 (Low Value)',
            labels={'pct': '비중 (%)', 'activity': '활동 수준'}
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box danger">
            <div class="insight-title">🚨 Low Value 문제점</div>
            <div class="insight-text">
                • 무활동 비율: <b>87.41%</b> (심각한 수준)<br>
                • 4-5 Sessions 유저: 단 <b>5명</b> (0.1%)<br>
                • 활동 유저도 LTV 상승 폭이 <b>미미</b> ($32→$47)
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 가입→첫구매 타이밍별 분석
    st.subheader("⏰ 가입→첫구매 타이밍별 VIP 전환율")
    
    fig = make_subplots(rows=1, cols=2, subplot_titles=('재구매율', 'VIP 전환율'))
    
    fig.add_trace(
        go.Bar(x=timing_data['timing'], y=timing_data['repurchase_rate'], 
               name='재구매율', marker_color='#3b82f6'),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(x=timing_data['timing'], y=timing_data['vip_rate'], 
               name='VIP 전환율', marker_color='#10b981'),
        row=1, col=2
    )
    
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box success">
        <div class="insight-title">✅ 핵심 발견: 조기 구매 = 높은 전환율</div>
        <div class="insight-text">
            • 1주일 내 첫 구매 시: 재구매율 <b>26.06%</b>, VIP 전환율 <b>10.42%</b><br>
            • 3개월+ 첫 구매 시: 재구매율 <b>15.79%</b>, VIP 전환율 <b>4.64%</b><br>
            • <b>결론:</b> 가입 후 빠른 첫 구매 유도가 VIP 전환의 핵심
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 페이지 5: VIP Champions 분석
# ============================================
elif pages[selected_page] == "vip":
    st.markdown("""
    <div class="main-header">
        <h1>🏆 VIP Champions 분석</h1>
        <p>VIP Champions 고객의 행동 패턴, 재구매 주기, LTV 극대화 전략</p>
    </div>
    """, unsafe_allow_html=True)
    
    # VIP 핵심 지표
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card green">
            <div class="metric-value">1,531명</div>
            <div class="metric-label">VIP Champions</div>
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

# ============================================
# 페이지 6: 채널 & 카테고리 분석
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
        fig.update_layout(height=400)
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
    fig.update_layout(height=500, yaxis={'categoryorder':'total ascending'})
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
# 페이지 7: Action Plan & ROI
# ============================================
elif pages[selected_page] == "action":
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Action Plan & ROI</h1>
        <p>세그먼트별 구체적 액션플랜 및 예상 ROI 산출</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 전체 ROI 요약
    st.subheader("💰 전체 예상 ROI 요약")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card green">
            <div class="metric-value">$420,000</div>
            <div class="metric-label">예상 총 ROI (Gross)</div>
            <div class="metric-delta delta-positive">현 매출 대비 +13.7%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card blue">
            <div class="metric-value">$336,000</div>
            <div class="metric-label">예상 총 ROI (Net)</div>
            <div class="metric-delta">캠페인 비용 20% 제외</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card purple">
            <div class="metric-value">4개</div>
            <div class="metric-label">핵심 이니셔티브</div>
            <div class="metric-delta">단계별 실행</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # ROI 요약 테이블
    st.subheader("📈 Phase별 ROI 요약")
    
    roi_summary = pd.DataFrame({
        "Phase": ["Phase 1: Promising 리텐션", "Phase 2: VIP 유지", "Phase 3: Winback", "Phase 4: 채널 최적화", "Total"],
        "대상 고객": ["8,446명", "1,531명", "16,344명", "전 채널", "-"],
        "Gross ROI": ["$188,000", "$79,000", "$93,000", "$60,000", "$420,000"],
        "Net ROI": ["$150,400", "$63,200", "$74,400", "$48,000", "$336,000"],
        "우선순위": ["🔴 P1", "🟡 P2", "🟠 P2", "🟢 P3", "-"]
    })
    st.dataframe(roi_summary, hide_index=True, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box success">
        <div class="insight-title">💰 예상 총 ROI</div>
        <div class="insight-text">
            • Gross ROI: <b>$420,000</b> (현 매출 $3.06M 대비 +13.7%)<br>
            • Net ROI: <b>$336,000</b> (캠페인 비용 20% 제외)<br>
            • 가장 높은 ROI: <b>Phase 1 Promising 리텐션</b> ($188,000)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # KPI 모니터링
    st.subheader("📊 KPI 모니터링 대시보드")
    
    kpi_data = pd.DataFrame({
        "KPI": ["Promising 무활동률", "VIP Champions 비율", "평균 LTV", "재구매율", "At Risk 비율"],
        "현재": ["66.77%", "5.14%", "$102.82", "~17%", "22.28%"],
        "목표 (6개월)": ["50%", "7%", "$115", "22%", "18%"],
        "목표 (1년)": ["40%", "10%", "$130", "28%", "15%"]
    })
    st.dataframe(kpi_data, hide_index=True, use_container_width=True)

# ============================================
# 푸터
# ============================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #9ca3af; font-size: 0.85rem; padding: 2rem 0; border-top: 1px solid #e5e7eb;">
    <p>TheLook E-commerce RFM 분석 포트폴리오 (Updated Version)</p>
    <p>분석 기간: 2023.01 - 2024.12 | 데이터: BigQuery thelook_ecommerce</p>
    <p>세그먼트: 9개 (VIP Champions, Loyal High/Low, Promising High/Low, Need Attention, At Risk, Hibernating, Others)</p>
    <p style="margin-top: 0.5rem;">Built with Streamlit & Plotly</p>
</div>
""", unsafe_allow_html=True)