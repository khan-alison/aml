## 📜 Table: Fact_Transaction

This table stores all transactional events such as transfers, deposits, and withdrawals from customer accounts. Each row represents one atomic transaction, which is critical for monitoring behavioral changes and detecting suspicious money movement patterns.

- **Type**: Fact  
- **CDC Type**: `1.1`  
- **Writer Type**: `factAppend`  
- **Primary Key**: Composite – `(Transaction_ID, ds_partition_date)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Append-only capture of all account transactions for downstream detection, modeling, and reporting.

---

### 🔗 Foreign Keys and Relationships:

| Column              | Referenced Table         | Description                          |
|---------------------|--------------------------|--------------------------------------|
| `From_Account_ID`   | `Dim_Account`            | Source account                       |
| `To_Account_ID`     | `Dim_Account`            | Destination account                  |
| `Transaction_Type_ID` | `Dim_Transaction_Type` | Type of transaction (Transfer, Cash) |
| `Channel_ID`        | `Dim_Channel`            | Transaction channel (Internet, ATM)  |
| `Country_Code`      | `Dim_Country`            | Country involved in transaction      |

---

### 📊 Key Columns (Standardize)

| Raw/Fact_Transaction | Raw Type | Standardized/std_Transaction | Standardized Type | Description                                              | PK  | Note                      |
|----------------------|----------|-------------------------------|-------------------|----------------------------------------------------------|-----|---------------------------|
| `Transaction_ID`     | VARCHAR  | `Transaction_ID`              | VARCHAR           | Unique transaction identifier                            | ✅  | Composite PK              |
| `From_Account_ID`    | VARCHAR  | `From_Account_ID`             | VARCHAR           | Sender's account                                         |     | FK to Dim_Account         |
| `To_Account_ID`      | VARCHAR  | `To_Account_ID`               | VARCHAR           | Receiver's account                                       |     | FK to Dim_Account         |
| `Amount`             | DECIMAL  | `Amount`                      | DECIMAL           | Monetary value of the transaction                        |     | AML rule input            |
| `Transaction_Type_ID`| VARCHAR  | `Transaction_Type_ID`         | VARCHAR           | Type of transaction (wire, cash, etc.)                   |     | FK                        |
| `Booking_Date`       | DATE     | `Booking_Date`                | DATE              | Transaction booking date                                 |     | Used for partitioning     |
| `Channel_ID`         | VARCHAR  | `Channel_ID`                  | VARCHAR           | Channel used (e.g., ATM, online)                         |     | FK                        |
| `Country_Code`       | VARCHAR  | `Country_Code`                | VARCHAR           | Country involved in the transaction                      |     | FK                        |
| `Transaction_Reason` | VARCHAR  | `Transaction_Reason`          | VARCHAR           | Free-text reason or label                                |     | Optional                  |
| `Currency`           | VARCHAR  | `Currency`                    | VARCHAR           | Currency code (e.g., VND, USD)                           |     |                           |
|              |  | `f_structuring_flag`          | BOOLEAN           | TRUE if ≥3 transactions < $10K in 24h                    |     | AML scenario flag         |
|              |  | `f_dormant_flag`              | BOOLEAN           | Dormant account activity                                 |     | AML support flag          |
|              |  | `f_high_velocity_flag`        | BOOLEAN           | >10 transactions in 24h                                  |     | AML support flag          |
|              |  | `f_dormant_now_active`        | BOOLEAN           | Dormant + velocity                                       |     | AML support flag          |
|              |  | `f_high_risk_country_flag`    | BOOLEAN           | Country is high-risk or sanctioned                       |     | AML support flag          |
|              |  | `f_rapid_inout_flag`          | BOOLEAN           | ≥80% incoming sent out within 1h                         |     | AML support flag          |
|              |  | `f_circular_fund_flow_flag`   | BOOLEAN           | TRUE if funds flow in a closed loop within 3 accounts in <24h |     | AML scenario flag         |
|Technical Fields (for CDC + audit)|
|              |   | `cdc_change_type`            | STRING    | Always `'cdc_insert'` (CDC 1.1)                         |     |                           |
|              |   | `cdc_index`                  | LONG      | Ingestion checkpoint index                             |     |                           |
|              |   | `scd_change_timestamp`       | TIMESTAMP | Time record entered lakehouse                          |     |                           |
|              |   | `ds_partition_date`          | DATE      | Partitioning date (from `Booking_Date`)                |     |    
|              |  | `f_outside_business_hours_flag` | BOOLEAN          | TRUE if transaction time falls outside declared hours |     | AML scenario flag              |                       |
|               |  | `f_spending_exceeds_income_flag` | BOOLEAN           | TRUE if total spending in month > 150% of income  |     | AML scenario flag         |
|               |  | `f_structuring_pattern_flag`     | BOOLEAN           | TRUE if repeated small txns just below reporting threshold |     | AML scenario flag         |
| *(N/A)*               | *(N/A)*  | `f_unregistered_channel_flag`     | BOOLEAN           | TRUE if transaction used obscure or unregistered channel |     | AML scenario flag         |

---

### 🚩 Related AML Scenarios (Standardize → Insight)

| AML Scenario Name                        | Flag at Standardize          | Used in Insight |
|------------------------------------------|-------------------------------|------------------|
| Circular Fund Flow Detected              | `f_circular_fund_flow_flag`   | ✅ Yes           |
| Structuring / Smurfing                   | `f_structuring_flag`          | ✅ Yes           |
| Dormant Account Activity                 | `f_dormant_flag`              | ✅ Support       |
| High Velocity                            | `f_high_velocity_flag`        | ✅ Support       |
| Rapid In/Out                             | `f_rapid_inout_flag`          | ✅ Yes           |
| High-Risk Country Origin                 | `f_high_risk_country_flag`    | ✅ Yes           |
| Account Activity Outside Business Hours   | `f_outside_business_hours_flag`  | ✅ Yes           |
| Spending Far Exceeds Monthly Income            | `f_spending_exceeds_income_flag`    | ✅ Yes           |
| Structuring via Layered Transactions           | `f_structuring_pattern_flag`       | ✅ Yes           |
| Use of Obscure/Unregistered Channels           | `f_unregistered_channel_flag`       | ✅ Yes           |

---

### 🧠 Flag Logic Definitions

| Flag Name                    | Type    | Logic                                                                                      |
|------------------------------|---------|--------------------------------------------------------------------------------------------|
| `f_structuring_flag`         | BOOLEAN | TRUE if ≥3 transactions under $10K detected within 24h for the same `From_Account_ID`     |
| `f_dormant_flag`             | BOOLEAN | TRUE if account had ≤6 transactions in last 6 months                                      |
| `f_high_velocity_flag`       | BOOLEAN | TRUE if ≥10 transactions within last 24 hours                                             |
| `f_dormant_now_active`       | BOOLEAN | TRUE if account was dormant and now has high velocity activity on same day               |
| `f_high_risk_country_flag`   | BOOLEAN | TRUE if `Country_Code` is in list of high-risk or sanctioned jurisdictions               |
| `f_rapid_inout_flag`         | BOOLEAN | TRUE if ≥80% of incoming funds are transferred out within 1 hour by same `To_Account_ID` |
| `f_circular_fund_flow_flag`  | BOOLEAN | TRUE if funds return to the originator within 3 hops (A → B → C → A) in under 24h         |
| `f_outside_business_hours_flag` | BOOLEAN | TRUE if transaction occurred outside declared `Work_Start_Hour` and `Work_End_Hour` in `Dim_Customer_Employment` |
| `f_spending_exceeds_income_flag`| BOOLEAN | TRUE if total spending in calendar month > 150% of monthly income    |
| `f_structuring_pattern_flag`    | BOOLEAN | TRUE if ≥ 3 transactions < reporting threshold (e.g., < $10,000) from same customer within 1 day |
| `f_unregistered_channel_flag` | BOOLEAN | TRUE if `Channel_ID` not in list of registered or commonly used channels |

---

### ✅ Notes

- Circular fund flow often indicates layering in money laundering  
- Detection may require window-based multi-hop join logic  
- Flag is computed during standardize phase using window graph traversal  
- Requires high-precision timestamp and directionally joined accounts