"""
TheLook E-commerce RFM 분석 포트폴리오
=====================================
분석 기간: 2023-01-01 ~ 2024-12-31
총 분석 고객: 29,795명
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
    .segment-champions { border-color: #10b981; }
    .segment-loyal { border-color: #3b82f6; }
    .segment-promising { border-color: #8b5cf6; }
    .segment-attention { border-color: #f59e0b; }
    .segment-risk { border-color: #f97316; }
    .segment-hibernating { border-color: #6b7280; }
    
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
    .styled-table tr:hover {
        background: #f9fafb;
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
    
    /* 사이드바 */
    .css-1d391kg {
        background: #f8fafc;
    }
    
    /* 섹션 디바이더 */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
        margin: 2rem 0;
        border-radius: 1px;
    }
    
    /* KPI 그리드 */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 데이터 정의
# ============================================

# RFM 세그먼트 데이터
segment_data = pd.DataFrame([
    {"segment": "Champions", "user_count": 2787, "pct": 9.35, "avg_recency": 80.4, 
     "avg_frequency": 2.22, "avg_monetary": 189.56, "revenue_pct": 17.25, 
     "r_score": 4.58, "f_score": 4.19, "m_score": 3.55},
    {"segment": "Loyal Customers", "user_count": 1357, "pct": 4.55, "avg_recency": 263.1, 
     "avg_frequency": 2.16, "avg_monetary": 185.14, "revenue_pct": 8.20,
     "r_score": 3.0, "f_score": 4.14, "m_score": 3.54},
    {"segment": "Promising", "user_count": 8446, "pct": 28.35, "avg_recency": 84.9, 
     "avg_frequency": 1.0, "avg_monetary": 85.45, "revenue_pct": 23.56,
     "r_score": 4.55, "f_score": 3.0, "m_score": 2.34},
    {"segment": "Need Attention", "user_count": 861, "pct": 2.89, "avg_recency": 478.3, 
     "avg_frequency": 2.07, "avg_monetary": 182.52, "revenue_pct": 5.13,
     "r_score": 1.77, "f_score": 4.07, "m_score": 3.49},
    {"segment": "At Risk", "user_count": 6637, "pct": 22.28, "avg_recency": 270.2, 
     "avg_frequency": 1.0, "avg_monetary": 85.36, "revenue_pct": 18.49,
     "r_score": 3.0, "f_score": 3.0, "m_score": 2.36},
    {"segment": "Hibernating", "user_count": 9707, "pct": 32.58, "avg_recency": 538.5, 
     "avg_frequency": 1.0, "avg_monetary": 86.38, "revenue_pct": 27.37,
     "r_score": 1.53, "f_score": 3.0, "m_score": 2.35}
])

# 채널별 전환율 데이터
channel_data = pd.DataFrame([
    {"channel": "Email", "conversion_rate": 27.13, "promising": 419, "champions": 156, 
     "avg_monetary_p": 82.63, "avg_monetary_c": 170.70},
    {"channel": "Facebook", "conversion_rate": 26.27, "promising": 508, "champions": 181,
     "avg_monetary_p": 84.99, "avg_monetary_c": 195.52},
    {"channel": "Search", "conversion_rate": 24.92, "promising": 5862, "champions": 1946,
     "avg_monetary_p": 85.86, "avg_monetary_c": 187.32},
    {"channel": "Display", "conversion_rate": 24.05, "promising": 360, "champions": 114,
     "avg_monetary_p": 85.48, "avg_monetary_c": 180.54},
    {"channel": "Organic", "conversion_rate": 23.12, "promising": 1297, "champions": 390,
     "avg_monetary_p": 84.69, "avg_monetary_c": 208.17}
])

# 첫 구매 타이밍별 재구매율
timing_data = pd.DataFrame([
    {"timing": "1주일 이내", "user_count": 307, "repurchase_rate": 26.06, 
     "champions_rate": 16.94, "avg_monetary": 112.28},
    {"timing": "1개월 이내", "user_count": 901, "repurchase_rate": 25.08, 
     "champions_rate": 16.32, "avg_monetary": 116.92},
    {"timing": "2개월 이내", "user_count": 1161, "repurchase_rate": 24.63, 
     "champions_rate": 15.42, "avg_monetary": 110.41},
    {"timing": "3개월 이내", "user_count": 1058, "repurchase_rate": 23.63, 
     "champions_rate": 14.08, "avg_monetary": 113.97},
    {"timing": "3개월+", "user_count": 26368, "repurchase_rate": 15.79, 
     "champions_rate": 8.57, "avg_monetary": 101.45}
])

# Promising 구매 후 활동
promising_activity = pd.DataFrame([
    {"activity": "활동 없음", "user_count": 5918, "pct": 70.07, "avg_monetary": 59.93},
    {"activity": "1회 세션", "user_count": 700, "pct": 8.29, "avg_monetary": 118.36},
    {"activity": "2-3회 세션", "user_count": 1652, "pct": 19.56, "avg_monetary": 146.74},
    {"activity": "4-5회 세션", "user_count": 175, "pct": 2.07, "avg_monetary": 238.28}
])

# Champions 재구매 타이밍
repurchase_timing = pd.DataFrame([
    {"bucket": "1주 이내", "count": 72, "pct": 2.58, "avg_days": 3.7, "avg_ltv": 225.77},
    {"bucket": "2주 이내", "count": 62, "pct": 2.22, "avg_days": 10.9, "avg_ltv": 210.16},
    {"bucket": "1개월 이내", "count": 131, "pct": 4.70, "avg_days": 22.6, "avg_ltv": 194.73},
    {"bucket": "2개월 이내", "count": 239, "pct": 8.58, "avg_days": 44.9, "avg_ltv": 189.17},
    {"bucket": "3개월 이내", "count": 246, "pct": 8.83, "avg_days": 75.6, "avg_ltv": 194.99},
    {"bucket": "3개월+", "count": 2037, "pct": 73.09, "avg_days": 302.4, "avg_ltv": 186.72}
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
    "🎯 문제 정의 & 가설": "problem",
    "📐 RFM 등급 설계": "rfm_design",
    "👥 세그먼트 분석": "segment",
    "🌱 Promising 전환 분석": "promising",
    "🏆 Champions 행동 분석": "champions",
    "📢 채널 & 카테고리 분석": "channel",
    "🚀 Action Plan": "action"
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
</div>
""", unsafe_allow_html=True)

# ============================================
# 페이지 1: Executive Summary
# ============================================
if pages[selected_page] == "executive":
    st.markdown("""
    <div class="main-header">
        <h1>🏠 Executive Summary</h1>
        <p>김동윤의 TheLook E-commerce RFM 기반 고객 세그먼트 분석 및 전략 제안</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 데이터셋 ERD 섹션
    st.subheader("🗄️ TheLook E-commerce 데이터셋 ERD")
    
    col_erd1, col_erd2 = st.columns([1.3, 1])
    
    with col_erd1:
        # Graphviz ERD
        erd_code = """
        digraph TheLook_ERD {
            rankdir=LR;
            node [shape=record, fontname="Helvetica", fontsize=10];
            edge [fontname="Helvetica", fontsize=9];
            
            users [label="{users|id (PK)\\nfirst_name\\nlast_name\\nemail\\ntraffic_source\\ncreated_at\\ncountry, city}"];
            orders [label="{orders|order_id (PK)\\nuser_id (FK)\\nstatus\\ncreated_at\\nnum_of_item}"];
            order_items [label="{order_items|id (PK)\\norder_id (FK)\\nuser_id (FK)\\nproduct_id (FK)\\nsale_price ★\\nstatus\\ncreated_at}"];
            products [label="{products|id (PK)\\nname\\ncategory\\ndepartment\\nretail_price\\nbrand}"];
            events [label="{events|id (PK)\\nuser_id (FK)\\nsession_id\\nevent_type\\nuri\\ncreated_at}"];
            
            users -> orders [label="1:N"];
            users -> events [label="1:N"];
            orders -> order_items [label="1:N"];
            products -> order_items [label="1:N"];
        }
        """
        st.graphviz_chart(erd_code, use_container_width=True)
    
    with col_erd2:
        st.markdown("""
        <div class="insight-box">
            <div class="insight-title">📊 분석에 사용된 테이블</div>
            <div class="insight-text">
                <table style="width:100%; font-size: 0.85rem;">
                    <tr style="border-bottom: 1px solid #e5e7eb;">
                        <td style="padding: 8px 0;"><b>users</b></td>
                        <td>고객 정보, 유입 채널</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e5e7eb;">
                        <td style="padding: 8px 0;"><b>orders</b></td>
                        <td>주문 헤더, 상태</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e5e7eb;">
                        <td style="padding: 8px 0;"><b>order_items</b></td>
                        <td>주문 상세, <span style="color:#10b981;">sale_price</span></td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e5e7eb;">
                        <td style="padding: 8px 0;"><b>products</b></td>
                        <td>상품, 카테고리</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0;"><b>events</b></td>
                        <td>사이트 행동 로그</td>
                    </tr>
                </table>
            </div>
        </div>
        
        <div class="insight-box warning" style="margin-top: 1rem;">
            <div class="insight-title">💡 Key Point</div>
            <div class="insight-text" style="font-size: 0.85rem;">
                Monetary 계산 시 <code>orders.num_of_item</code>이 아닌
                <code>order_items.sale_price</code>의 <b>실제 매출 합계</b>를 사용하여
                정확한 고객 가치 측정
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 핵심 지표
    col1, col2, col3, col4 = st.columns(4)
    
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
            <div class="metric-value">$102.82</div>
            <div class="metric-label">평균 고객 가치</div>
            <div class="metric-delta">LTV 기준</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card orange">
            <div class="metric-value">9.35%</div>
            <div class="metric-label">Champions 비율</div>
            <div class="metric-delta delta-positive">2,787명</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card red">
            <div class="metric-value">70.07%</div>
            <div class="metric-label">Promising 이탈률</div>
            <div class="metric-delta delta-negative">재방문 없음</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 핵심 발견사항
    st.subheader("🔍 핵심 발견사항")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box danger">
            <div class="insight-title">🚨 Critical Issue: Promising 이탈 위기</div>
            <div class="insight-text">
                전체 고객의 <b>28.35%</b>를 차지하는 Promising 세그먼트 중 
                <b>70.07%(5,918명)</b>이 첫 구매 후 재방문하지 않음.<br>
                이는 연간 <b>약 $505,000</b>의 잠재 매출 손실로 추정됨.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-box warning">
            <div class="insight-title">⚡ 빠른 첫 구매 = 높은 전환율</div>
            <div class="insight-text">
                가입 후 <b>1주일 내 첫 구매</b> 고객의 재구매율은 <b>26.06%</b>,<br>
                Champions 전환율은 <b>16.94%</b>로 3개월+ 대비 <b>2배</b> 높음.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box success">
            <div class="insight-title">✅ Email 채널 최고 품질</div>
            <div class="insight-text">
                Email 채널의 Champions 전환율 <b>27.13%</b>로 전 채널 중 최고.<br>
                Organic 채널 대비 <b>+4%p</b> 높은 전환율 기록.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-box">
            <div class="insight-title">📊 Champions의 빠른 재구매 = 높은 LTV</div>
            <div class="insight-text">
                1주 내 재구매 Champions의 평균 LTV는 <b>$225.77</b>,<br>
                3개월+ 재구매 대비 <b>+20.9%</b> 높음.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 세그먼트 개요
    st.subheader("👥 고객 세그먼트 개요")
    
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
        fig.update_layout(height=400, margin=dict(t=50, l=0, r=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.pie(
            segment_data,
            values='revenue_pct',
            names='segment',
            title='세그먼트별 매출 기여도',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(height=400)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # ROI 예상
    st.subheader("💰 예상 ROI")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="action-box">
            <div class="action-header">
                <div class="action-icon" style="background: #dcfce7;">🌱</div>
                <div class="action-title">Promising 리텐션</div>
            </div>
            <div class="action-content">
                <p><b>목표:</b> 이탈률 70% → 50% 감소</p>
                <p><b>예상 전환:</b> +1,184명 재구매</p>
                <p><b>예상 매출:</b> <span style="color: #10b981; font-weight: 700;">+$101,000/년</span></p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="action-box">
            <div class="action-header">
                <div class="action-icon" style="background: #fef3c7;">📧</div>
                <div class="action-title">Email 채널 확대</div>
            </div>
            <div class="action-content">
                <p><b>목표:</b> Email 비중 5% → 15%</p>
                <p><b>예상 전환:</b> +312명 Champions</p>
                <p><b>예상 매출:</b> <span style="color: #10b981; font-weight: 700;">+$53,000/년</span></p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="action-box">
            <div class="action-header">
                <div class="action-icon" style="background: #e0e7ff;">⏰</div>
                <div class="action-title">조기 전환 촉진</div>
            </div>
            <div class="action-content">
                <p><b>목표:</b> 1주 내 첫 구매 비율 1% → 5%</p>
                <p><b>예상 전환:</b> +180명 Champions</p>
                <p><b>예상 매출:</b> <span style="color: #10b981; font-weight: 700;">+$34,000/년</span></p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# 페이지 2: 문제 정의 & 가설
# ============================================
elif pages[selected_page] == "problem":
    st.markdown("""
    <div class="main-header">
        <h1>🎯 문제 정의 & 가설</h1>
        <p>데이터 기반 비즈니스 문제 정의 및 검증 가설 수립</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 비즈니스 컨텍스트
    st.subheader("📋 비즈니스 컨텍스트")
    
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">TheLook E-commerce 현황</div>
        <div class="insight-text">
            TheLook은 의류 중심 이커머스 플랫폼으로, 2년간 약 <b>30,000명</b>의 구매 고객을 확보했습니다.
            그러나 고객당 평균 구매 빈도는 <b>1.2회</b>에 불과하며, 75%의 고객이 단 1회만 구매하고 있습니다.
            이는 신규 고객 획득에는 성공했으나, <b>고객 유지(Retention)에 심각한 문제</b>가 있음을 시사합니다.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 핵심 문제
    st.subheader("🚨 핵심 문제 정의")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="segment-card segment-risk">
            <h4 style="margin-bottom: 1rem;">📉 Problem 1: 낮은 재구매율</h4>
            <ul style="color: #4b5563; line-height: 1.8;">
                <li>전체 고객의 <b>75%가 1회 구매</b> 후 이탈</li>
                <li>평균 구매 빈도 1.2회로 업계 평균(2.5회) 대비 52% 낮음</li>
                <li>고객 획득 비용 대비 낮은 LTV로 수익성 저하</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="segment-card segment-attention">
            <h4 style="margin-bottom: 1rem;">📉 Problem 2: Promising 전환 실패</h4>
            <ul style="color: #4b5563; line-height: 1.8;">
                <li>최근 구매 신규 고객의 <b>70%가 무활동</b> 상태</li>
                <li>Champions로의 전환율 24.92%에 불과</li>
                <li>잠재 고가치 고객을 놓치는 기회 비용 발생</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 가설 설정
    st.subheader("🔬 검증 가설")
    
    st.markdown("""
    <div class="action-box">
        <div class="action-header">
            <div class="action-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">H1</div>
            <div class="action-title">가설 1: 조기 전환 가설</div>
        </div>
        <div class="action-content">
            <p><b>가설:</b> 가입 후 빠른 시일 내 첫 구매를 유도하면 재구매율과 Champions 전환율이 높아질 것이다.</p>
            <p><b>측정 지표:</b> 가입-첫구매 기간별 재구매율, Champions 전환율</p>
            <p style="color: #10b981;"><b>✅ 검증 결과:</b> 1주 내 첫 구매 시 재구매율 26.06% vs 3개월+ 15.79% (1.65배 차이)</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="action-box">
        <div class="action-header">
            <div class="action-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">H2</div>
            <div class="action-title">가설 2: 활동 기반 전환 가설</div>
        </div>
        <div class="action-content">
            <p><b>가설:</b> 첫 구매 후 사이트 재방문 활동이 많은 Promising 고객일수록 Champions로 전환될 가능성이 높다.</p>
            <p><b>측정 지표:</b> 구매 후 세션 수별 평균 LTV, M Score</p>
            <p style="color: #10b981;"><b>✅ 검증 결과:</b> 4-5회 세션 유저의 avg LTV $238.28 vs 무활동 $59.93 (4배 차이)</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="action-box">
        <div class="action-header">
            <div class="action-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">H3</div>
            <div class="action-title">가설 3: 채널 품질 가설</div>
        </div>
        <div class="action-content">
            <p><b>가설:</b> 유입 채널에 따라 고객 품질(전환율, LTV)에 유의미한 차이가 있을 것이다.</p>
            <p><b>측정 지표:</b> 채널별 Champions 전환율, 평균 LTV</p>
            <p style="color: #10b981;"><b>✅ 검증 결과:</b> Email 전환율 27.13% > Organic 23.12% (+4%p 차이)</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 분석 프레임워크
    st.subheader("📊 분석 프레임워크")
    
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <div class="process-flow">
            <div class="process-step">
                <div class="process-number">1</div>
                <div class="process-label">데이터 수집</div>
                <div style="font-size: 0.75rem; color: #9ca3af;">Orders, Items, Events</div>
            </div>
            <div style="color: #d1d5db; font-size: 1.5rem;">→</div>
            <div class="process-step">
                <div class="process-number">2</div>
                <div class="process-label">RFM 계산</div>
                <div style="font-size: 0.75rem; color: #9ca3af;">분포 기반 점수화</div>
            </div>
            <div style="color: #d1d5db; font-size: 1.5rem;">→</div>
            <div class="process-step">
                <div class="process-number">3</div>
                <div class="process-label">세그먼트 분류</div>
                <div style="font-size: 0.75rem; color: #9ca3af;">6개 그룹</div>
            </div>
            <div style="color: #d1d5db; font-size: 1.5rem;">→</div>
            <div class="process-step">
                <div class="process-number">4</div>
                <div class="process-label">심화 분석</div>
                <div style="font-size: 0.75rem; color: #9ca3af;">행동, 채널, 카테고리</div>
            </div>
            <div style="color: #d1d5db; font-size: 1.5rem;">→</div>
            <div class="process-step">
                <div class="process-number">5</div>
                <div class="process-label">전략 도출</div>
                <div style="font-size: 0.75rem; color: #9ca3af;">세그먼트별 액션</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 페이지 3: RFM 등급 설계
# ============================================
elif pages[selected_page] == "rfm_design":
    st.markdown("""
    <div class="main-header">
        <h1>📐 RFM 등급 설계</h1>
        <p>데이터 분포 기반 RFM 스코어링 기준 및 세그먼트 정의</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 데이터 분포 요약
    st.subheader("📊 데이터 분포 분석")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="segment-card segment-champions">
            <h4>Recency (최근성)</h4>
            <table class="styled-table" style="margin-top: 1rem;">
                <tr><td>P10</td><td style="text-align:right;"><b>40일</b></td></tr>
                <tr><td>P25</td><td style="text-align:right;"><b>111일</b></td></tr>
                <tr><td>P50 (중앙값)</td><td style="text-align:right;"><b>259일</b></td></tr>
                <tr><td>P75</td><td style="text-align:right;"><b>455일</b></td></tr>
                <tr><td>P90</td><td style="text-align:right;"><b>610일</b></td></tr>
                <tr><td>평균 ± 표준편차</td><td style="text-align:right;"><b>293 ± 207일</b></td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="segment-card segment-loyal">
            <h4>Frequency (빈도)</h4>
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
        <div class="segment-card segment-promising">
            <h4>Monetary (금액)</h4>
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
    st.subheader("🎯 RFM 스코어 기준 설정")
    
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">💡 스코어링 원칙</div>
        <div class="insight-text">
            RFM 스코어는 <b>데이터 분포 기반</b>으로 설계되었습니다. 
            백분위(Percentile) 분포를 분석하여 비즈니스적으로 의미 있는 구간을 정의했으며,
            각 지표의 특성을 고려하여 차별화된 기준을 적용했습니다.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Recency Score 기준")
        r_score_data = pd.DataFrame({
            "Score": [5, 4, 3, 2, 1],
            "기준": ["≤ 90일", "91-180일", "181-365일", "366-545일", "546일+"],
            "의미": ["3개월 내 활성", "6개월 내 활성", "1년 내 활성", "1.5년 내 활성", "휴면"],
            "근거": ["P10(40일) 기준", "분기 단위", "연간 사이클", "관찰 기간 고려", "P90(610일) 이상"]
        })
        st.dataframe(r_score_data, hide_index=True, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box success">
            <div class="insight-text" style="font-size: 0.85rem;">
                <b>설계 의도:</b> 의류 구매 주기(3-6개월)를 고려하여 90일 이내를 최상위로 설정.
                6개월 이내 활동 고객을 핵심 타겟으로 분류.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### Frequency Score 기준")
        f_score_data = pd.DataFrame({
            "Score": [5, 4, 3],
            "기준": ["≥ 3회", "2회", "1회"],
            "의미": ["충성 고객", "재구매 고객", "신규/일회성"],
            "근거": ["상위 5%", "P90(상위 10%)", "75% 해당"]
        })
        st.dataframe(f_score_data, hide_index=True, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box warning">
            <div class="insight-text" style="font-size: 0.85rem;">
                <b>설계 의도:</b> 데이터상 75%가 1회 구매자로, F=3을 기본값으로 설정.
                2회 구매만으로도 상위 10%에 해당하므로 F=4 부여.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("#### Monetary Score 기준")
    m_score_data = pd.DataFrame({
        "Score": [5, 4, 3, 2, 1],
        "기준": ["≥ $300", "$135-299", "$67-134", "$34-66", "< $34"],
        "백분위": ["P95+", "P75-P95", "P50-P75", "P25-P50", "P25 미만"],
        "의미": ["VIP", "고가치", "중간", "저가치", "저액"],
        "고객 비율": ["~5%", "~20%", "~25%", "~25%", "~25%"]
    })
    st.dataframe(m_score_data, hide_index=True, use_container_width=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 세그먼트 정의
    st.subheader("👥 세그먼트 정의 로직")
    
    st.code("""
-- RFM 세그먼트 정의 SQL
CASE 
  WHEN r_score >= 4 AND f_score >= 4 THEN 'Champions'      -- 최근 활동 + 재구매
  WHEN r_score >= 3 AND f_score >= 4 THEN 'Loyal Customers' -- 활동 중 + 재구매
  WHEN r_score >= 4 AND f_score = 3 THEN 'Promising'       -- 최근 활동 + 1회 구매
  WHEN r_score <= 2 AND f_score >= 4 THEN 'Need Attention' -- 휴면 + 과거 충성
  WHEN r_score = 3 AND f_score = 3 THEN 'At Risk'          -- 이탈 위험
  WHEN r_score <= 2 AND f_score = 3 THEN 'Hibernating'     -- 장기 휴면
END as customer_segment
    """, language="sql")
    
    # 세그먼트 매트릭스
    st.markdown("#### RF 세그먼트 매트릭스")
    
    matrix_data = [
        ["", "F=5 (3회+)", "F=4 (2회)", "F=3 (1회)"],
        ["R=5 (≤90일)", "🏆 Champions", "🏆 Champions", "🌱 Promising"],
        ["R=4 (91-180일)", "🏆 Champions", "🏆 Champions", "🌱 Promising"],
        ["R=3 (181-365일)", "💙 Loyal", "💙 Loyal", "⚠️ At Risk"],
        ["R=2 (366-545일)", "🔔 Need Attention", "🔔 Need Attention", "😴 Hibernating"],
        ["R=1 (546일+)", "🔔 Need Attention", "🔔 Need Attention", "😴 Hibernating"]
    ]
    
    matrix_df = pd.DataFrame(matrix_data[1:], columns=matrix_data[0])
    st.dataframe(matrix_df, hide_index=True, use_container_width=True)

# ============================================
# 페이지 4: 세그먼트 분석
# ============================================
elif pages[selected_page] == "segment":
    st.markdown("""
    <div class="main-header">
        <h1>👥 세그먼트 분석</h1>
        <p>6개 고객 세그먼트의 특성, 규모, 매출 기여도 분석</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 세그먼트 개요 시각화
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            segment_data,
            x='segment',
            y='user_count',
            color='segment',
            title='세그먼트별 고객 수',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            segment_data,
            x='segment',
            y='avg_monetary',
            color='segment',
            title='세그먼트별 평균 LTV ($)',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 세그먼트 상세
    st.subheader("📋 세그먼트 상세 분석")
    
    # Champions
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        <div class="segment-card segment-champions">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0;">🏆 Champions</h3>
                <span style="background: #10b981; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem;">9.35%</span>
            </div>
            <p style="color: #6b7280; margin: 0.5rem 0;">최근 활동 + 2회 이상 구매 (R≥4 & F≥4)</p>
            <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 1rem 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div>
                    <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">고객 수</p>
                    <p style="font-size: 1.5rem; font-weight: 700; margin: 0;">2,787명</p>
                </div>
                <div>
                    <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">매출 기여</p>
                    <p style="font-size: 1.5rem; font-weight: 700; margin: 0; color: #10b981;">17.25%</p>
                </div>
                <div>
                    <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">평균 LTV</p>
                    <p style="font-size: 1.5rem; font-weight: 700; margin: 0;">$189.56</p>
                </div>
                <div>
                    <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">평균 Recency</p>
                    <p style="font-size: 1.5rem; font-weight: 700; margin: 0;">80.4일</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="segment-card segment-promising">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0;">🌱 Promising</h3>
                <span style="background: #8b5cf6; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem;">28.35%</span>
            </div>
            <p style="color: #6b7280; margin: 0.5rem 0;">최근 활동 + 1회 구매 (R≥4 & F=3)</p>
            <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 1rem 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div>
                    <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">고객 수</p>
                    <p style="font-size: 1.5rem; font-weight: 700; margin: 0;">8,446명</p>
                </div>
                <div>
                    <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">매출 기여</p>
                    <p style="font-size: 1.5rem; font-weight: 700; margin: 0; color: #8b5cf6;">23.56%</p>
                </div>
                <div>
                    <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">평균 LTV</p>
                    <p style="font-size: 1.5rem; font-weight: 700; margin: 0;">$85.45</p>
                </div>
                <div>
                    <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">평균 Recency</p>
                    <p style="font-size: 1.5rem; font-weight: 700; margin: 0;">84.9일</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        <div class="segment-card segment-risk">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0;">⚠️ At Risk</h3>
                <span style="background: #f97316; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem;">22.28%</span>
            </div>
            <p style="color: #6b7280; margin: 0.5rem 0;">이탈 위험 (R=3 & F=3)</p>
            <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 1rem 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div>
                    <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">고객 수</p>
                    <p style="font-size: 1.5rem; font-weight: 700; margin: 0;">6,637명</p>
                </div>
                <div>
                    <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">매출 기여</p>
                    <p style="font-size: 1.5rem; font-weight: 700; margin: 0; color: #f97316;">18.49%</p>
                </div>
                <div>
                    <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">평균 LTV</p>
                    <p style="font-size: 1.5rem; font-weight: 700; margin: 0;">$85.36</p>
                </div>
                <div>
                    <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">평균 Recency</p>
                    <p style="font-size: 1.5rem; font-weight: 700; margin: 0; color: #f97316;">270.2일</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="segment-card segment-hibernating">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0;">😴 Hibernating</h3>
                <span style="background: #6b7280; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem;">32.58%</span>
            </div>
            <p style="color: #6b7280; margin: 0.5rem 0;">장기 휴면 (R≤2 & F=3)</p>
            <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 1rem 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div>
                    <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">고객 수</p>
                    <p style="font-size: 1.5rem; font-weight: 700; margin: 0;">9,707명</p>
                </div>
                <div>
                    <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">매출 기여</p>
                    <p style="font-size: 1.5rem; font-weight: 700; margin: 0; color: #6b7280;">27.37%</p>
                </div>
                <div>
                    <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">평균 LTV</p>
                    <p style="font-size: 1.5rem; font-weight: 700; margin: 0;">$86.38</p>
                </div>
                <div>
                    <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">평균 Recency</p>
                    <p style="font-size: 1.5rem; font-weight: 700; margin: 0; color: #ef4444;">538.5일</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # RFM 스코어 레이더 차트
    st.subheader("📊 세그먼트별 RFM 프로필")
    
    categories = ['R Score', 'F Score', 'M Score']
    
    fig = go.Figure()
    
    colors = ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#f97316', '#6b7280']
    
    for i, row in segment_data.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row['r_score'], row['f_score'], row['m_score']],
            theta=categories,
            fill='toself',
            name=row['segment'],
            line_color=colors[i],
            opacity=0.7
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 5])
        ),
        showlegend=True,
        title="세그먼트별 RFM 스코어 비교",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# 페이지 5: Promising 전환 분석
# ============================================
elif pages[selected_page] == "promising":
    st.markdown("""
    <div class="main-header">
        <h1>🌱 Promising 전환 분석</h1>
        <p>신규 고객의 Champions 전환 요인 및 이탈 원인 분석</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 핵심 문제
    st.markdown("""
    <div class="insight-box danger">
        <div class="insight-title">🚨 핵심 문제: Promising 이탈 위기</div>
        <div class="insight-text">
            Promising 세그먼트(8,446명)의 <b>70.07%(5,918명)</b>이 첫 구매 후 
            사이트에 <b>단 한 번도 재방문하지 않음</b>. 이들의 평균 LTV는 $59.93으로,
            재방문 고객($146.74) 대비 <b>59% 낮음</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 구매 후 활동 분석
    st.subheader("📊 구매 후 활동 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            promising_activity,
            values='pct',
            names='activity',
            title='Promising 구매 후 활동 분포',
            color_discrete_sequence=['#ef4444', '#fbbf24', '#10b981', '#3b82f6']
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            promising_activity,
            x='activity',
            y='avg_monetary',
            title='활동 수준별 평균 LTV',
            color='avg_monetary',
            color_continuous_scale='Greens'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box success">
        <div class="insight-title">💡 인사이트: 활동량과 LTV의 강한 상관관계</div>
        <div class="insight-text">
            구매 후 4-5회 세션 방문자의 평균 LTV는 <b>$238.28</b>로, 
            무활동 고객($59.93) 대비 <b>4배 높음</b>.
            단 1회 재방문만으로도 LTV가 <b>2배</b>($118.36) 증가.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 첫 구매 타이밍 분석
    st.subheader("⏰ 가입-첫구매 타이밍의 영향")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            timing_data,
            x='timing',
            y='repurchase_rate',
            title='첫 구매 타이밍별 재구매율 (%)',
            color='repurchase_rate',
            color_continuous_scale='Blues'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            timing_data,
            x='timing',
            y='champions_rate',
            title='첫 구매 타이밍별 Champions 전환율 (%)',
            color='champions_rate',
            color_continuous_scale='Greens'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box warning">
        <div class="insight-title">⚡ 인사이트: 빠른 첫 구매 = 높은 전환율</div>
        <div class="insight-text">
            가입 후 <b>1주일 내</b> 첫 구매 고객의 재구매율은 <b>26.06%</b>, Champions 전환율은 <b>16.94%</b>로,
            3개월+ 고객(15.79%, 8.57%) 대비 각각 <b>65%, 98% 높음</b>.<br><br>
            <b>시사점:</b> 신규 가입 후 7일 이내 첫 구매를 유도하는 캠페인이 효과적
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 액션 플랜
    st.subheader("🎯 Promising 전환 전략")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="action-box">
            <div class="action-header">
                <div class="action-icon" style="background: #dcfce7;">📧</div>
                <div class="action-title">Day 1-3-7 이메일 시퀀스</div>
            </div>
            <div class="action-content">
                <p><b>Day 1:</b> 구매 감사 + 관련 상품 추천</p>
                <p><b>Day 3:</b> 리뷰 요청 + 10% 재구매 쿠폰</p>
                <p><b>Day 7:</b> 미방문 시 긴급 할인 알림</p>
                <p style="color: #10b981; margin-top: 1rem;"><b>예상 효과:</b> 재방문율 +15%p</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="action-box">
            <div class="action-header">
                <div class="action-icon" style="background: #e0f2fe;">🎁</div>
                <div class="action-title">첫 구매 후 재방문 인센티브</div>
            </div>
            <div class="action-content">
                <p><b>대상:</b> 첫 구매 후 7일 내 미재방문 고객</p>
                <p><b>혜택:</b> 무료배송 + 15% 할인 콤보</p>
                <p><b>조건:</b> 14일 내 사용 시에만 적용</p>
                <p style="color: #10b981; margin-top: 1rem;"><b>예상 효과:</b> 이탈률 70% → 55%</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# 페이지 6: Champions 행동 분석
# ============================================
elif pages[selected_page] == "champions":
    st.markdown("""
    <div class="main-header">
        <h1>🏆 Champions 행동 분석</h1>
        <p>최고 가치 고객의 구매 패턴 및 재구매 타이밍 분석</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Champions 프로필
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card green">
            <div class="metric-value">2,787</div>
            <div class="metric-label">Champions 수</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card green">
            <div class="metric-value">$189.56</div>
            <div class="metric-label">평균 LTV</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card green">
            <div class="metric-value">17.25%</div>
            <div class="metric-label">매출 기여도</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card green">
            <div class="metric-value">2.22회</div>
            <div class="metric-label">평균 구매 횟수</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 재구매 타이밍 분석
    st.subheader("⏰ 재구매 타이밍 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            repurchase_timing,
            x='bucket',
            y='pct',
            title='1차→2차 구매 간격 분포 (%)',
            color='pct',
            color_continuous_scale='Purples'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            repurchase_timing,
            x='avg_days',
            y='avg_ltv',
            size='count',
            color='bucket',
            title='재구매 타이밍 vs LTV',
            labels={'avg_days': '평균 재구매 일수', 'avg_ltv': '평균 LTV ($)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box success">
        <div class="insight-title">💡 인사이트: 빠른 재구매 = 높은 LTV</div>
        <div class="insight-text">
            <b>1주 내</b> 재구매 Champions의 평균 LTV는 <b>$225.77</b>로,
            3개월+ 재구매자($186.72) 대비 <b>20.9% 높음</b>.<br>
            그러나 전체 Champions의 <b>73%</b>가 3개월 이상 소요되어 재구매.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 전환 속도별 활동 분석
    st.subheader("📊 전환 속도별 구매 간 활동")
    
    conversion_speed = pd.DataFrame([
        {"speed": "Quick (≤30일)", "count": 265, "avg_ltv": 206.77, "avg_sessions": 0.7},
        {"speed": "Medium (31-60일)", "count": 239, "avg_ltv": 189.17, "avg_sessions": 0.8},
        {"speed": "Slow (61일+)", "count": 2283, "avg_ltv": 187.61, "avg_sessions": 0.8}
    ])
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            conversion_speed,
            x='speed',
            y='count',
            title='전환 속도별 Champions 수',
            color='count',
            color_continuous_scale='Oranges'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            conversion_speed,
            x='speed',
            y='avg_ltv',
            title='전환 속도별 평균 LTV ($)',
            color='avg_ltv',
            color_continuous_scale='Greens'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box warning">
        <div class="insight-title">⚡ 인사이트: 빠른 전환자의 행동 특성</div>
        <div class="insight-text">
            Quick 전환자(30일 이내)는 구매 사이 평균 <b>0.7회</b> 세션만 기록,
            이는 <b>즉각적인 구매 결정</b>을 내리는 고객임을 시사.<br>
            반면 Slow 전환자는 더 많은 탐색(0.8회)을 하지만 LTV는 낮음.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Champions 전략
    st.subheader("🎯 Champions 유지 전략")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="action-box">
            <div class="action-header">
                <div class="action-icon" style="background: #fef3c7;">👑</div>
                <div class="action-title">VIP 프로그램</div>
            </div>
            <div class="action-content">
                <p><b>대상:</b> M Score 4+ Champions (상위 25%)</p>
                <p><b>혜택:</b></p>
                <ul style="margin: 0.5rem 0; padding-left: 1.2rem;">
                    <li>신상품 Early Access</li>
                    <li>전용 고객센터</li>
                    <li>생일 특별 할인 30%</li>
                </ul>
                <p style="color: #10b981;"><b>예상 효과:</b> LTV +15%</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="action-box">
            <div class="action-header">
                <div class="action-icon" style="background: #e0e7ff;">⏰</div>
                <div class="action-title">재구매 타이밍 캠페인</div>
            </div>
            <div class="action-content">
                <p><b>대상:</b> 마지막 구매 후 60일 경과 Champions</p>
                <p><b>액션:</b></p>
                <ul style="margin: 0.5rem 0; padding-left: 1.2rem;">
                    <li>개인화된 상품 추천</li>
                    <li>한정 시간 할인 (48시간)</li>
                    <li>무료배송 쿠폰</li>
                </ul>
                <p style="color: #10b981;"><b>예상 효과:</b> 재구매 주기 단축 20%</p>
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
        <p>유입 채널 및 첫 구매 카테고리별 고객 품질 분석</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 채널별 전환율
    st.subheader("📊 채널별 Champions 전환율")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            channel_data.sort_values('conversion_rate', ascending=True),
            x='conversion_rate',
            y='channel',
            orientation='h',
            title='채널별 Champions 전환율 (%)',
            color='conversion_rate',
            color_continuous_scale='Greens'
        )
        fig.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            channel_data,
            x='channel',
            y=['promising', 'champions'],
            title='채널별 세그먼트 분포',
            barmode='group',
            color_discrete_sequence=['#8b5cf6', '#10b981']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box success">
        <div class="insight-title">✅ 인사이트: Email 채널이 최고 품질</div>
        <div class="insight-text">
            Email 채널의 Champions 전환율은 <b>27.13%</b>로 전 채널 중 최고.
            Organic(23.12%) 대비 <b>+4%p</b> 높은 전환율.<br>
            <b>시사점:</b> Email 마케팅 비중 확대 및 Newsletter 구독 유도 필요.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 카테고리별 전환율
    st.subheader("👗 카테고리별 Champions 전환율")
    
    category_conversion = pd.DataFrame([
        {"category": "Clothing Sets", "conversion_rate": 41.67, "avg_ltv": 231.84},
        {"category": "Jumpsuits & Rompers", "conversion_rate": 29.51, "avg_ltv": 136.60},
        {"category": "Plus", "conversion_rate": 28.40, "avg_ltv": 161.37},
        {"category": "Accessories", "conversion_rate": 28.38, "avg_ltv": 180.63},
        {"category": "Suits", "conversion_rate": 27.42, "avg_ltv": 234.22},
        {"category": "Blazers & Jackets", "conversion_rate": 27.62, "avg_ltv": 211.27},
        {"category": "Outerwear & Coats", "conversion_rate": 26.96, "avg_ltv": 292.54},
    ])
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            category_conversion.sort_values('conversion_rate', ascending=True),
            x='conversion_rate',
            y='category',
            orientation='h',
            title='카테고리별 Champions 전환율 (%)',
            color='conversion_rate',
            color_continuous_scale='Blues'
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            category_conversion,
            x='conversion_rate',
            y='avg_ltv',
            size='avg_ltv',
            color='category',
            title='전환율 vs LTV',
            labels={'conversion_rate': '전환율 (%)', 'avg_ltv': '평균 LTV ($)'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box warning">
        <div class="insight-title">💡 인사이트: 고가 카테고리의 높은 LTV</div>
        <div class="insight-text">
            <b>Outerwear & Coats</b>로 첫 구매한 고객의 평균 LTV는 <b>$292.54</b>로 최고.
            전환율(26.96%)도 상위권으로, <b>고가 아이템 첫 구매 유도가 효과적</b>.<br>
            반면 Clothing Sets는 전환율(41.67%)이 가장 높지만 샘플 수가 적어 주의 필요.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 채널×카테고리 히트맵
    st.subheader("🗺️ 채널 × 카테고리 LTV 히트맵")
    
    # 히트맵 데이터
    heatmap_data = pd.DataFrame({
        'Email': [287.38, 145.06, 147.13, 176.32, 147.07],
        'Facebook': [313.49, 211.36, 142.48, 200.25, 211.55],
        'Search': [266.62, 260.71, 156.94, 208.86, 185.25],
        'Display': [211.96, 199.41, None, 155.30, 148.38],
        'Organic': [307.85, 171.98, 228.45, 229.55, 187.61]
    }, index=['Outerwear', 'Jeans', 'Accessories', 'Sweaters', 'Sleep & Lounge'])
    
    fig = px.imshow(
        heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        color_continuous_scale='RdYlGn',
        title='채널 × 카테고리별 평균 LTV ($)',
        labels=dict(color="LTV ($)")
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">🎯 최적 채널×카테고리 조합</div>
        <div class="insight-text">
            <b>Top 3 조합:</b><br>
            1. Facebook × Outerwear: <b>$313.49</b><br>
            2. Organic × Outerwear: <b>$307.85</b><br>
            3. Email × Outerwear: <b>$287.38</b><br><br>
            <b>시사점:</b> Outerwear 카테고리의 광고 타겟팅 강화
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 페이지 8: Action Plan
# ============================================
elif pages[selected_page] == "action":
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Action Plan</h1>
        <p>RFM 분석 기반 세그먼트별 마케팅 전략 및 실행 로드맵</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Phase 1
    st.subheader("📅 Phase 1: Promising 리텐션 (Week 1-2)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="action-box" style="border-color: #8b5cf6;">
            <div class="action-header">
                <div class="action-icon" style="background: #ede9fe; color: #8b5cf6;">🌱</div>
                <div class="action-title">구매 후 이메일 시퀀스</div>
            </div>
            <div class="action-content">
                <p><b>목표:</b> Promising 이탈률 70% → 55%</p>
                <hr style="margin: 1rem 0;">
                <p><b>Day 1:</b> 구매 감사 + 연관 상품 추천</p>
                <p><b>Day 3:</b> 리뷰 요청 + 10% 재구매 쿠폰</p>
                <p><b>Day 7:</b> 재방문 유도 + 15% 할인</p>
                <p><b>Day 14:</b> 마지막 기회 + 무료배송</p>
                <hr style="margin: 1rem 0;">
                <p style="color: #10b981;"><b>예상 ROI:</b> +$101,000/년</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="action-box" style="border-color: #8b5cf6;">
            <div class="action-header">
                <div class="action-icon" style="background: #ede9fe; color: #8b5cf6;">⏰</div>
                <div class="action-title">신규 가입 조기 전환</div>
            </div>
            <div class="action-content">
                <p><b>목표:</b> 1주 내 첫 구매 비율 1% → 5%</p>
                <hr style="margin: 1rem 0;">
                <p><b>Welcome 이메일:</b> 가입 즉시 15% 할인 코드</p>
                <p><b>Push 알림:</b> 인기 상품 알림 (Day 1, 3)</p>
                <p><b>리타겟팅:</b> 장바구니 이탈 고객 대상</p>
                <p><b>한정 혜택:</b> 7일 내 구매 시 추가 5% 할인</p>
                <hr style="margin: 1rem 0;">
                <p style="color: #10b981;"><b>예상 ROI:</b> +$34,000/년</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Phase 2
    st.subheader("📅 Phase 2: Champions VIP 프로그램 (Week 3-4)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="action-box" style="border-color: #10b981;">
            <div class="action-header">
                <div class="action-icon" style="background: #dcfce7; color: #10b981;">👑</div>
                <div class="action-title">Champions VIP 혜택</div>
            </div>
            <div class="action-content">
                <p><b>목표:</b> Champions LTV +15%</p>
                <hr style="margin: 1rem 0;">
                <p><b>Tier 1 (M≥4):</b></p>
                <ul style="margin: 0.5rem 0; padding-left: 1.2rem;">
                    <li>신상품 48시간 Early Access</li>
                    <li>전용 고객센터 라인</li>
                    <li>연 2회 VIP 세일 (30% 할인)</li>
                </ul>
                <p><b>Tier 2 (M=3):</b></p>
                <ul style="margin: 0.5rem 0; padding-left: 1.2rem;">
                    <li>신상품 알림 우선 발송</li>
                    <li>생일 20% 할인</li>
                </ul>
                <hr style="margin: 1rem 0;">
                <p style="color: #10b981;"><b>예상 ROI:</b> +$79,000/년</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="action-box" style="border-color: #10b981;">
            <div class="action-header">
                <div class="action-icon" style="background: #dcfce7; color: #10b981;">🔄</div>
                <div class="action-title">재구매 주기 단축</div>
            </div>
            <div class="action-content">
                <p><b>목표:</b> 평균 재구매 주기 300일 → 240일</p>
                <hr style="margin: 1rem 0;">
                <p><b>D+30 알림:</b> "새로운 상품이 도착했어요"</p>
                <p><b>D+60 알림:</b> "오래 기다리셨죠?" + 쿠폰</p>
                <p><b>D+90 알림:</b> "보고 싶었어요" + 특별 할인</p>
                <p><b>개인화:</b> 이전 구매 기반 추천</p>
                <hr style="margin: 1rem 0;">
                <p style="color: #10b981;"><b>예상 효과:</b> 재구매 주기 20% 단축</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Phase 3
    st.subheader("📅 Phase 3: At Risk/Hibernating 윈백 (Month 2)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="action-box" style="border-color: #f97316;">
            <div class="action-header">
                <div class="action-icon" style="background: #ffedd5; color: #f97316;">⚠️</div>
                <div class="action-title">At Risk 윈백</div>
            </div>
            <div class="action-content">
                <p><b>대상:</b> 6,637명 (마지막 구매 181-365일)</p>
                <p><b>목표:</b> 1,000명 재활성화</p>
                <hr style="margin: 1rem 0;">
                <p><b>전략:</b></p>
                <ul style="margin: 0.5rem 0; padding-left: 1.2rem;">
                    <li>"우리가 그리웠어요" 캠페인</li>
                    <li>20% 복귀 환영 쿠폰</li>
                    <li>과거 구매 기반 개인화 추천</li>
                </ul>
                <hr style="margin: 1rem 0;">
                <p style="color: #10b981;"><b>예상 ROI:</b> +$85,000</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="action-box" style="border-color: #6b7280;">
            <div class="action-header">
                <div class="action-icon" style="background: #f3f4f6; color: #6b7280;">😴</div>
                <div class="action-title">Hibernating 재활성화</div>
            </div>
            <div class="action-content">
                <p><b>대상:</b> 9,707명 (마지막 구매 365일+)</p>
                <p><b>목표:</b> 500명 재활성화</p>
                <hr style="margin: 1rem 0;">
                <p><b>전략:</b></p>
                <ul style="margin: 0.5rem 0; padding-left: 1.2rem;">
                    <li>"많이 달라졌어요" 신상품 소개</li>
                    <li>30% 복귀 특별 할인</li>
                    <li>무료배송 + 반품 무료</li>
                </ul>
                <hr style="margin: 1rem 0;">
                <p style="color: #10b981;"><b>예상 ROI:</b> +$43,000</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 채널 전략
    st.subheader("📢 채널 최적화 전략")
    
    st.markdown("""
    <div class="action-box" style="border-color: #3b82f6;">
        <div class="action-header">
            <div class="action-icon" style="background: #dbeafe; color: #3b82f6;">📧</div>
            <div class="action-title">Email 채널 강화</div>
        </div>
        <div class="action-content">
            <p><b>현황:</b> Email 전환율 27.13% (최고) but 비중은 5% 미만</p>
            <p><b>목표:</b> Email 마케팅 비중 5% → 15%</p>
            <hr style="margin: 1rem 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div>
                    <p><b>액션:</b></p>
                    <ul style="margin: 0.5rem 0; padding-left: 1.2rem;">
                        <li>Newsletter 구독 팝업 강화</li>
                        <li>구독 시 15% 할인 제공</li>
                        <li>개인화된 콘텐츠 발송</li>
                    </ul>
                </div>
                <div>
                    <p><b>예상 효과:</b></p>
                    <ul style="margin: 0.5rem 0; padding-left: 1.2rem;">
                        <li>+312명 Champions</li>
                        <li>+$53,000/년 매출</li>
                        <li>CAC 20% 절감</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # KPI 대시보드
    st.subheader("📈 KPI 모니터링")
    
    kpi_data = pd.DataFrame({
        "KPI": ["Promising 이탈률", "Champions 비율", "평균 LTV", "재구매율", "Email 전환율"],
        "현재": ["70.07%", "9.35%", "$102.82", "16.85%", "27.13%"],
        "목표 (6개월)": ["55%", "12%", "$120", "22%", "35%"],
        "목표 (1년)": ["45%", "15%", "$140", "28%", "35%"]
    })
    
    st.dataframe(kpi_data, hide_index=True, use_container_width=True)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # ROI 계산 로직 상세
    st.subheader("🧮 ROI 계산 로직")
    
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">📐 ROI 산출 방법론</div>
        <div class="insight-text">
            모든 ROI는 <b>실제 분석 데이터 기반</b>으로 보수적인 가정 하에 산출되었습니다.
            업계 평균 캠페인 성공률과 TheLook 데이터의 전환율을 혼합 적용했습니다.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Phase 1 ROI 계산
    with st.expander("📊 Phase 1: Promising 리텐션 ROI 계산", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🌱 구매 후 이메일 시퀀스 (+$101,000)**
            
            | 항목 | 수치 | 근거 |
            |------|------|------|
            | Promising 총 고객 | 8,446명 | RFM 분석 결과 |
            | 현재 이탈률 | 70.07% | 재방문 없는 비율 |
            | 목표 이탈률 | 55% | 업계 평균 기준 |
            | 이탈 감소 | 15%p | 70% → 55% |
            | 추가 유지 고객 | **1,267명** | 8,446 × 15% |
            | 재구매 시 추가 수익 | $80/인 | avg_monetary 기준 |
            | **예상 ROI** | **$101,360** | 1,267 × $80 |
            """)
        
        with col2:
            st.markdown("""
            **⏰ 신규 가입 조기 전환 (+$34,000)**
            
            | 항목 | 수치 | 근거 |
            |------|------|------|
            | 연간 신규 가입자 | ~15,000명 | 2년간 29,795명 기준 |
            | 현재 1주 내 구매 | 1% (150명) | timing 분석 결과 |
            | 목표 1주 내 구매 | 5% (750명) | 캠페인 효과 가정 |
            | 추가 조기 전환자 | **600명** | 750 - 150 |
            | LTV 차이 | +$11/인 | $112 vs $101 |
            | Champions 전환 차이 | 8.4%p | 16.94% vs 8.57% |
            | 추가 Champions | 50명 | 600 × 8.4% |
            | **예상 ROI** | **$34,050** | 600×$11 + 50×$189×2 |
            """)
    
    # Phase 2 ROI 계산
    with st.expander("📊 Phase 2: Champions VIP ROI 계산"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **👑 Champions VIP 혜택 (+$79,000)**
            
            | 항목 | 수치 | 근거 |
            |------|------|------|
            | Champions 총 고객 | 2,787명 | RFM 분석 결과 |
            | 현재 평균 LTV | $189.56 | segment 분석 |
            | LTV 증가 목표 | +15% | VIP 프로그램 효과 |
            | 추가 수익/인 | $28.43 | $189.56 × 15% |
            | **예상 ROI** | **$79,233** | 2,787 × $28.43 |
            
            *VIP 프로그램 운영 비용 제외 Gross ROI 기준*
            """)
        
        with col2:
            st.markdown("""
            **🔄 재구매 주기 단축 (LTV 포함)**
            
            | 항목 | 수치 | 근거 |
            |------|------|------|
            | 현재 재구매 주기 | 302.4일 | 3개월+ 버킷 평균 |
            | 목표 재구매 주기 | 240일 | 20% 단축 |
            | 2년 내 추가 구매 | +0.3회/인 | 주기 단축 효과 |
            | 추가 수익/인 | ~$28 | $85 × 0.3 |
            
            *Champions VIP ROI에 포함하여 계산*
            """)
    
    # Phase 3 ROI 계산
    with st.expander("📊 Phase 3: Winback ROI 계산"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **⚠️ At Risk 윈백 (+$85,000)**
            
            | 항목 | 수치 | 근거 |
            |------|------|------|
            | At Risk 총 고객 | 6,637명 | RFM 분석 결과 |
            | 윈백 캠페인 응답률 | 15% | 업계 평균 |
            | 재활성화 목표 | **1,000명** | 6,637 × 15% |
            | 평균 LTV | $85.36 | segment 분석 |
            | **예상 ROI** | **$85,360** | 1,000 × $85.36 |
            
            *윈백 쿠폰 비용(~20%) 포함 시 Net ROI ~$68,000*
            """)
        
        with col2:
            st.markdown("""
            **😴 Hibernating 재활성화 (+$43,000)**
            
            | 항목 | 수치 | 근거 |
            |------|------|------|
            | Hibernating 총 고객 | 9,707명 | RFM 분석 결과 |
            | 윈백 캠페인 응답률 | 5% | 휴면 고객 낮은 응답률 |
            | 재활성화 목표 | **500명** | 9,707 × 5% |
            | 평균 LTV | $86.38 | segment 분석 |
            | **예상 ROI** | **$43,190** | 500 × $86.38 |
            
            *30% 할인 적용 시 Net ROI ~$30,000*
            """)
    
    # Channel ROI 계산
    with st.expander("📊 채널 최적화 ROI 계산"):
        st.markdown("""
        **📧 Email 채널 강화 (+$53,000)**
        
        | 항목 | 수치 | 근거 |
        |------|------|------|
        | 현재 Email 비중 | 5% | 575명 (Promising+Champions) |
        | 목표 Email 비중 | 15% | 3배 확대 |
        | 현재 Email Champions | 156명 | 채널 분석 결과 |
        | Email 전환율 | 27.13% | 전 채널 최고 |
        | 추가 확보 Champions | **312명** | 156 × 2 (비중 3배) |
        | Champions 평균 LTV | $170.70 | Email Champions 평균 |
        | **예상 ROI** | **$53,258** | 312 × $170.70 |
        
        **계산 로직:**
        - Email 비중을 5% → 15%로 확대하면 기존 대비 3배의 고객 유입
        - Email 채널의 높은 전환율(27.13%) 유지 가정
        - 추가 Champions 수 = 기존 156명 × (3-1) = 312명
        """)
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # 최종 ROI 요약
    st.markdown("""
    <div class="insight-box success">
        <div class="insight-title">💰 예상 총 ROI 요약</div>
        <div class="insight-text">
            <table style="width: 100%; font-size: 0.95rem;">
                <tr style="border-bottom: 2px solid #10b981;">
                    <th style="text-align: left; padding: 8px;">Phase</th>
                    <th style="text-align: right; padding: 8px;">Gross ROI</th>
                    <th style="text-align: right; padding: 8px;">Net ROI (추정)</th>
                </tr>
                <tr style="border-bottom: 1px solid #e5e7eb;">
                    <td style="padding: 8px;">Phase 1: Promising 리텐션</td>
                    <td style="text-align: right; padding: 8px;">$135,000</td>
                    <td style="text-align: right; padding: 8px;">$108,000</td>
                </tr>
                <tr style="border-bottom: 1px solid #e5e7eb;">
                    <td style="padding: 8px;">Phase 2: Champions VIP</td>
                    <td style="text-align: right; padding: 8px;">$79,000</td>
                    <td style="text-align: right; padding: 8px;">$63,000</td>
                </tr>
                <tr style="border-bottom: 1px solid #e5e7eb;">
                    <td style="padding: 8px;">Phase 3: Winback</td>
                    <td style="text-align: right; padding: 8px;">$128,000</td>
                    <td style="text-align: right; padding: 8px;">$98,000</td>
                </tr>
                <tr style="border-bottom: 1px solid #e5e7eb;">
                    <td style="padding: 8px;">Channel Optimization</td>
                    <td style="text-align: right; padding: 8px;">$53,000</td>
                    <td style="text-align: right; padding: 8px;">$42,000</td>
                </tr>
                <tr style="background: #ecfdf5;">
                    <td style="padding: 12px; font-weight: 700;">Total</td>
                    <td style="text-align: right; padding: 12px; font-weight: 700; color: #10b981;">$395,000</td>
                    <td style="text-align: right; padding: 12px; font-weight: 700; color: #10b981;">$311,000</td>
                </tr>
            </table>
            <p style="margin-top: 1rem; font-size: 0.85rem; color: #6b7280;">
                * Net ROI = Gross ROI - 예상 캠페인 비용 (쿠폰, 할인, 운영비 등 약 20% 가정)<br>
                * 현재 총 매출 $3,063,495 대비 <b>+12.9% 성장</b> (Gross 기준)
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 푸터
# ============================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #9ca3af; font-size: 0.85rem; padding: 2rem 0; border-top: 1px solid #e5e7eb;">
    <p>TheLook E-commerce RFM 분석 포트폴리오</p>
    <p>분석 기간: 2023.01 - 2024.12 | 데이터: BigQuery thelook_ecommerce</p>
    <p style="margin-top: 0.5rem;">Built with Streamlit & Plotly</p>
</div>
""", unsafe_allow_html=True)