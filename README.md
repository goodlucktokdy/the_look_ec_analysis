# 📊 E-Commerce Customer Segmentation & Retention Strategy Dashboard
**(이커머스 고객 세분화 및 리텐션 전략 대시보드)**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18-3F4F75?logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?logo=pandas&logoColor=white)

## Database Schema
erDiagram
    USERS ||--o{ ORDERS : "places"
    USERS ||--o{ EVENTS : "generates"
    USERS ||--o{ ORDER_ITEMS : "related_to"
    
    ORDERS ||--|{ ORDER_ITEMS : "contains"
    
    PRODUCTS ||--o{ ORDER_ITEMS : "listed_in"
    PRODUCTS ||--o{ INVENTORY_ITEMS : "stocked_as"
    
    DISTRIBUTION_CENTERS ||--o{ INVENTORY_ITEMS : "stores"
    INVENTORY_ITEMS ||--o{ ORDER_ITEMS : "supplied_to"

    USERS {
        int id PK
        string first_name
        string last_name
        string email
        int age
        string gender
        string state
        string street_address
        string postal_code
        string city
        string country
        float latitude
        float longitude
        string traffic_source
        timestamp created_at
    }

    ORDERS {
        int order_id PK
        int user_id FK
        string status
        string gender
        timestamp created_at
        timestamp returned_at
        timestamp shipped_at
        timestamp delivered_at
        int num_of_item
    }

    ORDER_ITEMS {
        int id PK
        int order_id FK
        int user_id FK
        int product_id FK
        int inventory_item_id FK
        string status
        timestamp created_at
        timestamp shipped_at
        timestamp delivered_at
        timestamp returned_at
        float sale_price
    }

    PRODUCTS {
        int id PK
        float cost
        string category
        string name
        string brand
        float retail_price
        string department
        string sku
        string distribution_center_id
    }

    EVENTS {
        int id PK
        int user_id FK
        string sequence_number
        string session_id
        timestamp created_at
        string ip_address
        string city
        string state
        string postal_code
        string browser
        string traffic_source
        string uri
        string event_type
    }
    
    INVENTORY_ITEMS {
        int id PK
        int product_id FK
        timestamp created_at
        timestamp sold_at
        float cost
        string product_category
        string product_name
        string product_brand
        float product_retail_price
        string product_department
        string product_sku
        string product_distribution_center_id
    }

    DISTRIBUTION_CENTERS {
        int id PK
        string name
        float latitude
        float longitude
    }
## 📝 Project Overview
이 프로젝트는 **Looker E-commerce 데이터셋**을 기반으로 고객의 구매 행동을 분석하여 **RFM 세그먼테이션**을 수행하고, 각 세그먼트별 맞춤형 **리텐션(Retention) 전략 및 예상 ROI**를 제안하는 비즈니스 인텔리전스 대시보드입니다.

단순한 현황 파악을 넘어, **"누구를(Who), 언제(When), 어떻게(How) 타겟팅해야 최대의 수익(LTV)을 창출할 수 있는가?"** 라는 비즈니스 질문에 답하기 위해 설계되었습니다.

---

## 🎯 Key Business Problems
프로젝트는 다음과 같은 이커머스의 핵심 문제를 해결하는 데 초점을 맞췄습니다.

* **📉 단발성 구매 (One-time Purchase):** 구매 고객의 다수가 1회성 구매(Promising 세그먼트)에 그치며 이탈하는 현상 발생.
* **🐢 VIP 전환 지연 (Slow Conversion):** 첫 구매 후 VIP가 되기까지의 재구매 주기가 지나치게 김 (Slow Track).
* **💰 효율적 예산 배분 (Budget Efficiency):** 리텐션 마케팅 비용 대비 수익성(ROI)을 사전에 검증하기 어려워 전략 수립에 난항.

---

## 🖥️ Dashboard Features (Main Sections)

### 1. 🔍 RFM Segmentation Overview
* **세분화 모델:** Recency, Frequency, Monetary 점수(5점 척도)를 기반으로 **9개의 고객 세그먼트**를 정의했습니다.
* **시각화:** Tree map과 Pie chart를 통해 세그먼트별 매출 기여도 및 고객 수 비중을 시각화했습니다.
* **핵심 발견:** 상위 20% 고객이 전체 매출의 **XX%**를 차지하는 파레토 법칙을 확인했습니다.

### 2. ⚠️ Problem Definition & Insight
데이터 심층 분석을 통해 비즈니스 임팩트가 큰 문제점을 도출했습니다.
* **Promising High vs Low:** 두 그룹 모두 구매 횟수는 1회로 동일하지만, **'세션 활동(탐색)' 여부에 따라 LTV가 2배 이상 차이**나는 현상을 발견했습니다.
* **Churn Risk:** 이탈 위험군(At Risk, Hibernating)의 매출 비중이 과다하여 방어 전략의 필요성을 도출했습니다.

### 3. 📢 Channel & Category Analysis (Acquisition Quality)
"VIP는 어디서 왔고, 처음에 무엇을 샀는가?"를 분석하여 획득 전략(UA)을 최적화합니다.
* **Gateway Product (입문 상품):** 현재 VIP 고객들이 가입 직후 처음 구매했던 상품을 분석했습니다.
    > 💡 **Insight:** `Outerwear & Coats`로 입문한 고객이 `Jeans`로 입문한 고객보다 **LTV가 약 $100 높음**을 확인했습니다.
* **Acquisition Source (유입 채널):** 활성 유저 내 VIP 비중(Maturity Rate)을 분석했습니다.
    > 💡 **Insight:** `Facebook` 유입 고객의 VIP 성숙도가 **17.8%**로 가장 높아, 충성 고객 확보에 유리함을 증명했습니다.

### 4. 🚀 Action Plan & ROI Simulation
* **Action Plan:** 세그먼트별 차별화된 액션 플랜(Nurturing vs Win-back)을 수립했습니다.
* **ROI 시뮬레이션:** 마케팅 비용을 매출의 20%로 가정하고 예상 순이익을 산출했습니다.
* **Target:** `Promising High` 미활동 고객 → 세션 유도 → 재구매 전환 시 **ROI 400% 달성**을 예상합니다.

---

## 📐 Data Analysis Methodology

### 1. RFM Scoring Logic
고객의 가치를 정량화하기 위해 다음과 같은 기준으로 점수를 부여했습니다.

| Score | Recency (최근성) | Frequency (빈도) | Monetary (금액) |
|:---:|:---:|:---:|:---:|
| **5** | <= 90일 | 3회+ | P95 이상 |
| **4** | <= 180일 | 2회 | P75 이상 |
| **3** | <= 365일 | 1회 | P50 이상 |
| **2** | <= 545일 | - | P25 이상 |
| **1** | 545일+ | - | P25 미만 |

### 2. Key Segments Definition
* **👑 VIP Champions:** R/F/M 모두 4점 이상 (최근, 자주, 많이 구매).
* **💎 Promising High Value:** 최근 구매했으나(R≥4), 구매 횟수 1회(F=3), 객단가 높음(M≥3).
* **🌱 Promising Low Value:** 최근 구매했으나(R≥4), 구매 횟수 1회(F=3), 객단가 낮음(M≤2).

### 3. ROI Assumption (비용 산출 근거)
본 프로젝트의 ROI 시뮬레이션은 다음과 같은 논리에 기반합니다.
* **비용 설정:** 예상 추가 매출의 **20%**를 캠페인 총비용으로 설정.
* **근거:** 패션 이커머스 표준 목표 **ROAS(500%)**를 역산하고, **판촉비(할인쿠폰 15%) + 운영비(5%)** 구조를 반영하여 보수적으로 책정.

---

## 🛠️ Tech Stack

* **Language:** Python
* **Dashboard Framework:** Streamlit
* **Visualization:** Plotly Express / Graph Objects
* **Data Manipulation:** Pandas, NumPy
* **Database:** Google BigQuery SQL
