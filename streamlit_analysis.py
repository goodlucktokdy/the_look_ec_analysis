import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -----------------------------------------------------------------------------
# 1. Page Configuration & Setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="TheLook eCommerce CRM Growth Strategy",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2563EB;
        font-weight: bold;
        margin-top: 20px;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2563EB;
    }
    .insight-box {
        background-color: #ECFDF5;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #10B981;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Data Loading (Embedding provided JSON data)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    # 2.1 Post Purchase Activity
    data_post_activity = [
        {"activity_level": "0. No Activity", "user_count": 3287, "pct": 70.78, "avg_events": 0.0, "avg_product_views": 0.0, "avg_cart_adds": 0.0},
        {"activity_level": "1. 1 Session", "user_count": 374, "pct": 8.05, "avg_events": 1.3, "avg_product_views": 0.1, "avg_cart_adds": 0.1},
        {"activity_level": "2. 2-3 Sessions", "user_count": 886, "pct": 19.08, "avg_events": 2.4, "avg_product_views": 0.0, "avg_cart_adds": 0.0},
        {"activity_level": "3. 4-5 Sessions", "user_count": 97, "pct": 2.09, "avg_events": 5.8, "avg_product_views": 0.6, "avg_cart_adds": 0.6}
    ]

    # 2.2 Champions Time to 2nd Purchase
    data_time_bucket = [
        {"time_bucket": "1. Within 1 Week", "champions_count": 39, "pct": 2.41, "avg_days": 3.6, "cumulative_pct": 2.41},
        {"time_bucket": "2. Within 2 Weeks", "champions_count": 44, "pct": 2.72, "avg_days": 11.0, "cumulative_pct": 5.13},
        {"time_bucket": "3. Within 1 Month", "champions_count": 74, "pct": 4.57, "avg_days": 23.5, "cumulative_pct": 9.7},
        {"time_bucket": "4. Within 2 Months", "champions_count": 141, "pct": 8.71, "avg_days": 44.8, "cumulative_pct": 18.41},
        {"time_bucket": "5. Within 3 Months", "champions_count": 147, "pct": 9.08, "avg_days": 75.4, "cumulative_pct": 27.49},
        {"time_bucket": "6. 3+ Months", "champions_count": 1174, "pct": 72.51, "avg_days": 309.0, "cumulative_pct": 100.0}
    ]

    # 2.3 Category Comparison
    data_category_comp = [
        {"purchase_pattern": "Same Department", "champions_count": 2086, "pct": 92.51},
        {"purchase_pattern": "Same Category", "champions_count": 169, "pct": 7.49}
    ]
    
    # 2.4 Category Pairs (Top 10 for visualization)
    data_category_pairs = [
        {"first_category": "Accessories", "second_category": "Tops & Tees", "pair_count": 17},
        {"first_category": "Active", "second_category": "Swim", "pair_count": 13},
        {"first_category": "Dresses", "second_category": "Intimates", "pair_count": 10},
        {"first_category": "Jeans", "second_category": "Sleep & Lounge", "pair_count": 14},
        {"first_category": "Outerwear & Coats", "second_category": "Tops & Tees", "pair_count": 12},
        {"first_category": "Pants", "second_category": "Tops & Tees", "pair_count": 16},
        {"first_category": "Shorts", "second_category": "Tops & Tees", "pair_count": 21},
        {"first_category": "Sleep & Lounge", "second_category": "Sleep & Lounge", "pair_count": 17},
        {"first_category": "Sweaters", "second_category": "Jeans", "pair_count": 20},
        {"first_category": "Tops & Tees", "second_category": "Sleep & Lounge", "pair_count": 19}
    ]

    # 2.5 Conversion Speed Activity
    data_conv_speed = [
        {"conversion_speed": "1. Quick (≤30 days)", "avg_events": 1.4, "avg_sessions": 0.6},
        {"conversion_speed": "2. Medium (31-60 days)", "avg_events": 1.6, "avg_sessions": 0.8},
        {"conversion_speed": "3. Slow (61+ days)", "avg_events": 2.3, "avg_sessions": 0.9}
    ]

    # 2.6 RFM Segments
    data_rfm_segments = [
        {"customer_segment": "6. Hibernating", "user_count": 9707, "pct": 32.58, "revenue_contribution_pct": 27.21, "avg_rfm_total": 6.93},
        {"customer_segment": "3. Promising", "user_count": 8446, "pct": 28.35, "revenue_contribution_pct": 23.73, "avg_rfm_total": 9.95},
        {"customer_segment": "5. At Risk", "user_count": 6637, "pct": 22.28, "revenue_contribution_pct": 18.75, "avg_rfm_total": 8.41},
        {"customer_segment": "1. Champions", "user_count": 2787, "pct": 9.35, "revenue_contribution_pct": 17.1, "avg_rfm_total": 12.53},
        {"customer_segment": "2. Loyal Customers", "user_count": 1357, "pct": 4.55, "revenue_contribution_pct": 8.22, "avg_rfm_total": 10.88},
        {"customer_segment": "4. Need Attention", "user_count": 861, "pct": 2.89, "revenue_contribution_pct": 5.0, "avg_rfm_total": 9.53}
    ]

    # 2.7 Repurchase Timing
    data_repurchase = [
        {"first_purchase_timing": "1주일 이내", "repurchase_rate": 26.06, "avg_days_to_repurchase": 203.4},
        {"first_purchase_timing": "1개월 이내", "repurchase_rate": 25.08, "avg_days_to_repurchase": 179.6},
        {"first_purchase_timing": "2개월 이내", "repurchase_rate": 24.63, "avg_days_to_repurchase": 181.6},
        {"first_purchase_timing": "3개월 이내", "repurchase_rate": 23.63, "avg_days_to_repurchase": 170.7},
        {"first_purchase_timing": "3개월+", "repurchase_rate": 15.79, "avg_days_to_repurchase": 204.5}
    ]
    
    # 2.8 Champions First Category
    data_champ_cat = [
        {"category": "Jeans", "conversion_pct": 25.2, "avg_value": 97.47, "user_count": 191},
        {"category": "Tops & Tees", "conversion_pct": 24.45, "avg_value": 44.24, "user_count": 189},
        {"category": "Intimates", "conversion_pct": 22.3, "avg_value": 35.35, "user_count": 184},
        {"category": "Fashion Hoodies", "conversion_pct": 24.73, "avg_value": 54.07, "user_count": 181},
        {"category": "Sleep & Lounge", "conversion_pct": 25.21, "avg_value": 52.09, "user_count": 178},
        {"category": "Accessories", "conversion_pct": 28.38, "avg_value": 42.72, "user_count": 174},
        {"category": "Outerwear & Coats", "conversion_pct": 26.96, "avg_value": 151.77, "user_count": 158}
    ]

    # 2.9 Traffic Source LTV (Top performers)
    data_ltv = [
        {"source": "Organic", "category": "Outerwear", "avg_ltv": 452.22},
        {"source": "Organic", "category": "Tops & Tees", "avg_ltv": 419.65},
        {"source": "Search", "category": "Suits", "avg_ltv": 378.35},
        {"source": "Facebook", "category": "Hoodies", "avg_ltv": 370.73},
        {"source": "Search", "category": "Jeans", "avg_ltv": 337.21}
    ]

    # 2.10 Traffic Source Conversion
    data_traffic_conv = [
        {"source": "Email", "conversion_rate": 27.13},
        {"source": "Facebook", "conversion_rate": 26.27},
        {"source": "Search", "conversion_rate": 24.92},
        {"source": "Display", "conversion_rate": 24.05},
        {"source": "Organic", "conversion_rate": 23.12}
    ]

    return {
        "post_activity": pd.DataFrame(data_post_activity),
        "time_bucket": pd.DataFrame(data_time_bucket),
        "category_comp": pd.DataFrame(data_category_comp),
        "category_pairs": pd.DataFrame(data_category_pairs),
        "conv_speed": pd.DataFrame(data_conv_speed),
        "rfm_segments": pd.DataFrame(data_rfm_segments),
        "repurchase": pd.DataFrame(data_repurchase),
        "champ_cat": pd.DataFrame(data_champ_cat),
        "ltv": pd.DataFrame(data_ltv),
        "traffic_conv": pd.DataFrame(data_traffic_conv)
    }

dfs = load_data()

# -----------------------------------------------------------------------------
# 3. Sidebar Navigation
# -----------------------------------------------------------------------------
st.sidebar.title("📑 분석 목차")
page = st.sidebar.radio("Go to", 
    ["1. 프로젝트 개요", 
     "2. 고객 세분화 (RFM)", 
     "3. 고객 행동 분석", 
     "4. 챔피언 고객 분석",
     "5. 채널 및 상품 전략",
     "6. 최종 결론 및 액션 플랜"]
)

st.sidebar.markdown("---")
st.sidebar.info("**Data Source:** TheLook eCommerce (Google BigQuery)\n\n**Period:** 2023-01-01 ~ 2024-12-31")

# -----------------------------------------------------------------------------
# 4. Page Content
# -----------------------------------------------------------------------------

# --- PAGE 1: Project Overview ---
if page == "1. 프로젝트 개요":
    st.markdown('<div class="main-header">TheLook eCommerce CRM 성장 전략</div>', unsafe_allow_html=True)
    st.markdown("### :dart: 문제 정의 및 가설 설정")
    
    st.write("""
    **배경:** 최근 신규 유입은 증가하고 있으나, 구매 후 이탈률이 높고 충성 고객(Champions)으로의 전환이 더딥니다. 
    마케팅 예산의 효율적인 집행을 위해 '누가', '언제', '무엇을' 샀을 때 LTV가 높은지 파악해야 합니다.
    
    **문제 정의:**
    1. **높은 초기 이탈:** 첫 구매 후 재방문/활동이 없는 유저 비율이 매우 높음 (약 70%).
    2. **챔피언 전환의 비밀:** 충성 고객이 되는 유저들은 어떤 초기 행동 패턴을 보이는가?
    
    **가설:**
    1. **"Golden Time":** 가입 후 첫 구매, 그리고 첫 구매 후 재구매까지의 시간이 짧을수록 충성 고객이 될 확률이 높을 것이다.
    2. **"Gateway Product":** 특정 카테고리(예: Jeans, Tops)로 진입한 고객이 LTV가 더 높을 것이다.
    3. **"Channel Effect":** Email 채널이 재구매율(Retention) 방어에 가장 효과적일 것이다.
    """)

    st.markdown("### :chart_with_upwards_trend: 주요 데이터 요약")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("분석 대상 유저", "약 30,000명")
    with col2:
        st.metric("총 기간", "24개월 (2023-2024)")
    with col3:
        st.metric("핵심 목표", "재구매율 증대")

# --- PAGE 2: RFM Analysis ---
elif page == "2. 고객 세분화 (RFM)":
    st.markdown('<div class="main-header">RFM 기반 고객 세분화</div>', unsafe_allow_html=True)
    
    st.info("""
    **💡 RFM 스코어 산정 기준 (1~5점 척도)**
    
    *분석의 정확도를 위해 TheLook 데이터 분포에 맞춰 아래와 같이 기준을 설정했습니다.*
    
    * **Recency (최근성):** 90일 이내(5점), 180일 이내(4점), 1년 이내(3점), 1.5년 이내(2점), 그 외(1점)
    * **Frequency (빈도):** 3회 이상(5점), 2회(4점), 1회(3점), 그 외(1점 - *단, 구매 이력 필터링으로 인해 대부분 3점부터 시작*)
    * **Monetary (규모/수량):** 5개 이상(5점), 3~4개(4점), 2개(3점), 1개(2점)
    """)

    # Visualization: Segment Distribution
    st.markdown("### 📊 고객 세그먼트 분포 및 매출 기여도")
    
    df_rfm = dfs["rfm_segments"]
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(x=df_rfm['customer_segment'], y=df_rfm['pct'], name="유저 비율 (%)", marker_color='#93C5FD'),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(x=df_rfm['customer_segment'], y=df_rfm['revenue_contribution_pct'], name="매출 기여도 (%)", 
                   mode='lines+markers', line=dict(color='#1D4ED8', width=3)),
        secondary_y=True
    )
    
    fig.update_layout(title_text="유저 수 비율 vs 매출 기여도 비교")
    fig.update_yaxes(title_text="유저 비율 (%)", secondary_y=False)
    fig.update_yaxes(title_text="매출 기여도 (%)", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
    <strong>Key Insight:</strong><br>
    <ul>
        <li><strong>Champions (9.35%)</strong>가 전체 매출의 <strong>17.1%</strong>를 차지하며, Loyal Customers를 합치면 상위 14%가 매출의 25% 이상을 견인합니다.</li>
        <li><strong>Hibernating (32.6%)</strong> 그룹이 가장 큰 비중을 차지합니다. 이들은 과거 1회 구매 후 1.5년 가까이 활동이 없는 상태로, 사실상 이탈로 간주해야 합니다.</li>
        <li><strong>Promising (28.3%)</strong> 그룹은 최근에 가입하여 1회 구매한 '성장 가능성'이 있는 그룹입니다. 이들을 Champions로 전환시키는 것이 핵심 과제입니다.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# --- PAGE 3: Customer Behavior ---
elif page == "3. 고객 행동 분석":
    st.markdown('<div class="main-header">구매 후 행동 분석 (Retention)</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🛑 충격적인 초기 이탈률")
        st.write("첫 구매 후 유저들의 세션 활동 수를 분석했습니다.")
        df_activity = dfs["post_activity"]
        fig_act = px.pie(df_activity, values='pct', names='activity_level', 
                         title='첫 구매 후 추가 활동(Session) 비율',
                         color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_act, use_container_width=True)
    
    with col2:
        st.markdown("### ⏱️ 골든 타임: 재구매까지 걸리는 시간")
        st.write("첫 가입 후 구매 시점에 따른 재구매율 변화입니다.")
        df_repurchase = dfs["repurchase"]
        fig_re = px.bar(df_repurchase, x='first_purchase_timing', y='repurchase_rate',
                        title='가입 후 첫 구매 시기별 재구매율(%)',
                        color='repurchase_rate', color_continuous_scale='Blues')
        st.plotly_chart(fig_re, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    <strong>Key Insight:</strong><br>
    <ul>
        <li><strong>70%의 유저</strong>가 첫 구매 이후 단 한 번의 세션 활동도 없이 사라집니다. 이는 Onboarding 및 첫 배송 경험 프로세스에 문제가 있음을 시사합니다.</li>
        <li><strong>가입 후 1주일 이내</strong>에 첫 구매를 한 고객의 재구매율(26%)이 3개월 이후 구매자(15%)보다 <strong>10%p 이상 높습니다.</strong></li>
        <li>즉, 가입 직후 7일 이내에 구매를 유도하는 것이 LTV 상승의 지름길입니다.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# --- PAGE 4: Champion Analysis ---
elif page == "4. 챔피언 고객 분석":
    st.markdown('<div class="main-header">Champions는 어떻게 만들어지는가?</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["재구매 속도", "크로스 셀링 패턴"])
    
    with tab1:
        st.markdown("### 🚀 Champions의 두 번째 구매 속도")
        df_time = dfs["time_bucket"]
        
        # Cumulative Line Chart combined with Bar
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=df_time['time_bucket'], y=df_time['pct'], name="비율", marker_color='#10B981'), secondary_y=False)
        fig.add_trace(go.Scatter(x=df_time['time_bucket'], y=df_time['cumulative_pct'], name="누적 비율", mode='lines+markers'), secondary_y=True)
        
        fig.update_layout(title="Champions의 첫 구매 후 두 번째 구매까지 소요 시간")
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("Champions의 약 72%는 3개월 이후에 재구매를 했지만, **초기 3개월 내에 재구매한 27%**가 핵심 가속 성장 그룹입니다.")

    with tab2:
        st.markdown("### 🛍️ 크로스 셀링 (Cross-Selling) 패턴")
        col_a, col_b = st.columns([1, 2])
        
        with col_a:
            st.metric("동일 부서(Department) 재구매율", "92.5%")
            st.write("대부분의 유저는 자신이 처음 산 카테고리(남성/여성 등) 내에서 재구매합니다.")
        
        with col_b:
            st.write("**함께 많이 팔리는 카테고리 조합 (Top Pairs)**")
            df_pairs = dfs["category_pairs"]
            fig_sankey = px.bar(df_pairs, x='pair_count', y='first_category', color='second_category', orientation='h',
                                title="첫 구매 카테고리별 두 번째 구매 카테고리 (Top 10)")
            st.plotly_chart(fig_sankey, use_container_width=True)
            st.caption("예: Shorts를 산 고객은 다음에 Tops & Tees를 살 확률이 높습니다.")

# --- PAGE 5: Strategy ---
elif page == "5. 채널 및 상품 전략":
    st.markdown('<div class="main-header">채널 및 상품 최적화 전략</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Champions 전환율이 높은 첫 상품")
        df_champ = dfs["champ_cat"].sort_values('conversion_pct', ascending=True)
        fig_prod = px.bar(df_champ, x='conversion_pct', y='category', orientation='h',
                          title='첫 구매 카테고리별 Champions 전환율 (%)',
                          color='avg_value', labels={'avg_value': '첫 구매 단가($)'})
        st.plotly_chart(fig_prod, use_container_width=True)
        
    with col2:
        st.markdown("### 📣 트래픽 소스별 전환 효율")
        df_traffic = dfs["traffic_conv"].sort_values('conversion_rate', ascending=False)
        fig_trf = px.bar(df_traffic, x='source', y='conversion_rate',
                         title='Traffic Source별 Champions 전환율 (%)',
                         color='source', color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig_trf, use_container_width=True)

    st.markdown("### 💰 고가치 유입 경로 (LTV 관점)")
    st.write("Organic(자연 유입)으로 들어와 Outerwear나 Tops를 구매하는 고객의 LTV가 압도적으로 높습니다.")
    df_ltv = dfs["ltv"]
    st.dataframe(df_ltv.style.background_gradient(cmap="Greens", subset=['avg_ltv']), use_container_width=True)

# --- PAGE 6: Conclusion ---
elif page == "6. 최종 결론 및 액션 플랜":
    st.markdown('<div class="main-header">🚀 최종 결론 및 액션 플랜</div>', unsafe_allow_html=True)
    
    st.success("""
    ### 🎯 Summary
    1. **초기 이탈 방어:** 첫 구매자의 70%가 이탈합니다. 가입 후 7일 이내 첫 구매 유도가 중요합니다.
    2. **Gateway Products:** **Accessories, Outerwear, Plus** 제품군으로 진입한 고객이 충성 고객이 될 확률이 높습니다.
    3. **Channel:** **Email**은 재구매 유도에 가장 효과적이며, **Organic** 유입 고객은 LTV가 가장 높습니다.
    """)
    
    st.markdown("---")
    
    st.markdown("### 📋 Action Plan")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 1. CRM 자동화 (Golden Time)")
        st.write("""
        - **D+0 ~ D+7:** 가입 직후 웰컴 쿠폰 만료 알림 강화.
        - **D+30:** 첫 구매 후 활동 없는 유저(70%) 대상 '재방문 유도' 개인화 메시지 발송.
        - **Action:** 이메일 마케팅 자동화 시나리오 재설계.
        """)
        
    with col2:
        st.markdown("#### 2. 크로스 셀링 (Cross-sell)")
        st.write("""
        - **Shorts 구매자:** → Tops & Tees 추천.
        - **Jeans 구매자:** → Sweaters 추천.
        - **Action:** 상품 상세 페이지 하단 '함께 구매하면 좋은 상품' 알고리즘을 위 데이터 기반으로 고정 노출.
        """)
        
    with col3:
        st.markdown("#### 3. 고가치 유저 타겟팅")
        st.write("""
        - **Organic & Search:** Outerwear, Suits 등 객단가 높은 카테고리의 SEO 강화.
        - **Promising 관리:** 최근 1회 구매한 'Promising' 등급 고객에게 VIP 혜택 맛보기(무료 배송 등) 제공하여 2회차 구매 유도.
        """)

    st.info("이 대시보드는 TheLook eCommerce 데이터를 기반으로 작성되었으며, 실제 비즈니스 적용 시 A/B 테스트를 통한 검증을 권장합니다.")