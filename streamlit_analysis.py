import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="TheLook CRM Strategy | Data Portfolio",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Look
st.markdown("""
<style>
    /* Global Font & Layout */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        color: #0F172A;
        font-weight: 700;
    }
    h4 {
        color: #334155;
        font-weight: 600;
    }
    
    /* Custom Metric Card */
    div.css-1r6slb0.e1tzin5v2 {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }

    /* KPI Card Style */
    .kpi-card {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.04);
        border: 1px solid #F1F5F9;
        text-align: center;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: bold;
        color: #2563EB;
        margin: 10px 0;
    }
    .kpi-label {
        color: #64748B;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Insight Box */
    .insight-box {
        background-color: #F8FAFC;
        border-left: 4px solid #3B82F6;
        padding: 16px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
    }
    .insight-title {
        font-weight: bold;
        color: #1E40AF;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        font-size: 16px;
    }
    
    /* Strategy Action Card */
    .action-card {
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 8px;
        padding: 20px;
        margin-top: 10px;
    }
    .action-title {
        color: #166534;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Data Loading (Embedded JSON from BigQuery Results)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    # 2.1 Post Purchase Activity (Retention Drop-off)
    data_post_activity = [
        {"activity_level": "0. No Activity (이탈)", "user_count": 3287, "pct": 70.78, "desc": "구매 후 즉시 이탈"},
        {"activity_level": "1. 1 Session", "user_count": 374, "pct": 8.05, "desc": "최소한의 관심"},
        {"activity_level": "2. 2-3 Sessions", "user_count": 886, "pct": 19.08, "desc": "재방문 유저"},
        {"activity_level": "3. 4+ Sessions", "user_count": 97, "pct": 2.09, "desc": "적극적 탐색"}
    ]

    # 2.2 Champions Time to 2nd Purchase (Golden Time)
    data_time_bucket = [
        {"time_bucket": "1주 이내", "pct": 2.41, "cumulative_pct": 2.41, "avg_days": 3.6},
        {"time_bucket": "2주 이내", "pct": 2.72, "cumulative_pct": 5.13, "avg_days": 11.0},
        {"time_bucket": "1개월 이내", "pct": 4.57, "cumulative_pct": 9.7, "avg_days": 23.5},
        {"time_bucket": "2개월 이내", "pct": 8.71, "cumulative_pct": 18.41, "avg_days": 44.8},
        {"time_bucket": "3개월 이내", "pct": 9.08, "cumulative_pct": 27.49, "avg_days": 75.4},
        {"time_bucket": "3개월 이후", "pct": 72.51, "cumulative_pct": 100.0, "avg_days": 309.0}
    ]

    # 2.4 Category Pairs (Cross-selling)
    data_category_pairs = [
        {"first_category": "Shorts", "second_category": "Tops & Tees", "pair_count": 21, "affinity_score": 95},
        {"first_category": "Sweaters", "second_category": "Jeans", "pair_count": 20, "affinity_score": 90},
        {"first_category": "Tops & Tees", "second_category": "Sleep & Lounge", "pair_count": 19, "affinity_score": 85},
        {"first_category": "Accessories", "second_category": "Tops & Tees", "pair_count": 17, "affinity_score": 75},
        {"first_category": "Jeans", "second_category": "Sleep & Lounge", "pair_count": 14, "affinity_score": 60}
    ]

    # 2.6 RFM Segments
    data_rfm_segments = [
        {"customer_segment": "Hibernating", "user_count": 9707, "pct": 32.58, "revenue_contribution_pct": 27.21, "strategy": "Win-back or Ignore"},
        {"customer_segment": "Promising", "user_count": 8446, "pct": 28.35, "revenue_contribution_pct": 23.73, "strategy": "Nurture to Loyal"},
        {"customer_segment": "At Risk", "user_count": 6637, "pct": 22.28, "revenue_contribution_pct": 18.75, "strategy": "Prevent Churn"},
        {"customer_segment": "Champions", "user_count": 2787, "pct": 9.35, "revenue_contribution_pct": 17.1, "strategy": "Reward & VIP"},
        {"customer_segment": "Loyal Customers", "user_count": 1357, "pct": 4.55, "revenue_contribution_pct": 8.22, "strategy": "Upsell"},
        {"customer_segment": "Need Attention", "user_count": 861, "pct": 2.89, "revenue_contribution_pct": 5.0, "strategy": "Re-activation"}
    ]

    # 2.7 Repurchase Timing (Cohort Analysis)
    data_repurchase = [
        {"first_purchase_timing": "D+0 ~ D+7 (Golden Time)", "repurchase_rate": 26.06, "lift": "+10.2%p"},
        {"first_purchase_timing": "D+8 ~ D+30", "repurchase_rate": 25.08, "lift": "+9.3%p"},
        {"first_purchase_timing": "D+31 ~ D+60", "repurchase_rate": 24.63, "lift": "+8.8%p"},
        {"first_purchase_timing": "D+61 ~ D+90", "repurchase_rate": 23.63, "lift": "+7.8%p"},
        {"first_purchase_timing": "D+91 +", "repurchase_rate": 15.79, "lift": "Baseline"}
    ]
    
    # 2.8 Champions First Category (Gateway Products)
    data_champ_cat = [
        {"category": "Accessories", "conversion_pct": 28.38, "avg_value": 42.72, "potential": "High"},
        {"category": "Outerwear & Coats", "conversion_pct": 26.96, "avg_value": 151.77, "potential": "High"},
        {"category": "Plus", "conversion_pct": 28.40, "avg_value": 52.12, "potential": "High"},
        {"category": "Jeans", "conversion_pct": 25.20, "avg_value": 97.47, "potential": "Medium"},
        {"category": "Swim", "conversion_pct": 24.16, "avg_value": 55.47, "potential": "Medium"},
        {"category": "Tops & Tees", "conversion_pct": 24.45, "avg_value": 44.24, "potential": "Medium"}
    ]

    # 2.9 Traffic Source LTV
    data_ltv = [
        {"source": "Organic", "category": "Outerwear", "avg_ltv": 452.22, "roi_index": 100},
        {"source": "Organic", "category": "Tops & Tees", "avg_ltv": 419.65, "roi_index": 92},
        {"source": "Search", "category": "Suits", "avg_ltv": 378.35, "roi_index": 83},
        {"source": "Facebook", "category": "Hoodies", "avg_ltv": 370.73, "roi_index": 81},
        {"source": "Search", "category": "Jeans", "avg_ltv": 337.21, "roi_index": 74}
    ]

    return {
        "post_activity": pd.DataFrame(data_post_activity),
        "time_bucket": pd.DataFrame(data_time_bucket),
        "category_pairs": pd.DataFrame(data_category_pairs),
        "rfm_segments": pd.DataFrame(data_rfm_segments),
        "repurchase": pd.DataFrame(data_repurchase),
        "champ_cat": pd.DataFrame(data_champ_cat),
        "ltv": pd.DataFrame(data_ltv)
    }

dfs = load_data()

# -----------------------------------------------------------------------------
# 3. Sidebar Navigation
# -----------------------------------------------------------------------------
st.sidebar.title("📑 분석 리포트 목차")
menu = st.sidebar.radio("Go to", 
    ["1. Executive Summary", 
     "2. 고객 세분화 (RFM Analysis)", 
     "3. 이탈 방어 및 골든타임", 
     "4. 챔피언 고객 육성 전략", 
     "5. 최종 결론 (Action Plan)"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='background-color:#F1F5F9; padding:10px; border-radius:5px;'>
    <strong>📊 Data Scope</strong><br>
    <span style='font-size:12px; color:#64748B;'>
    • Source: TheLook eCommerce<br>
    • Period: 2023.01 ~ 2024.12<br>
    • Users: 29,795 IDs
    </span>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. Page Content
# -----------------------------------------------------------------------------

# ==========================================
# PAGE 1: Executive Summary
# ==========================================
if menu == "1. Executive Summary":
    st.markdown("### 🚀 TheLook eCommerce CRM 성장 전략")
    st.markdown("**부제: 데이터 기반의 이탈 방어 및 고가치 고객(Champions) 육성 로드맵**")
    
    st.markdown("---")
    
    # 1. Key Metrics Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Total Users</div>
            <div class="kpi-value">29,795</div>
            <div style="color:green; font-size:12px;">Data for 2 Years</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Avg Repurchase Rate</div>
            <div class="kpi-value">15.8%</div>
            <div style="color:red; font-size:12px;">⚠️ Industry Avg: 20-30%</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Initial Churn Rate</div>
            <div class="kpi-value">70.8%</div>
            <div style="color:red; font-size:12px;">Left after 1st Order</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Champion Revenue %</div>
            <div class="kpi-value">17.1%</div>
            <div style="color:blue; font-size:12px;">From Top 9% Users</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Problem & Hypothesis
    st.subheader("📌 문제 정의 및 핵심 발견")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        <div class="insight-box">
        <div class="insight-title">🚨 Problem: "밑 빠진 독" (Leaky Bucket)</div>
        신규 유입은 지속되지만, <strong>첫 구매자의 70%가 재방문 없이 이탈</strong>합니다.
        고객 획득 비용(CAC) 효율을 높이기 위해서는 획득보다는 <strong>유지(Retention)</strong>에 집중해야 할 때입니다.
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="insight-box">
        <div class="insight-title">💡 Insight: "7일의 골든타임"</div>
        데이터 분석 결과, <strong>가입 후 7일 이내</strong>에 첫 구매를 완료한 고객의 재구매율이
        평균 대비 <strong>10%p 이상</strong> 높았습니다. 초기 7일의 경험 관리가 LTV의 핵심입니다.
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# PAGE 2: RFM Segmentation
# ==========================================
elif menu == "2. 고객 세분화 (RFM Analysis)":
    st.title("👥 고객 가치 기반 세분화 (RFM)")
    st.markdown("전체 고객을 Recency(최신성), Frequency(빈도), Monetary(금액) 기준으로 6개 그룹으로 분류했습니다.")
    
    # 1. Pareto Chart
    df_rfm = dfs["rfm_segments"]
    
    st.subheader("1. 파레토 법칙의 확인: 20%의 고객이 매출을 주도")
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(
            x=df_rfm['customer_segment'], 
            y=df_rfm['pct'], 
            name="고객 수 비율 (%)",
            marker_color='#CBD5E1',
            text=df_rfm['pct'],
            textposition='auto'
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=df_rfm['customer_segment'], 
            y=df_rfm['revenue_contribution_pct'], 
            name="매출 기여도 (%)",
            mode='lines+markers+text',
            text=df_rfm['revenue_contribution_pct'],
            textposition='top center',
            line=dict(color='#2563EB', width=3),
            marker=dict(size=8)
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        title="<b>Segment Size vs Revenue Contribution</b>",
        template="plotly_white",
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor='center'),
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
    <strong>📊 데이터 해석:</strong><br>
    <ul>
        <li><strong>High Value (Champions + Loyal):</strong> 전체 유저의 약 14%에 불과하지만, 전체 매출의 <strong>25% 이상</strong>을 책임집니다.</li>
        <li><strong>Potential (Promising):</strong> 28.3%를 차지하는 '유망주' 그룹입니다. 최근 가입하여 1회 구매한 이들을 2회 구매로 유도하는 것이 성장의 열쇠입니다.</li>
        <li><strong>Lost (Hibernating):</strong> 32%의 유저는 이미 장기 이탈 상태입니다. 이들에게 예산을 쓰기보다 Promising 그룹 육성에 집중해야 합니다.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("2. 세그먼트별 전략 테이블")
    st.dataframe(
        df_rfm[['customer_segment', 'pct', 'revenue_contribution_pct', 'strategy']],
        column_config={
            "customer_segment": "세그먼트",
            "pct": st.column_config.ProgressColumn(
                "고객 비중", format="%.1f%%", min_value=0, max_value=40
            ),
            "revenue_contribution_pct": st.column_config.NumberColumn(
                "매출 기여도", format="%.1f%%"
            ),
            "strategy": "핵심 대응 전략"
        },
        hide_index=True,
        use_container_width=True
    )

# ==========================================
# PAGE 3: Churn & Golden Time
# ==========================================
elif menu == "3. 이탈 방어 및 골든타임":
    st.title("⏳ 이탈 방어와 골든 타임 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚨 초기 이탈률 현황")
        st.write("첫 구매 후 세션(방문) 횟수 분포")
        
        df_act = dfs["post_activity"]
        fig_donut = px.pie(
            df_act, values='pct', names='activity_level', hole=0.6,
            color_discrete_sequence=['#EF4444', '#FCD34D', '#60A5FA', '#3B82F6']
        )
        fig_donut.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.1))
        fig_donut.update_traces(textinfo='percent')
        st.plotly_chart(fig_donut, use_container_width=True)
        
        st.caption("해석: 70.8%의 고객은 구매 후 배송 조회 등을 위해 다시 방문하지도 않음.")

    with col2:
        st.subheader("🔑 골든 타임의 발견")
        st.write("가입 후 첫 구매 시점에 따른 재구매율 차이")
        
        df_re = dfs["repurchase"]
        fig_bar = px.bar(
            df_re, x='first_purchase_timing', y='repurchase_rate',
            color='repurchase_rate',
            color_continuous_scale='Blues',
            text='repurchase_rate'
        )
        fig_bar.update_layout(xaxis_title="첫 구매 소요 기간", yaxis_title="재구매율 (%)", coloraxis_showscale=False)
        st.plotly_chart(fig_bar, use_container_width=True)
        
    st.markdown("""
    <div class="insight-box">
    <div class="insight-title">💡 Insight: Speed Matters</div>
    고객이 <strong>가입 후 7일 이내</strong>에 첫 구매를 경험하게 하면, 재구매율이 <strong>26%</strong>까지 상승합니다.
    하지만 3개월이 지난 뒤 첫 구매를 한 경우 재구매율은 15%대로 급락합니다.
    <br><br>
    <strong>👉 결론: 신규 가입자의 '첫 구매'를 앞당기는 것이 LTV 상승의 지름길입니다.</strong>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# PAGE 4: Champions Strategy
# ==========================================
elif menu == "4. 챔피언 고객 육성 전략":
    st.title("🏆 Champions 육성 로드맵")
    st.markdown("우리 브랜드의 충성 고객(Champions)은 어떤 경로로 성장했는지 분석했습니다.")
    
    # 1. Gateway Products
    st.subheader("1. Gateway Product (챔피언 입문 상품)")
    st.write("어떤 카테고리로 첫 구매를 시작해야 챔피언이 될 확률이 높을까요?")
    
    df_champ = dfs["champ_cat"].sort_values(by="conversion_pct", ascending=False)
    
    st.dataframe(
        df_champ,
        column_config={
            "category": "첫 구매 카테고리",
            "conversion_pct": st.column_config.NumberColumn(
                "챔피언 전환율 (%)", format="%.1f%%", help="이 카테고리로 시작한 고객 중 챔피언이 된 비율"
            ),
            "avg_value": st.column_config.NumberColumn(
                "첫 구매 객단가 ($)", format="$%.2f"
            ),
            "potential": st.column_config.Column(
                "잠재력 등급", width="medium"
            )
        },
        hide_index=True,
        use_container_width=True
    )
    
    st.markdown("> **Accessories와 Outerwear**가 챔피언 전환율과 객단가 모두 높은 'Star Category'임이 밝혀졌습니다.")
    
    st.markdown("---")
    
    # 2. Cross-Selling & LTV
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("2. Cross-Selling 패턴")
        st.write("첫 구매 상품(Y축)에 따른 두 번째 구매 상품(색상) Top 5")
        
        df_pair = dfs["category_pairs"]
        fig_sankey = px.bar(
            df_pair, y="first_category", x="pair_count", color="second_category",
            orientation='h',
            text="second_category",
            title="연관 구매 흐름"
        )
        fig_sankey.update_traces(textposition='inside', insidetextanchor='middle')
        fig_sankey.update_layout(showlegend=False)
        st.plotly_chart(fig_sankey, use_container_width=True)
        
    with col2:
        st.subheader("3. 채널별 LTV 매트릭스")
        st.write("Organic(자연유입) vs Paid(광고) 채널 효율 비교")
        
        df_ltv = dfs["ltv"]
        fig_bubble = px.scatter(
            df_ltv, x="source", y="avg_ltv",
            size="avg_ltv", color="category",
            hover_name="category",
            size_max=40,
            title="Channel Profitability (Size = LTV)"
        )
        st.plotly_chart(fig_bubble, use_container_width=True)
        
    st.info("💡 **전략적 시사점:** 'Jeans'나 'Shorts' 같은 기본 아이템 구매자에게는 상의(Tops)를 추천하는 것이 가장 효과적이며, 고가치 고객은 주로 검색이나 광고가 아닌 'Organic(자연 유입)'을 통해 들어옵니다.")

# ==========================================
# PAGE 5: Action Plan
# ==========================================
elif menu == "5. 최종 결론 (Action Plan)":
    st.title("🚀 최종 제언 및 액션 플랜")
    
    st.markdown("""
    데이터 분석 결과, TheLook eCommerce의 성장을 위해서는 **'획득(Acquisition)'보다는 '유지(Retention)'**에 집중해야 하며,
    그 핵심은 **'초기 7일의 경험 관리'**에 있습니다.
    """)
    
    st.subheader("📋 3단계 CRM 액션 플랜")
    
    # Action Card 1
    st.markdown("""
    <div class="action-card">
        <div class="action-title">STEP 1. 온보딩 프로세스 혁신 (단기)</div>
        <ul>
            <li><strong>Welcome Coupon 만료일 단축:</strong> 가입 후 30일이 아닌 <strong>7일</strong>로 설정하여 긴급성(Urgency) 부여.</li>
            <li><strong>첫 구매 유도 상품 큐레이션:</strong> 전환율이 높은 <strong>Accessories</strong>와 <strong>Outerwear</strong> 위주의 랜딩 페이지 구성.</li>
            <li><strong>목표:</strong> 가입 후 7일 내 첫 구매율 10% 증대.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Action Card 2
    st.markdown("""
    <div class="action-card">
        <div class="action-title">STEP 2. 개인화된 교차 판매 (중기)</div>
        <ul>
            <li><strong>알고리즘 기반 추천:</strong> "Shorts 구매자에게는 Tops 추천", "Sweaters 구매자에게는 Jeans 추천" 등 데이터로 검증된 조합 노출.</li>
            <li><strong>타이밍 마케팅:</strong> 첫 구매 후 이탈이 일어나는 시점(D+3)에 "스타일링 팁" 콘텐츠 발송으로 세션 복귀 유도.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Action Card 3
    st.markdown("""
    <div class="action-card">
        <div class="action-title">STEP 3. 고가치 채널 집중 (장기)</div>
        <ul>
            <li><strong>Organic 강화:</strong> LTV가 가장 높은 Organic 유저 확보를 위해 SEO(검색엔진최적화) 예산 증액.</li>
            <li><strong>Display 광고 축소:</strong> 전환율이 낮은 단순 노출형 광고 예산을 축소하고, 리타겟팅(Re-targeting) 광고로 전환.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Designed by 김동윤 | Powered by Streamlit & Plotly")