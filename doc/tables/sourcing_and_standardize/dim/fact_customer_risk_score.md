## 📜 Table: Fact_Customer_Risk_Score

This fact table stores the daily computed risk score of each customer based on multiple AML signals. It supports alert generation, profiling, model training, and ongoing monitoring of behavioral and exposure-based risk.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Customer_ID + Score_Date` (from source)  
- **Partitioned By**: `ds_partition_date` (string, in `_Hist` table only)  
- **Snapshot Strategy**: SCD4a – current risk score in main table, full scoring history in `_Hist`

---

### 📊 Key Columns (Standardize)

| Raw/Fact_Customer_Risk_Score | Raw Type  | PK  | Standardized/Fact_Customer_Risk_Score | Standardized Type | Description                                       | Value of Technical Field           | Note                          |
|------------------------------|-----------|-----|----------------------------------------|--------------------|---------------------------------------------------|------------------------------------|-------------------------------|
| `Customer_ID`                | STRING    | ✅  | `Customer_ID`                         | STRING             | Customer whose risk is being scored               |                                    | FK to `Dim_Customer`         |
| `Score_Date`                 | DATE      | ✅  | `Score_Date`                          | DATE               | Date of the risk score snapshot                   |                                    | Used in scoring partition     |
| `Risk_Score`                 | DECIMAL   |     | `Risk_Score`                          | DECIMAL(5,2)       | Computed numeric score (e.g., 0–100)              |                                    | ML or rule-based              |
| `Risk_Level`                 | STRING    |     | `Risk_Level`                          | STRING             | Low, Medium, High                                 |                                    | Derived from score thresholds |
| `Risk_Category`             | STRING    |     | `Risk_Category`                       | STRING             | Financial, Behavioral, KYC, etc.                  |                                    | Optional classification       |
| `Scoring_Model_Version`     | STRING    |     | `Scoring_Model_Version`               | STRING             | Version of rule/ML logic used                     |                                    | For audit tracking            |
| `created_at`                 | TIMESTAMP |     | `created_at`                          | TIMESTAMP          | Timestamp when this score was computed            | From source                        |                               |
| `updated_at`                 | TIMESTAMP |     | `updated_at`                          | TIMESTAMP          | Last seen update to this score                    | From source                        |                               |
| **Technical Fields**         |           |     |                                        |                    |                                                   |                                    |                               |
|                              |           |     | `ds_key`                              | STRING             | Surrogate primary key                             | `md5(Customer_ID || Score_Date)`  | Required for uniqueness       |
|                              |           |     | `cdc_index`                           | INT                | 1 = current, 0 = outdated                         | `1` or `0`                         | Used for filtering            |
|                              |           |     | `cdc_change_type`                     | STRING             | CDC change type                                   | `'cdc_insert'`, `'cdc_update'`    | From scoring engine CDC       |
|                              |           |     | `scd_change_timestamp`                | TIMESTAMP          | Snapshot timestamp                                | `updated_at` or job time           | For audit and traceability    |
|                              |           |     | `dtf_start_date`                      | DATE               | Validity start date                               | From `updated_at` or partition     |                               |
|                              |           |     | `dtf_end_date`                        | DATE               | Validity end date (nullable)                      | NULL if current                    |                               |
|                              |           |     | `dtf_current_flag`                    | BOOLEAN            | TRUE if current version                           | TRUE/FALSE                         | Required in scd4a              |
|                              |           |     | `ds_partition_date`                   | STRING             | Partition column (`yyyy-MM-dd`)                   | Job run date                       | Required in `_Hist`            |

---

### ✅ Business Use Cases

- Drive real-time alerting thresholds based on score changes  
- Detect risk escalations and persistent high-risk behavior  
- Feed ML models and trend analysis dashboards  
- Provide explainability for high-risk customer designations  