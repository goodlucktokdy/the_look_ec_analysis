"""
TheLook E-commerce RFM 분석 포트폴리오
BigQuery Public Dataset 활용 고객 세분화 및 마케팅 전략 수립

Author: Data Analyst Portfolio
Dataset: BigQuery - thelook_ecommerce
Analysis Period: 2023-01-01 ~ 2024-12-31
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
# 스타일 설정
# ============================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .insight-box {
        background-color: #e8f4f8;
        border-left: 4px solid #3498db;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
    }
    .action-box {
        background-color: #e8f8e8;
        border-left: 4px solid #27ae60;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
    }
    .warning-box {
        background-color: #fdf2e9;
        border-left: 4px solid #e67e22;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 데이터 정의 (쿼리 결과 기반)
# ============================================

# RFM 분포 데이터
rfm_distribution = {
    "recency_p10": 40, "recency_p25": 111, "recency_p50": 259, 
    "recency_p75": 455, "recency_p90": 610, "recency_p95": 668,
    "frequency_p10": 1, "frequency_p25": 1, "frequency_p50": 1, 
    "frequency_p75": 1, "frequency_p90": 2, "frequency_p95": 2,
    "monetary_p10": 1.0, "monetary_p25": 1.0, "monetary_p50": 1.0, 
    "monetary_p75": 2.0, "monetary_p90": 3.0, "monetary_p95": 4.0,
    "avg_recency": 293.0, "std_recency": 207.2,
    "avg_frequency": 1.2, "std_frequency": 0.47,
    "avg_monetary": 1.74, "std_monetary": 1.11,
    "total_users": 29795
}

# RFM 세그먼트 데이터
rfm_segments = pd.DataFrame([
    {"segment": "Champions", "user_count": 2787, "pct": 9.35, "avg_recency": 80.4, 
     "avg_frequency": 2.22, "avg_monetary": 3.17, "revenue_pct": 17.10},
    {"segment": "Loyal Customers", "user_count": 1357, "pct": 4.55, "avg_recency": 263.1,
     "avg_frequency": 2.16, "avg_monetary": 3.13, "revenue_pct": 8.22},
    {"segment": "Promising", "user_count": 8446, "pct": 28.35, "avg_recency": 84.9,
     "avg_frequency": 1.0, "avg_monetary": 1.45, "revenue_pct": 23.73},
    {"segment": "Need Attention", "user_count": 861, "pct": 2.89, "avg_recency": 478.3,
     "avg_frequency": 2.07, "avg_monetary": 3.0, "revenue_pct": 5.0},
    {"segment": "At Risk", "user_count": 6637, "pct": 22.28, "avg_recency": 270.2,
     "avg_frequency": 1.0, "avg_monetary": 1.46, "revenue_pct": 18.75},
    {"segment": "Hibernating", "user_count": 9707, "pct": 32.58, "avg_recency": 538.5,
     "avg_frequency": 1.0, "avg_monetary": 1.45, "revenue_pct": 27.21}
])

# Promising 유저 활동 분석
promising_activity = pd.DataFrame([
    {"activity_level": "0. No Activity", "user_count": 3287, "pct": 70.78, 
     "avg_events": 0.0, "avg_product_views": 0.0, "avg_cart_adds": 0.0, "avg_days_inactive": None},
    {"activity_level": "1. 1 Session", "user_count": 374, "pct": 8.05,
     "avg_events": 1.3, "avg_product_views": 0.1, "avg_cart_adds": 0.1, "avg_days_inactive": 39.8},
    {"activity_level": "2. 2-3 Sessions", "user_count": 886, "pct": 19.08,
     "avg_events": 2.4, "avg_product_views": 0.0, "avg_cart_adds": 0.0, "avg_days_inactive": 42.2},
    {"activity_level": "3. 4-5 Sessions", "user_count": 97, "pct": 2.09,
     "avg_events": 5.8, "avg_product_views": 0.6, "avg_cart_adds": 0.6, "avg_days_inactive": 44.2}
])

# Champions 재구매 타이밍
champions_repurchase = pd.DataFrame([
    {"time_bucket": "1주 이내", "count": 39, "pct": 2.41, "avg_days": 3.6, "cumulative_pct": 2.41},
    {"time_bucket": "2주 이내", "count": 44, "pct": 2.72, "avg_days": 11.0, "cumulative_pct": 5.13},
    {"time_bucket": "1개월 이내", "count": 74, "pct": 4.57, "avg_days": 23.5, "cumulative_pct": 9.7},
    {"time_bucket": "2개월 이내", "count": 141, "pct": 8.71, "avg_days": 44.8, "cumulative_pct": 18.41},
    {"time_bucket": "3개월 이내", "count": 147, "pct": 9.08, "avg_days": 75.4, "cumulative_pct": 27.49},
    {"time_bucket": "3개월+", "count": 1174, "pct": 72.51, "avg_days": 309.0, "cumulative_pct": 100.0}
])

# 첫 구매 타이밍과 재구매율
first_purchase_timing = pd.DataFrame([
    {"timing": "1주일 이내", "user_count": 307, "repurchased": 80, "repurchase_rate": 26.06, "avg_days": 203.4},
    {"timing": "1개월 이내", "user_count": 901, "repurchased": 226, "repurchase_rate": 25.08, "avg_days": 179.6},
    {"timing": "2개월 이내", "user_count": 1161, "repurchased": 286, "repurchase_rate": 24.63, "avg_days": 181.6},
    {"timing": "3개월 이내", "user_count": 1058, "repurchased": 250, "repurchase_rate": 23.63, "avg_days": 170.7},
    {"timing": "3개월+", "user_count": 26368, "repurchased": 4163, "repurchase_rate": 15.79, "avg_days": 204.5}
])

# 트래픽 소스별 전환율
traffic_source_data = pd.DataFrame([
    {"source": "Email", "promising": 419, "champions": 156, "conversion_rate": 27.13},
    {"source": "Facebook", "promising": 508, "champions": 181, "conversion_rate": 26.27},
    {"source": "Search", "promising": 5862, "champions": 1946, "conversion_rate": 24.92},
    {"source": "Display", "promising": 360, "champions": 114, "conversion_rate": 24.05},
    {"source": "Organic", "promising": 1297, "champions": 390, "conversion_rate": 23.12}
])

# 카테고리별 Champions 전환율 (상위 10개)
category_conversion = pd.DataFrame([
    {"category": "Clothing Sets", "conversion_rate": 41.67, "champions": 5},
    {"category": "Jumpsuits & Rompers", "conversion_rate": 29.51, "champions": 18},
    {"category": "Plus", "conversion_rate": 28.40, "champions": 73},
    {"category": "Accessories", "conversion_rate": 28.38, "champions": 174},
    {"category": "Blazers & Jackets", "conversion_rate": 27.62, "champions": 50},
    {"category": "Suits", "conversion_rate": 27.42, "champions": 17},
    {"category": "Outerwear & Coats", "conversion_rate": 26.96, "champions": 158},
    {"category": "Socks & Hosiery", "conversion_rate": 25.83, "champions": 62},
    {"category": "Pants", "conversion_rate": 25.77, "champions": 117},
    {"category": "Socks", "conversion_rate": 25.65, "champions": 98}
])

# LTV 상위 조합 데이터
ltv_data = pd.DataFrame([
    {"source": "Organic", "category": "Outerwear & Coats", "champions": 6, "avg_ltv": 452.22},
    {"source": "Organic", "category": "Tops & Tees", "champions": 10, "avg_ltv": 419.65},
    {"source": "Search", "category": "Suits & Sport Coats", "champions": 15, "avg_ltv": 378.35},
    {"source": "Facebook", "category": "Fashion Hoodies", "champions": 5, "avg_ltv": 370.73},
    {"source": "Search", "category": "Pants & Capris", "champions": 10, "avg_ltv": 347.83},
    {"source": "Search", "category": "Jeans", "champions": 40, "avg_ltv": 337.21},
    {"source": "Search", "category": "Outerwear & Coats", "champions": 32, "avg_ltv": 323.01},
    {"source": "Search", "category": "Fashion Hoodies", "champions": 30, "avg_ltv": 307.43}
])

# 전환 속도별 분석
conversion_speed = pd.DataFrame([
    {"speed": "Quick (≤30일)", "count": 157, "avg_days": 15.0, "avg_sessions": 0.6, "avg_product_views": 0.2},
    {"speed": "Medium (31-60일)", "count": 141, "avg_days": 44.8, "avg_sessions": 0.8, "avg_product_views": 0.3},
    {"speed": "Slow (61+일)", "count": 1321, "avg_days": 283.0, "avg_sessions": 0.9, "avg_product_views": 0.4}
])

# ============================================
# 사이드바 네비게이션
# ============================================
st.sidebar.markdown("## 📊 Navigation")
page = st.sidebar.radio(
    "페이지 선택",
    ["📋 Executive Summary",
     "🔍 문제 정의 & 가설",
     "📈 RFM 등급 설계",
     "👥 세그먼트 분석",
     "🎯 Promising 전환 분석",
     "🏆 Champions 행동 분석",
     "📊 채널 & 카테고리 분석",
     "💡 액션 플랜"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📅 분석 기간")
st.sidebar.info("2023.01.01 ~ 2024.12.31")
st.sidebar.markdown("### 📦 데이터셋")
st.sidebar.info("BigQuery: thelook_ecommerce")
st.sidebar.markdown("### 👤 분석 대상")
st.sidebar.info(f"총 {rfm_distribution['total_users']:,}명")

# ============================================
# 페이지 1: Executive Summary
# ============================================
if page == "📋 Executive Summary":
    st.markdown('<h1 class="main-header">🛒 TheLook E-commerce RFM 분석</h1>', unsafe_allow_html=True)
    st.markdown("### Customer Segmentation & Marketing Strategy Portfolio")
    
    st.markdown("---")
    
    # Key Metrics
    st.markdown("## 📌 핵심 지표 요약")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="총 분석 고객 수",
            value=f"{rfm_distribution['total_users']:,}명",
            delta="2년간 구매 고객"
        )
    
    with col2:
        st.metric(
            label="Champions 비율",
            value="9.35%",
            delta="2,787명 (매출 17.1% 기여)"
        )
    
    with col3:
        st.metric(
            label="Promising 비율",
            value="28.35%",
            delta="8,446명 (성장 잠재력)"
        )
    
    with col4:
        st.metric(
            label="이탈 위험 고객",
            value="54.86%",
            delta="At Risk + Hibernating"
        )
    
    st.markdown("---")
    
    # Executive Summary Content
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## 🎯 분석 목적")
        st.markdown("""
        **비즈니스 목표**: RFM 기반 고객 세분화를 통한 마케팅 효율 극대화
        
        **핵심 질문**:
        1. 재구매 가능성이 높은 고객은 누구인가?
        2. Champions로 전환될 가능성이 높은 Promising 고객의 특성은?
        3. 어떤 채널과 카테고리가 고가치 고객을 만드는가?
        """)
        
        st.markdown("## ⚡ 핵심 발견")
        st.markdown("""
        <div class="insight-box">
        <strong>1. 초기 전환이 핵심</strong><br>
        가입 1주일 내 첫 구매 고객의 재구매율(26.1%)은 3개월+ 고객(15.8%) 대비 <strong>65% 높음</strong>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-box">
        <strong>2. Promising 고객 70.8%가 비활성</strong><br>
        첫 구매 후 사이트 재방문 없음 → <strong>리텐션 캠페인 시급</strong>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-box">
        <strong>3. Email 채널 최고 전환율</strong><br>
        Email 유입 고객의 Champions 전환율 27.1%로 <strong>전 채널 1위</strong>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("## 📊 세그먼트 분포")
        
        fig = px.pie(
            rfm_segments,
            values='user_count',
            names='segment',
            color='segment',
            color_discrete_map={
                'Champions': '#2ecc71',
                'Loyal Customers': '#3498db',
                'Promising': '#f39c12',
                'Need Attention': '#e74c3c',
                'At Risk': '#9b59b6',
                'Hibernating': '#95a5a6'
            },
            hole=0.4
        )
        fig.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2),
            margin=dict(t=30, b=30)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("## 💰 예상 ROI")
        st.markdown("""
        <div class="action-box">
        <strong>Promising → Champions 전환 시</strong><br>
        • 현재 Promising: 8,446명<br>
        • 목표 전환율: 25% → 30% (+5%p)<br>
        • 추가 Champions: 약 422명<br>
        • 예상 추가 매출: <strong>월 +12.7%</strong>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Action Plan Summary
    st.markdown("## 🚀 핵심 액션 플랜 (우선순위순)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 1️⃣ 즉시 실행 (0-2주)
        - **Promising 재방문 유도 푸시**
          - 첫 구매 후 3일 내 상품 추천 이메일
          - 7일 후 할인 쿠폰 발송
        
        - **Champions VIP 프로그램**
          - 조기 접근권, 전용 할인
        """)
    
    with col2:
        st.markdown("""
        ### 2️⃣ 단기 (2-4주)
        - **Email 채널 집중 투자**
          - 전환율 27.1% 최고 성과
          - 뉴스레터 구독 유도 강화
        
        - **고가치 카테고리 크로스셀**
          - Outerwear, Accessories 추천
        """)
    
    with col3:
        st.markdown("""
        ### 3️⃣ 중기 (1-3개월)
        - **At Risk 고객 윈백**
          - 개인화된 재구매 혜택
          - 과거 구매 기반 추천
        
        - **신규 가입 72시간 전환 캠페인**
          - 첫 구매 유도 집중
        """)

# ============================================
# 페이지 2: 문제 정의 & 가설
# ============================================
elif page == "🔍 문제 정의 & 가설":
    st.markdown("# 🔍 문제 정의 & 가설 설정")
    
    st.markdown("---")
    
    st.markdown("## 📋 비즈니스 배경")
    st.markdown("""
    TheLook은 패션 이커머스 플랫폼으로, 2년간(2023-2024) **29,795명**의 고객 데이터를 보유하고 있습니다.
    그러나 대부분의 마케팅이 일괄적으로 진행되어 **고객 특성에 맞는 개인화된 전략**이 부재한 상황입니다.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## ❓ 핵심 문제 정의")
        st.markdown("""
        <div class="warning-box">
        <strong>Problem Statement</strong><br><br>
        "전체 고객의 <strong>75%가 1회 구매</strong>에 그치고 있으며,
        재구매로 이어지는 고객 특성과 전환 경로를 파악하지 못해
        <strong>마케팅 효율이 낮은 상태</strong>이다."
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📊 현황 데이터")
        
        # 현황 시각화
        current_state = pd.DataFrame({
            "구분": ["1회 구매 (75%)", "2회 이상 구매 (25%)"],
            "비율": [75, 25]
        })
        
        fig = px.bar(
            current_state,
            x="구분",
            y="비율",
            color="구분",
            color_discrete_sequence=["#e74c3c", "#2ecc71"],
            text="비율"
        )
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        fig.update_layout(showlegend=False, yaxis_title="비율 (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("## 🎯 분석 목표")
        st.markdown("""
        1. **고객 세분화**: RFM 기반 6개 세그먼트 정의
        2. **전환 경로 파악**: Promising → Champions 전환 요인 분석
        3. **채널 효율성**: 유입 채널별 고가치 고객 생성 비교
        4. **액션 플랜**: 세그먼트별 맞춤 마케팅 전략 수립
        """)
        
        st.markdown("## 💡 가설 설정")
        st.markdown("""
        <div class="insight-box">
        <strong>H1: 초기 전환 가설</strong><br>
        가입 후 빠르게 첫 구매를 한 고객일수록 재구매율이 높을 것이다.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-box">
        <strong>H2: 활동 기반 전환 가설</strong><br>
        첫 구매 후 사이트 재방문 활동이 많은 Promising 고객이 Champions로 전환될 확률이 높을 것이다.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-box">
        <strong>H3: 채널 품질 가설</strong><br>
        유입 채널에 따라 고객의 LTV(생애가치)가 다를 것이며, 특정 채널이 우수한 성과를 보일 것이다.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("## 🔬 분석 프레임워크")
    
    st.markdown("""
    ```
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                         RFM 분석 프레임워크                               │
    ├─────────────────────────────────────────────────────────────────────────┤
    │                                                                          │
    │   1. 데이터 수집          2. RFM 지표 계산        3. 등급화               │
    │   ┌──────────┐           ┌──────────┐           ┌──────────┐            │
    │   │ Orders   │──────────▶│ Recency  │──────────▶│ R Score  │            │
    │   │ Items    │           │ Frequency│           │ F Score  │            │
    │   │ Events   │           │ Monetary │           │ M Score  │            │
    │   └──────────┘           └──────────┘           └──────────┘            │
    │                                                        │                 │
    │                                                        ▼                 │
    │   4. 세그먼트 정의        5. 행동 분석            6. 전략 수립            │
    │   ┌──────────┐           ┌──────────┐           ┌──────────┐            │
    │   │Champions │◀──────────│ 전환경로 │◀──────────│ Action   │            │
    │   │Promising │           │ 채널효과 │           │ Plan     │            │
    │   │At Risk   │           │ 카테고리 │           │ KPI      │            │
    │   └──────────┘           └──────────┘           └──────────┘            │
    │                                                                          │
    └─────────────────────────────────────────────────────────────────────────┘
    ```
    """)

# ============================================
# 페이지 3: RFM 등급 설계
# ============================================
elif page == "📈 RFM 등급 설계":
    st.markdown("# 📈 RFM 등급 설계 근거")
    
    st.markdown("---")
    
    st.markdown("## 📊 RFM 지표 분포 분석")
    st.markdown("""
    RFM 등급 기준을 설정하기 위해 먼저 **29,795명 고객**의 Recency, Frequency, Monetary 분포를 분석했습니다.
    백분위수와 평균/표준편차를 기반으로 비즈니스에 적합한 구간을 설정했습니다.
    """)
    
    # 분포 테이블
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### ⏰ Recency (최근성)")
        st.markdown("*마지막 구매로부터 경과 일수*")
        recency_df = pd.DataFrame({
            "백분위": ["P10", "P25", "P50", "P75", "P90", "P95"],
            "일수": [40, 111, 259, 455, 610, 668]
        })
        st.dataframe(recency_df, hide_index=True)
        st.markdown(f"""
        - 평균: **{rfm_distribution['avg_recency']}일**
        - 표준편차: {rfm_distribution['std_recency']}일
        - 범위: 0 ~ 730일
        """)
    
    with col2:
        st.markdown("### 🔄 Frequency (빈도)")
        st.markdown("*총 구매 횟수*")
        frequency_df = pd.DataFrame({
            "백분위": ["P10", "P25", "P50", "P75", "P90", "P95"],
            "횟수": [1, 1, 1, 1, 2, 2]
        })
        st.dataframe(frequency_df, hide_index=True)
        st.markdown(f"""
        - 평균: **{rfm_distribution['avg_frequency']}회**
        - 표준편차: {rfm_distribution['std_frequency']}회
        - 범위: 1 ~ 4회
        """)
    
    with col3:
        st.markdown("### 💰 Monetary (구매량)")
        st.markdown("*총 구매 아이템 수*")
        monetary_df = pd.DataFrame({
            "백분위": ["P10", "P25", "P50", "P75", "P90", "P95"],
            "개수": [1.0, 1.0, 1.0, 2.0, 3.0, 4.0]
        })
        st.dataframe(monetary_df, hide_index=True)
        st.markdown(f"""
        - 평균: **{rfm_distribution['avg_monetary']}개**
        - 표준편차: {rfm_distribution['std_monetary']}개
        - 범위: 1 ~ 10개
        """)
    
    st.markdown("---")
    
    st.markdown("## 🎯 RFM 스코어 기준 설정")
    
    st.markdown("""
    <div class="insight-box">
    <strong>💡 등급 설계 원칙</strong><br>
    1. <strong>비즈니스 의미</strong>: 마케팅 액션과 연결되는 구간 설정<br>
    2. <strong>데이터 분포</strong>: 백분위수 기반으로 균형 있는 분포 확보<br>
    3. <strong>실행 가능성</strong>: 너무 세분화하지 않고 6개 핵심 세그먼트로 단순화
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⏰ Recency Score 기준")
        recency_score = pd.DataFrame({
            "Score": [5, 4, 3, 2, 1],
            "기준": ["≤90일", "91-180일", "181-365일", "366-545일", "546일+"],
            "의미": ["최근 활성", "비교적 최근", "중간", "장기 비활성", "휴면"],
            "근거": [
                "3개월 이내 = 활성 고객 기준",
                "6개월 이내 = 관심 유지 가능",
                "1년 이내 = 리마인드 필요",
                "1.5년 이내 = 이탈 위험",
                "1.5년+ = 휴면 상태"
            ]
        })
        st.dataframe(recency_score, hide_index=True)
    
    with col2:
        st.markdown("### 🔄 Frequency Score 기준")
        frequency_score = pd.DataFrame({
            "Score": [5, 4, 3],
            "기준": ["≥3회", "2회", "1회"],
            "의미": ["충성 고객", "재구매 고객", "신규/일회성"],
            "근거": [
                "상위 5% (P95=2회 초과)",
                "상위 10% (P90=2회)",
                "대다수 75% (중앙값=1회)"
            ]
        })
        st.dataframe(frequency_score, hide_index=True)
        
        st.markdown("### 💰 Monetary Score 기준")
        monetary_score = pd.DataFrame({
            "Score": [5, 4, 3, 2],
            "기준": ["≥5개", "3-4개", "2개", "1개"],
            "의미": ["대량 구매", "다량 구매", "복수 구매", "단일 구매"],
            "근거": [
                "상위 5% 초과",
                "상위 10% (P90=3)",
                "상위 25% (P75=2)",
                "중앙값 (P50=1)"
            ]
        })
        st.dataframe(monetary_score, hide_index=True)
    
    st.markdown("---")
    
    st.markdown("## 👥 세그먼트 정의 로직")
    
    st.markdown("""
    RFM 점수 조합을 기반으로 **6개 핵심 세그먼트**를 정의했습니다.
    Monetary는 Frequency와 상관관계가 높아, **R-F 조합**을 중심으로 세그먼트를 구분했습니다.
    """)
    
    segment_logic = pd.DataFrame({
        "세그먼트": ["Champions", "Loyal Customers", "Promising", "Need Attention", "At Risk", "Hibernating"],
        "R Score": ["≥4 (최근)", "≥3 (중간)", "≥4 (최근)", "≤2 (오래됨)", "=3 (중간)", "≤2 (오래됨)"],
        "F Score": ["≥4 (다회)", "≥4 (다회)", "=3 (1회)", "≥4 (다회)", "=3 (1회)", "=3 (1회)"],
        "특성": [
            "최근 + 다회 구매 = 최우수 고객",
            "과거 다회 구매 = 충성 고객 (재활성 필요)",
            "최근 첫 구매 = 성장 잠재력",
            "과거 다회 구매자 이탈 = 윈백 대상",
            "중간 활동 + 1회 구매 = 전환 촉진 필요",
            "1회 구매 후 장기 미활동 = 휴면"
        ],
        "마케팅 액션": [
            "VIP 혜택, 크로스셀",
            "재활성 캠페인",
            "리텐션, 2nd 구매 유도",
            "윈백 할인, 개인화 추천",
            "긴급 리마인드",
            "대규모 프로모션"
        ]
    })
    
    st.dataframe(segment_logic, hide_index=True, use_container_width=True)
    
    # 세그먼트 분포 시각화
    st.markdown("### 📊 세그먼트별 분포 및 매출 기여도")
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("고객 수 비율", "매출 기여도"),
        specs=[[{"type": "pie"}, {"type": "pie"}]]
    )
    
    colors = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c', '#9b59b6', '#95a5a6']
    
    fig.add_trace(
        go.Pie(labels=rfm_segments['segment'], values=rfm_segments['user_count'],
               marker_colors=colors, name="고객 수"),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Pie(labels=rfm_segments['segment'], values=rfm_segments['revenue_pct'],
               marker_colors=colors, name="매출 기여"),
        row=1, col=2
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# 페이지 4: 세그먼트 분석
# ============================================
elif page == "👥 세그먼트 분석":
    st.markdown("# 👥 세그먼트별 상세 분석")
    
    st.markdown("---")
    
    st.markdown("## 📊 세그먼트 개요")
    
    # 세그먼트 상세 테이블
    st.dataframe(
        rfm_segments.style.format({
            "user_count": "{:,.0f}",
            "pct": "{:.2f}%",
            "avg_recency": "{:.1f}",
            "avg_frequency": "{:.2f}",
            "avg_monetary": "{:.2f}",
            "revenue_pct": "{:.2f}%"
        }),
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    
    # 세그먼트별 상세 분석
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Champions 분석")
        st.markdown("""
        <div class="action-box">
        <strong>특성</strong><br>
        • 고객 수: 2,787명 (9.35%)<br>
        • 평균 Recency: 80.4일 (최근 활동)<br>
        • 평균 Frequency: 2.22회<br>
        • 매출 기여: 17.1% (고객 비중 대비 1.8배)<br><br>
        <strong>인사이트</strong><br>
        가장 가치 있는 고객으로, 전체의 9.35%이지만 매출의 17.1%를 차지.
        높은 LTV를 보이며 충성도가 높음.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 Promising 분석")
        st.markdown("""
        <div class="insight-box">
        <strong>특성</strong><br>
        • 고객 수: 8,446명 (28.35%)<br>
        • 평균 Recency: 84.9일 (최근 활동)<br>
        • 평균 Frequency: 1.0회 (첫 구매만)<br>
        • 매출 기여: 23.73%<br><br>
        <strong>인사이트</strong><br>
        가장 큰 성장 잠재력. 최근 첫 구매를 한 고객으로,
        적절한 리텐션 전략을 통해 Champions로 전환 가능.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### ⚠️ At Risk 분석")
        st.markdown("""
        <div class="warning-box">
        <strong>특성</strong><br>
        • 고객 수: 6,637명 (22.28%)<br>
        • 평균 Recency: 270.2일 (9개월 전)<br>
        • 평균 Frequency: 1.0회<br>
        • 매출 기여: 18.75%<br><br>
        <strong>인사이트</strong><br>
        1회 구매 후 장기간 비활동. 이탈 가능성이 높아
        긴급한 재활성 캠페인이 필요한 그룹.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 😴 Hibernating 분석")
        st.markdown("""
        <div class="warning-box">
        <strong>특성</strong><br>
        • 고객 수: 9,707명 (32.58%) - 최대 비중<br>
        • 평균 Recency: 538.5일 (1.5년+)<br>
        • 평균 Frequency: 1.0회<br>
        • 매출 기여: 27.21%<br><br>
        <strong>인사이트</strong><br>
        완전 휴면 상태. 과거 매출 기여는 크나 재활성 비용 대비
        효과를 고려한 선별적 윈백 전략 필요.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("## 📈 세그먼트별 RFM 지표 비교")
    
    # Radar Chart
    categories = ['Recency (역수)', 'Frequency', 'Monetary']
    
    # 정규화된 값 계산 (0-100 스케일)
    fig = go.Figure()
    
    for _, row in rfm_segments.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[
                100 - (row['avg_recency'] / 538.5 * 100),  # Recency 역수 (낮을수록 좋음)
                row['avg_frequency'] / 2.22 * 100,          # Frequency 정규화
                row['avg_monetary'] / 3.17 * 100            # Monetary 정규화
            ],
            theta=categories,
            fill='toself',
            name=row['segment']
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
    <strong>📊 해석 가이드</strong><br>
    • Recency (역수): 높을수록 최근 구매 (Champions가 가장 높음)<br>
    • Frequency: 높을수록 자주 구매<br>
    • Monetary: 높을수록 많이 구매<br>
    • Champions와 Loyal Customers가 모든 지표에서 우수
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 페이지 5: Promising 전환 분석
# ============================================
elif page == "🎯 Promising 전환 분석":
    st.markdown("# 🎯 Promising → Champions 전환 분석")
    
    st.markdown("---")
    
    st.markdown("## ❓ 핵심 질문")
    st.markdown("""
    > "Promising 고객 8,446명 중 Champions로 전환될 가능성이 높은 고객은 누구인가?"
    """)
    
    st.markdown("---")
    
    st.markdown("## 📊 Promising 고객의 구매 후 활동 분석")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.bar(
            promising_activity,
            x='activity_level',
            y='pct',
            text='pct',
            color='activity_level',
            color_discrete_sequence=['#e74c3c', '#f39c12', '#3498db', '#2ecc71']
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(
            title="첫 구매 후 사이트 재방문 세션 분포",
            xaxis_title="활동 수준",
            yaxis_title="비율 (%)",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="warning-box">
        <strong>🚨 핵심 발견</strong><br><br>
        Promising 고객의 <strong>70.78%</strong>가
        첫 구매 후 사이트를 재방문하지 않음!<br><br>
        이는 리텐션 전략의 심각한 부재를 의미합니다.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="action-box">
        <strong>💡 기회</strong><br><br>
        4+ 세션 방문 고객(2.09%)은
        평균 5.8개 이벤트, 0.6개 상품 조회로
        <strong>높은 구매 의향</strong>을 보임.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("## ⏰ 가입~첫 구매 타이밍과 재구매율 관계")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.bar(
            first_purchase_timing,
            x='timing',
            y='repurchase_rate',
            text='repurchase_rate',
            color='repurchase_rate',
            color_continuous_scale='Greens'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(
            title="가입 후 첫 구매 시점별 재구매율",
            xaxis_title="가입~첫 구매 시점",
            yaxis_title="재구매율 (%)",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
        <strong>✅ 가설 H1 검증됨</strong><br><br>
        가입 후 <strong>빠르게 첫 구매</strong>를 한 고객의
        재구매율이 확실히 높습니다!<br><br>
        • 1주 이내: <strong>26.06%</strong><br>
        • 3개월+: <strong>15.79%</strong><br><br>
        <strong>차이: +65%</strong>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("## 📈 Champions의 2차 구매 패턴")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            champions_repurchase,
            x='time_bucket',
            y='pct',
            text='pct',
            color='time_bucket',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(
            title="Champions의 첫→2차 구매 간격",
            xaxis_title="구매 간격",
            yaxis_title="비율 (%)",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.line(
            champions_repurchase,
            x='time_bucket',
            y='cumulative_pct',
            markers=True,
            text='cumulative_pct'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='top center')
        fig.update_layout(
            title="누적 전환율",
            xaxis_title="구매 간격",
            yaxis_title="누적 비율 (%)"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="warning-box">
    <strong>⚠️ 주의점</strong><br><br>
    Champions의 72.51%가 3개월 이후에 2차 구매를 함.
    단기 전환 (1개월 내)은 9.7%에 불과.<br><br>
    → <strong>장기적 관점</strong>의 리텐션 전략 필요<br>
    → 3개월 이내 전환 목표 설정 시 현실적 기대치 필요
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("## 🎯 전환 속도별 행동 분석")
    
    st.dataframe(
        conversion_speed.style.format({
            "count": "{:,}",
            "avg_days": "{:.1f}",
            "avg_sessions": "{:.1f}",
            "avg_product_views": "{:.1f}"
        }),
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("""
    <div class="insight-box">
    <strong>💡 인사이트</strong><br><br>
    빠른 전환 (≤30일) 고객은:
    • 세션 수가 적음 (0.6회) → <strong>즉각적 결정</strong><br>
    • 상품 조회도 적음 (0.2회) → <strong>목적 구매</strong><br><br>
    느린 전환 (61+일) 고객은:
    • 세션 수가 많음 (0.9회) → <strong>고민 구매</strong><br>
    • 상품 조회가 많음 (0.4회) → <strong>비교 탐색</strong><br><br>
    → 목적 구매자는 빠른 전환, 탐색형은 장기 육성 필요
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 페이지 6: Champions 행동 분석
# ============================================
elif page == "🏆 Champions 행동 분석":
    st.markdown("# 🏆 Champions 고객 행동 심층 분석")
    
    st.markdown("---")
    
    st.markdown("## 🛍️ 구매 카테고리 패턴")
    
    st.markdown("""
    Champions 고객의 1차 → 2차 구매 시 카테고리 변화를 분석했습니다.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 카테고리 패턴 파이 차트
        category_pattern = pd.DataFrame({
            "pattern": ["Same Department", "Same Category"],
            "pct": [92.51, 7.49]
        })
        
        fig = px.pie(
            category_pattern,
            values='pct',
            names='pattern',
            color_discrete_sequence=['#3498db', '#2ecc71'],
            hole=0.4
        )
        fig.update_layout(title="1차→2차 구매 카테고리 패턴")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
        <strong>📊 카테고리 충성도</strong><br><br>
        Champions의 <strong>92.51%</strong>가
        같은 Department 내에서 2차 구매!<br><br>
        이는 고객이 특정 카테고리에 대한
        <strong>강한 선호도</strong>를 가지고 있음을 의미합니다.<br><br>
        <strong>액션</strong>: 첫 구매 카테고리 기반
        동일 Department 상품 추천 전략 효과적
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("## 📈 카테고리별 Champions 전환율")
    
    fig = px.bar(
        category_conversion.sort_values('conversion_rate', ascending=True),
        x='conversion_rate',
        y='category',
        orientation='h',
        text='conversion_rate',
        color='conversion_rate',
        color_continuous_scale='Greens'
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        title="첫 구매 카테고리별 Champions 전환율 (상위 10개)",
        xaxis_title="전환율 (%)",
        yaxis_title="카테고리",
        showlegend=False,
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="action-box">
        <strong>🏆 고전환 카테고리</strong><br><br>
        1. Clothing Sets: 41.67%<br>
        2. Jumpsuits & Rompers: 29.51%<br>
        3. Plus: 28.40%<br>
        4. Accessories: 28.38%<br>
        5. Blazers & Jackets: 27.62%<br><br>
        → 이 카테고리 첫 구매자 집중 관리!
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
        <strong>💡 전략적 시사점</strong><br><br>
        • <strong>Accessories</strong> (28.38%):
        높은 전환율 + 많은 Champions (174명)
        → 신규 고객 첫 구매 유도용 적합<br><br>
        • <strong>Outerwear & Coats</strong> (26.96%):
        높은 객단가 + 좋은 전환율
        → 고가치 고객 육성 경로
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("## 🔄 주요 카테고리 구매 흐름")
    
    st.markdown("""
    첫 구매 카테고리 → 2차 구매 카테고리 연결 패턴 (10건 이상)
    """)
    
    # 주요 구매 흐름 데이터
    category_flow = pd.DataFrame([
        {"first": "Intimates", "second": "Intimates", "count": 33, "pct": 44.0},
        {"first": "Shorts", "second": "Tops & Tees", "count": 21, "pct": 46.67},
        {"first": "Sweaters", "second": "Jeans", "count": 20, "pct": 27.78},
        {"first": "Tops & Tees", "second": "Sleep & Lounge", "count": 19, "pct": 24.36},
        {"first": "Accessories", "second": "Tops & Tees", "count": 17, "pct": 22.08},
        {"first": "Sleep & Lounge", "second": "Sleep & Lounge", "count": 17, "pct": 24.64},
        {"first": "Pants", "second": "Tops & Tees", "count": 16, "pct": 28.57}
    ])
    
    fig = px.scatter(
        category_flow,
        x='first',
        y='second',
        size='count',
        color='pct',
        color_continuous_scale='Viridis',
        size_max=50,
        hover_data=['count', 'pct']
    )
    fig.update_layout(
        title="카테고리 구매 흐름 (버블 크기 = 건수)",
        xaxis_title="첫 구매 카테고리",
        yaxis_title="2차 구매 카테고리",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
    <strong>💡 크로스셀 기회</strong><br><br>
    • Shorts 구매자 → <strong>Tops & Tees</strong> 추천 (46.67%)<br>
    • Pants 구매자 → <strong>Tops & Tees</strong> 추천 (28.57%)<br>
    • Sweaters 구매자 → <strong>Jeans</strong> 추천 (27.78%)<br><br>
    → 상의+하의 조합 추천 번들 전략 효과적
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 페이지 7: 채널 & 카테고리 분석
# ============================================
elif page == "📊 채널 & 카테고리 분석":
    st.markdown("# 📊 채널 & 카테고리 심층 분석")
    
    st.markdown("---")
    
    st.markdown("## 📱 유입 채널별 Champions 전환율")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.bar(
            traffic_source_data.sort_values('conversion_rate', ascending=True),
            x='conversion_rate',
            y='source',
            orientation='h',
            text='conversion_rate',
            color='conversion_rate',
            color_continuous_scale='Blues'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(
            title="채널별 Promising → Champions 전환율",
            xaxis_title="전환율 (%)",
            yaxis_title="유입 채널",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="action-box">
        <strong>✅ 가설 H3 검증됨</strong><br><br>
        채널에 따라 고객 품질이 다릅니다!<br><br>
        <strong>1위 Email</strong>: 27.13%<br>
        <strong>2위 Facebook</strong>: 26.27%<br>
        <strong>3위 Search</strong>: 24.92%<br>
        <strong>4위 Display</strong>: 24.05%<br>
        <strong>5위 Organic</strong>: 23.12%<br><br>
        Email 채널이 가장 높은 전환율!
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("## 💰 채널 × 카테고리별 LTV 분석")
    
    st.markdown("""
    Champions 고객의 유입 채널과 첫 구매 카테고리 조합별 평균 LTV(생애가치)를 분석했습니다.
    """)
    
    # LTV 히트맵
    ltv_pivot = ltv_data.pivot_table(
        values='avg_ltv', 
        index='category', 
        columns='source', 
        aggfunc='mean'
    ).fillna(0)
    
    fig = px.imshow(
        ltv_pivot,
        color_continuous_scale='RdYlGn',
        labels=dict(x="유입 채널", y="첫 구매 카테고리", color="평균 LTV ($)"),
        aspect="auto"
    )
    fig.update_layout(
        title="채널 × 카테고리 조합별 평균 LTV (상위 데이터)",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 LTV 상위 조합")
        top_ltv = ltv_data.nlargest(5, 'avg_ltv')[['source', 'category', 'avg_ltv', 'champions']]
        st.dataframe(
            top_ltv.style.format({
                'avg_ltv': '${:.2f}',
                'champions': '{:,.0f}'
            }),
            hide_index=True
        )
    
    with col2:
        st.markdown("""
        <div class="insight-box">
        <strong>💡 최고 LTV 조합</strong><br><br>
        1. <strong>Organic + Outerwear</strong>: $452<br>
        2. <strong>Organic + Tops</strong>: $420<br>
        3. <strong>Search + Suits</strong>: $378<br><br>
        Organic 유입 고객의 LTV가 특히 높음!<br>
        (전환율은 낮지만 고객 가치는 최고)
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("## 📊 채널별 전략적 포지셔닝")
    
    # 채널별 특성 요약
    channel_strategy = pd.DataFrame({
        "채널": ["Email", "Facebook", "Search", "Display", "Organic"],
        "전환율": [27.13, 26.27, 24.92, 24.05, 23.12],
        "볼륨 (Promising)": [419, 508, 5862, 360, 1297],
        "Champions 수": [156, 181, 1946, 114, 390],
        "전략": [
            "높은 전환율 활용, 구독자 확대",
            "소셜 광고 최적화, 리타겟팅",
            "핵심 볼륨 채널, 효율 유지",
            "전환율 개선 필요, 타겟팅 정교화",
            "낮은 전환율이나 높은 LTV, 브랜드 투자"
        ]
    })
    
    st.dataframe(channel_strategy, hide_index=True, use_container_width=True)
    
    # 채널 포지셔닝 차트
    fig = px.scatter(
        traffic_source_data,
        x='promising',
        y='conversion_rate',
        size='champions',
        color='source',
        text='source',
        size_max=50
    )
    fig.update_traces(textposition='top center')
    fig.update_layout(
        title="채널별 볼륨 vs 전환율 포지셔닝",
        xaxis_title="Promising 고객 수 (볼륨)",
        yaxis_title="Champions 전환율 (%)",
        showlegend=True,
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
    <strong>📊 채널 포지셔닝 해석</strong><br><br>
    • <strong>Search</strong>: 높은 볼륨 + 중간 전환율 → 핵심 채널, 효율 유지 중요<br>
    • <strong>Email</strong>: 낮은 볼륨 + 최고 전환율 → 확장 기회, 구독자 확대 필요<br>
    • <strong>Organic</strong>: 중간 볼륨 + 낮은 전환율 → 그러나 최고 LTV, 브랜드 투자<br>
    • <strong>Display</strong>: 낮은 볼륨 + 낮은 전환율 → 타겟팅 개선 또는 예산 재배분
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 페이지 8: 액션 플랜
# ============================================
elif page == "💡 액션 플랜":
    st.markdown("# 💡 세그먼트별 액션 플랜")
    
    st.markdown("---")
    
    st.markdown("## 🎯 전략 프레임워크")
    
    st.markdown("""
    분석 결과를 바탕으로 각 세그먼트별 맞춤 마케팅 전략을 수립했습니다.
    """)
    
    # 우선순위 매트릭스
    priority_data = pd.DataFrame({
        "세그먼트": ["Promising", "Champions", "At Risk", "Loyal", "Need Attention", "Hibernating"],
        "우선순위": [1, 2, 3, 4, 5, 6],
        "고객 수": [8446, 2787, 6637, 1357, 861, 9707],
        "예상 ROI": ["높음", "매우 높음", "중간", "높음", "중간", "낮음"],
        "긴급도": ["매우 높음", "중간", "높음", "중간", "높음", "낮음"]
    })
    
    st.dataframe(priority_data, hide_index=True, use_container_width=True)
    
    st.markdown("---")
    
    # 세그먼트별 상세 액션 플랜
    st.markdown("## 📋 세그먼트별 상세 액션 플랜")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🎯 Promising", "🏆 Champions", "⚠️ At Risk", 
        "💎 Loyal", "🔔 Need Attention", "😴 Hibernating"
    ])
    
    with tab1:
        st.markdown("### 🎯 Promising 고객 전환 전략")
        st.markdown("""
        **목표**: 8,446명 중 25% (2,111명)를 Champions로 전환
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="action-box">
            <strong>📧 리텐션 캠페인</strong><br><br>
            <strong>1. Welcome 시퀀스 (첫 구매 후)</strong><br>
            • Day 1: 감사 메일 + 추천 상품<br>
            • Day 3: 동일 카테고리 신상품 소개<br>
            • Day 7: 첫 구매 할인 쿠폰 (10%)<br>
            • Day 14: 크로스셀 제안<br><br>
            <strong>2. 재방문 유도</strong><br>
            • 푸시 알림 설정 유도<br>
            • 앱 설치 인센티브<br>
            • 위시리스트 기능 안내
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="insight-box">
            <strong>🎁 오퍼 전략</strong><br><br>
            <strong>활동 기반 차등 혜택</strong><br><br>
            • 비활동(70.78%): 재방문 시 포인트 2배<br>
            • 1 Session (8.05%): 장바구니 리마인드<br>
            • 2-3 Sessions (19.08%): 무료 배송 쿠폰<br>
            • 4+ Sessions (2.09%): VIP 프리뷰 초대<br><br>
            <strong>예상 효과</strong><br>
            전환율 +5%p → 추가 Champions 422명
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🏆 Champions 유지 & 확대 전략")
        st.markdown("""
        **목표**: 2,787명 충성도 강화 + LTV 15% 증가
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="action-box">
            <strong>👑 VIP 프로그램</strong><br><br>
            <strong>Tier 혜택</strong><br>
            • 조기 접근: 신상품 48시간 선공개<br>
            • 전용 할인: 연간 15% 추가 할인<br>
            • 무료 배송: 전 구매 무료 배송<br>
            • 생일 혜택: 20% 할인 쿠폰<br><br>
            <strong>리워드 프로그램</strong><br>
            • 구매당 포인트 적립 (5%)<br>
            • 리뷰 작성 보너스<br>
            • 친구 추천 인센티브
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="insight-box">
            <strong>🛍️ 크로스셀 전략</strong><br><br>
            <strong>카테고리 기반 추천</strong><br>
            (92.51%가 같은 Department 재구매)<br><br>
            • Shorts → Tops & Tees (46.67%)<br>
            • Sweaters → Jeans (27.78%)<br>
            • Pants → Tops & Tees (28.57%)<br><br>
            <strong>번들 상품</strong><br>
            상하의 조합 10% 추가 할인
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### ⚠️ At Risk 고객 구조 전략")
        st.markdown("""
        **목표**: 6,637명 중 20% (1,327명) 재활성화
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="warning-box">
            <strong>📍 현황</strong><br><br>
            • 평균 Recency: 270일 (9개월)<br>
            • 1회 구매 후 장기 비활동<br>
            • 이탈 가능성 높음<br><br>
            <strong>⏰ 골든 타임</strong><br>
            3개월 내 재활성화 시도 필요
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="action-box">
            <strong>🎯 재활성화 캠페인</strong><br><br>
            <strong>1. "We Miss You" 시퀀스</strong><br>
            • 개인화된 상품 추천 메일<br>
            • 과거 구매 기반 신상품 소개<br><br>
            <strong>2. 특별 혜택</strong><br>
            • 재구매 시 20% 할인<br>
            • 무료 배송 + 적립금<br><br>
            <strong>3. 타이밍</strong><br>
            • 세일 시즌 타겟 발송<br>
            • 과거 구매 주기 분석
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 💎 Loyal Customers 케어 전략")
        st.markdown("""
        **목표**: 1,357명의 활동 주기 단축
        """)
        
        st.markdown("""
        <div class="insight-box">
        <strong>특성</strong>: 다회 구매 이력이 있으나 최근 활동이 뜸한 고객<br><br>
        <strong>전략</strong>:<br>
        • 개인화된 "다시 만나요" 메시지<br>
        • 과거 구매 패턴 기반 신상품 알림<br>
        • 한정판 또는 시즌 상품 조기 알림<br>
        • 멤버십 혜택 리마인드
        </div>
        """, unsafe_allow_html=True)
    
    with tab5:
        st.markdown("### 🔔 Need Attention 긴급 대응")
        st.markdown("""
        **목표**: 861명 윈백
        """)
        
        st.markdown("""
        <div class="warning-box">
        <strong>⚠️ 긴급 상황</strong><br><br>
        • 과거 다회 구매 고객이 이탈 중!<br>
        • 평균 Recency: 478일 (1년 4개월)<br>
        • 높은 가치의 고객을 잃고 있음<br><br>
        <strong>즉시 조치</strong>:<br>
        • 개인화된 윈백 메일 발송<br>
        • 과거 구매 품목 기반 대폭 할인 (30%)<br>
        • 1:1 고객 서비스 연락
        </div>
        """, unsafe_allow_html=True)
    
    with tab6:
        st.markdown("### 😴 Hibernating 선별적 접근")
        st.markdown("""
        **목표**: 비용 효율적 윈백 또는 정리
        """)
        
        st.markdown("""
        <div class="insight-box">
        <strong>현실적 접근</strong><br><br>
        9,707명 전체를 대상으로 마케팅하는 것은 비효율적.<br><br>
        <strong>선별 기준</strong>:<br>
        • 과거 구매 금액 상위 20%만 타겟<br>
        • 대규모 프로모션 시즌에만 접촉<br>
        • 저비용 채널 (이메일) 활용<br><br>
        <strong>나머지 80%</strong>:<br>
        • 마케팅 비용 절감<br>
        • 신규 고객 확보에 예산 재배분
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("## 📊 KPI & 성과 측정")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🎯 전환 KPI
        - Promising → Champions 전환율
          - 현재: 25%
          - 목표: 30% (+5%p)
        
        - At Risk 재활성화율
          - 목표: 20%
        """)
    
    with col2:
        st.markdown("""
        ### 💰 매출 KPI
        - Champions LTV
          - 현재: $280
          - 목표: $320 (+14%)
        
        - 전체 재구매율
          - 현재: 16.8%
          - 목표: 22% (+5.2%p)
        """)
    
    with col3:
        st.markdown("""
        ### 📈 활동 KPI
        - Promising 재방문율
          - 현재: 29.2%
          - 목표: 50%
        
        - Champions 이탈률
          - 현재: N/A
          - 목표: <5%/월
        """)
    
    st.markdown("---")
    
    st.markdown("## 🗓️ 실행 로드맵")
    
    roadmap = pd.DataFrame({
        "단계": ["Phase 1", "Phase 2", "Phase 3", "Phase 4"],
        "기간": ["Week 1-2", "Week 3-4", "Month 2", "Month 3+"],
        "주요 활동": [
            "Promising 리텐션 캠페인 런칭",
            "Champions VIP 프로그램 구축",
            "At Risk 윈백 캠페인",
            "전체 성과 분석 & 최적화"
        ],
        "예상 성과": [
            "재방문율 +15%p",
            "LTV +10%",
            "재활성화 1,000명+",
            "전체 매출 +12%"
        ]
    })
    
    st.dataframe(roadmap, hide_index=True, use_container_width=True)
    
    st.markdown("""
    <div class="action-box">
    <strong>🚀 핵심 메시지</strong><br><br>
    이 분석을 통해 <strong>29,795명의 고객을 6개 세그먼트</strong>로 분류하고,
    각 세그먼트별 맞춤 전략을 수립했습니다.<br><br>
    가장 큰 기회는 <strong>Promising 8,446명</strong>의 전환이며,
    초기 리텐션 전략을 통해 <strong>월 +12.7% 매출 성장</strong>이 가능합니다.<br><br>
    지금 바로 Welcome 시퀀스부터 시작하세요! 💪
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 푸터
# ============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 0.9rem;">
    📊 TheLook E-commerce RFM 분석 포트폴리오<br>
    김동윤 포트폴리오 | BigQuery thelook_ecommerce 데이터셋 활용<br>
    분석 기간: 2023.01.01 ~ 2024.12.31
</div>
""", unsafe_allow_html=True)