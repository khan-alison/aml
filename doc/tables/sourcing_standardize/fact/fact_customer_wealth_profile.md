## 📜 Table: Dim_Customer_Wealth_Profile

This dimension captures the estimated financial position of a customer, including assets, liabilities, income, and wealth classification. Implemented as `SCD4a`, it provides full daily snapshots to support behavioral trend analysis, regulatory reporting, and ML features.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Customer_ID`  
- **Partitioned By**: `ds_partition_date` (in history table)  
- **Snapshot Strategy**: Daily full overwrite to history table; latest view in main table

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Customer_Wealth_Profile | Raw Type | Standardized/std_Customer_Wealth_Profile | Standardized Type | Standardized/std_Customer_Wealth_Profile_Hist | Description                                      | PK  | Note                             |
|----------------------------------|----------|------------------------------------------|-------------------|-------------------------------------------------|--------------------------------------------------|-----|----------------------------------|
| `Customer_ID`                   | VARCHAR  | `Customer_ID`                            | VARCHAR           | `Customer_ID`                                  | Unique customer identifier                      | ✅  |                                  |
| `Date_ID`                       | DATE     | `Date_ID`                                | DATE              | `Date_ID`                                      | Snapshot date (can be booking date)             |     |                                  |
| `Total_Balance`                 | DECIMAL  | `Total_Balance`                          | DECIMAL           | `Total_Balance`                                | Sum of customer balance across accounts         |     |                                  |
| `Total_Assets`                 | DECIMAL  | `Total_Assets`                           | DECIMAL           | `Total_Assets`                                 | Estimated total asset value                     |     |                                  |
| `Estimated_Income`             | DECIMAL  | `Estimated_Income`                       | DECIMAL           | `Estimated_Income`                             | Estimated monthly/annual income                 |     |                                  |
| `Loan_Exposure`                | DECIMAL  | `Loan_Exposure`                          | DECIMAL           | `Loan_Exposure`                                | Total outstanding loan exposure                 |     |                                  |
| `Wealth_Tier`                  | VARCHAR  | `Wealth_Tier`                            | VARCHAR           | `Wealth_Tier`                                  | Wealth category (e.g., Mass, Affluent, HNW)     |     |                                  |
|Technical Fields (for CDC + audit + snapshot logic)|
|              |   | `scd_change_type`             | STRING    | `scd_change_type`             | `'cdc_insert'` or `'cdc_update'`                  |     | CDC 1.3 logic                     |
|              |   | `cdc_index`                   | INT       | `cdc_index`                   | Change index (optional for sequencing)            |     |                                  |
|              |   | `scd_change_timestamp`        | TIMESTAMP | `scd_change_timestamp`        | Ingestion timestamp                               |     |                                  |
|              |   | `dtf_start_date`              | DATE      | `dtf_start_date`              | Snapshot validity start date                      |     |                                  |
|              |   | `dtf_end_date`                | DATE      | `dtf_end_date`                | Snapshot end date (NULL = current)                |     |                                  |
|              |   | `dtf_current_flag`            | BOOLEAN   | `dtf_current_flag`            | TRUE = currently active snapshot                  |     |                                  |
|              |   |            | DATE      | `ds_partition_date`           | Partition column (history table only)             |     | Only in `_hist` table            |

---

### ✅ Business Use Cases

- Detect sudden drop/increase in wealth across time  
- Identify inconsistencies between declared and observed behavior  
- Train ML models on time-series features like asset volatility  
- Reconstruct financial profile at the time of alerts or onboarding