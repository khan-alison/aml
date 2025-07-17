## 📜 Table: Dim_Customer_Wealth_Profile

This dimension captures the estimated financial position of a customer, including assets, liabilities, income, and wealth classification. Implemented as `SCD4a`, it provides full daily snapshots to support behavioral trend analysis, regulatory reporting, and ML features.

- **Type**: Dimension  
- **CDC Type**: `1.3`
- **Writer Type**: `scd4a`  
- **Primary Key**: `Customer_ID`  
- **Partitioned By**: `ds_partition_date` (in history table)  
- **Snapshot Strategy**: Daily full overwrite to history table; latest view in main table

---

### 🧩 Main Table Schema (Latest Snapshot Only)

| Column Name           | Type     | Description                                |
|-----------------------|----------|--------------------------------------------|
| `Customer_ID`         | VARCHAR  | Unique customer identifier                 |
| `Date_ID`             | DATE     | Snapshot date (can be booking date)        |
| `Total_Balance`       | DECIMAL  | Sum of customer balance across accounts    |
| `Total_Assets`        | DECIMAL  | Estimated total asset value                |
| `Estimated_Income`    | DECIMAL  | Estimated monthly/annual income            |
| `Loan_Exposure`       | DECIMAL  | Total outstanding loan exposure            |
| `Wealth_Tier`         | VARCHAR  | Wealth category (e.g., Mass, Affluent, HNW)|

#### 🧪 Technical Fields (Main Table):
| Column Name            | Type       | Description                              |
|------------------------|------------|------------------------------------------|
| `scd_change_type`      | STRING     | 'cdc_insert' or 'cdc_update'             |
| `cdc_index`            | INT        | Optional change order index              |
| `scd_change_timestamp` | TIMESTAMP  | When this snapshot was loaded            |
| `dtf_start_date`       | DATE       | Snapshot start date                      |
| `dtf_end_date`         | DATE       | NULL = current, otherwise expiry date    |
| `dtf_current_flag`     | BOOLEAN    | TRUE = current active snapshot           |

---

### 🗃 History Table Schema (Full Snapshot Per Day)

Same structure as Main Table, **plus:**

| Column Name          | Type     | Description                                 |
|----------------------|----------|---------------------------------------------|
| `ds_partition_date`  | DATE     | Partition column = snapshot date            |

- History table keeps **1 row per customer per snapshot day**
- Enables full point-in-time reconstruction of wealth profile

---

### ✅ Business Use Cases
- Detect sudden drop/increase in wealth across time
- Identify inconsistencies between declared and observed behavior
- Train ML models on time-series features like asset volatility
- Reconstruct financial profile at the time of alerts or onboarding
