📊 E-Commerce Customer Segmentation & Retention Strategy Dashboard
(이커머스 고객 세분화 및 리텐션 전략 대시보드)

📝 Project Overview
이 프로젝트는 Looker E-commerce 데이터셋을 기반으로 고객의 구매 행동을 분석하여 RFM 세그먼테이션을 수행하고, 각 세그먼트별 맞춤형 리텐션(Retention) 전략 및 예상 ROI를 제안하는 비즈니스 인텔리전스 대시보드입니다.

단순한 현황 파악을 넘어, "누구를(Who), 언제(When), 어떻게(How) 타겟팅해야 최대의 수익(LTV)을 창출할 수 있는가?" 라는 비즈니스 질문에 답하기 위해 설계되었습니다.

🎯 Key Business Problems
단발성 구매: 구매 고객의 다수가 1회성 구매(Promising)에 그치며 이탈함.

VIP 전환 지연: VIP가 되기까지 재구매 주기가 너무 김(Slow Track).

효율적 예산 배분: 리텐션 마케팅 비용 대비 수익성(ROI)을 사전에 검증하기 어려움.

🖥️ Dashboard Features (Main Sections)
1. 🔍 RFM Segmentation Overview
Recency, Frequency, Monetary 점수(5점 척도)를 기반으로 9개의 고객 세그먼트 정의.

세그먼트별 매출 기여도 및 고객 수 비중 시각화 (Tree map, Pie chart).

핵심 발견: 상위 20% 고객이 전체 매출의 00%를 차지하는 파레토 법칙 확인.

2. ⚠️ Problem Definition & Insight
Promising High/Low: 구매 횟수는 1회로 동일하지만, 세션 활동(탐색) 여부에 따라 LTV가 2배 이상 차이나는 현상 발견.

Churn Risk: 이탈 위험군(At Risk, Hibernating)의 매출 비중이 과다하여 방어 전략 필요성 도출.

3. 📢 Channel & Category Analysis (Acquisition Quality)
Gateway Product: 현재 VIP 고객들이 가입 직후 처음 구매했던 '입문 상품' 분석.

Insight: Outerwear & Coats로 입문한 고객이 Jeans로 입문한 고객보다 LTV가 약 $100 높음.

Acquisition Source: 활성 유저 내 VIP 비중(Maturity Rate) 분석.

Insight: Facebook 유입 고객의 VIP 성숙도가 17.8%로 가장 높음.

4. 🚀 Action Plan & ROI Simulation
세그먼트별 차별화된 액션 플랜 수립 (Nurturing vs Win-back).

ROI 시뮬레이션: 마케팅 비용(매출의 20% 가정) 대비 예상 순이익 산출.

Target: Promising High 미활동 고객 → 세션 유도 → 재구매 전환 시 ROI 400% 달성 예상.

📐 Data Analysis Methodology
1. RFM Scoring Logic
고객의 가치를 정량화하기 위해 다음과 같은 기준으로 점수를 부여했습니다. | Score | Recency (최근성) | Frequency (빈도) | Monetary (금액) | |:---:|:---:|:---:|:---:| | 5 | <= 90일 | 3회+ | P95 이상 | | 4 | <= 180일 | 2회 | P75 이상 | | 3 | <= 365일 | 1회 | P50 이상 | | 2 | <= 545일 | - | P25 이상 | | 1 | 545일+ | - | P25 미만 |

2. Key Segments Definition
VIP Champions: R/F/M 모두 4점 이상 (최근, 자주, 많이 구매).

Promising High Value: 최근 구매했으나(R≥4), 구매 횟수 1회(F=3), 객단가 높음(M≥3).

Promising Low Value: 최근 구매했으나(R≥4), 구매 횟수 1회(F=3), 객단가 낮음(M≤2).

3. ROI Assumption (비용 산출 근거)
비용 설정: 예상 추가 매출의 **20%**를 캠페인 총비용으로 설정.

근거: 패션 이커머스 표준 목표 ROAS(500%) 역산 및 판촉비(할인쿠폰 15%) + 운영비(5%) 고려.

🛠️ Tech Stack
Language: Python

Dashboard: Streamlit

Visualization: Plotly Express / Graph Objects

Data Manipulation: Pandas, NumPy

Database: Google BigQuery SQL
