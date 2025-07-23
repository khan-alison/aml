## 📜 Table: Dim_Customer_Wealth_Profile

This dimension estimates customer wealth classification over time. It is used in customer risk scoring, high-net-worth monitoring, and behavioral profiling. The values evolve and are tracked using SCD4a strategy.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Customer_ID` (from source)  
- **Partitioned By**: `ds_partition_date` (string, in `_Hist` table only)  
- **Snapshot Strategy**: SCD4a – current version in main table, full history in `_Hist`

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Customer_Wealth_Profile | Raw Type  | PK  | Standardized/Dim_Customer_Wealth_Profile | Standardized Type | Description                                        | Value of Technical Field         | Note                          |
|----------------------------------|-----------|-----|-------------------------------------------|--------------------|----------------------------------------------------|----------------------------------|-------------------------------|
| `Customer_ID`                    | STRING    | ✅  | `Customer_ID`                             | STRING             | Customer identifier                               |                                  | FK to `Dim_Customer`         |
| `Wealth_Tier`                    | STRING    |     | `Wealth_Tier`                             | STRING             | Tier category (e.g., Mass, Affluent, HNW)         |                                  | Mapped from score/rules      |
| `Wealth_Score`                   | INT       |     | `Wealth_Score`                            | INT                | Numeric wealth score used for segmentation        |                                  | Can be derived or sourced    |
| `Est_Annual_Income`             | DECIMAL   |     | `Est_Annual_Income`                       | DECIMAL(18,2)      | Estimated annual income                           |                                  | Optional                     |
| `Est_Total_Assets`              | DECIMAL   |     | `Est_Total_Assets`                        | DECIMAL(18,2)      | Estimated total assets held                       |                                  | Optional                     |
| `created_at`                    | TIMESTAMP |     | `created_at`                              | TIMESTAMP          | First seen in source                              | From source                      |                              |
| `updated_at`                    | TIMESTAMP |     | `updated_at`                              | TIMESTAMP          | Last seen update in source                        | From source                      |                              |
| **Technical Fields**            |           |     |                                           |                    |                                                    |                                  |                              |
|                                  |           |     | `ds_key`                                   | STRING             | Surrogate primary key                             | `Customer_ID`                    | Used as PK in standardized   |
|                                  |           |     | `cdc_index`                                | INT                | Current record flag                               | `1` or `0`                       | 1 = current                  |
|                                  |           |     | `cdc_change_type`                          | STRING             | Type of change                                    | `'cdc_insert'` or `'cdc_update'`| From CDC engine              |
|                                  |           |     | `scd_change_timestamp`                     | TIMESTAMP          | Change detection timestamp                        | `updated_at` or job time         |                              |
|                                  |           |     | `dtf_start_date`                           | DATE               | Start of record validity                          | From `updated_at` or partition   |                              |
|                                  |           |     | `dtf_end_date`                             | DATE               | End of record validity                            | NULL if current                  |                              |
|                                  |           |     | `dtf_current_flag`                         | BOOLEAN            | TRUE if currently active                          | TRUE/FALSE                       |                              |
|                                  |           |     | `ds_partition_date`                        | STRING             | Partition column (yyyy-MM-dd)                     | Job run date                     | Only used in `_Hist`         |

---

### ✅ Business Use Cases

- Support risk scoring models based on customer wealth tier  
- Identify high-net-worth individuals (HNW) and track movement across tiers  
- Enable segmentation in sales and compliance reviews  
- Enhance alerts for unusual activity inconsistent with wealth level  