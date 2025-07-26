## 📜 Table: Dim_Customer_Wealth_Profile

This dimension estimates customer wealth classification over time. It is used in customer risk scoring, high-net-worth monitoring, and behavioral profiling. The values evolve and are tracked using SCD4a strategy.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `ds_key`  
- **Main Table**: `Dim_Customer_Wealth_Profile` – stores current wealth status only  
- **History Table**: `Dim_Customer_Wealth_Profile_Hist` – stores full change history  
- **Partitioned By**: `ds_partition_date` (only in `_Hist` table)  
- **Snapshot Strategy**: SCD4a – current version in main, historical traceability in `_Hist`

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Customer_Wealth_Profile | Raw Type  | PK (Source) | Standardized/Dim_Customer_Wealth_Profile | Standardized Type | Standardized/Dim_Customer_Wealth_Profile_Hist | Description                                        | PK  | Value of Technical Field         | Note                          |
|----------------------------------|-----------|-------------|-------------------------------------------|--------------------|-----------------------------------------------|----------------------------------------------------|-----|----------------------------------|-------------------------------|
| `Customer_ID`                    | STRING    | ✅          | `Customer_ID`                             | STRING             | Customer identifier                               |     |                                  | FK to `Dim_Customer`         |
| `Wealth_Tier`                    | STRING    |             | `Wealth_Tier`                             | STRING             | Tier category (e.g., Mass, Affluent, HNW)         |     |                                  | Mapped from score/rules      |
| `Wealth_Score`                   | INT       |             | `Wealth_Score`                            | INT                | Numeric wealth score used for segmentation        |     |                                  | Can be derived or sourced    |
| `Est_Annual_Income`             | DECIMAL   |             | `Est_Annual_Income`                       | DECIMAL(18,2)      | Estimated annual income                           |     |                                  | Optional                     |
| `Est_Total_Assets`              | DECIMAL   |             | `Est_Total_Assets`                        | DECIMAL(18,2)      | Estimated total assets held                       |     |                                  | Optional                     |
| `created_at`                    | TIMESTAMP |             | `created_at`                              | TIMESTAMP          | First seen in source                              |     | From source                      |                              |
| `updated_at`                    | TIMESTAMP |             | `updated_at`                              | TIMESTAMP          | Last seen update in source                        |     | From source                      |                              |
| **Technical Fields**            |           |             |                                           |                    |                                                  |                                                    |     |                                  |                              |
|                                  |           |             | `ds_key`                                   | STRING             | Surrogate primary key                             | ✅  | `md5(Customer_ID)`              | Replaces raw PK              |
|                                  |           |             | `cdc_index`                                | INT                | Current record flag                               |     | `1` or `0`                       | 1 = current version          |
|                                  |           |             | `cdc_change_type`                          | STRING             | Type of change                                    |     | `'cdc_insert'` or `'cdc_update'`| From CDC engine              |
|                                  |           |             | `scd_change_timestamp`                     | TIMESTAMP          | Change detection timestamp                        |     | `updated_at` or job time        |                              |
|                                  |           |             | `dtf_start_date`                           | DATE               | Start of record validity                          |     | From `ds_partition_date`        | Used in SCD4a tracking       |
|                                  |           |             | `dtf_end_date`                             | DATE               | End of record validity                            |     | NULL if current                  |                              |
|                                  |           |             | `dtf_current_flag`                         | BOOLEAN            | TRUE if currently active                          |     | TRUE/FALSE                       |                              |
|                                  |           |             |                                            |                    | `ds_partition_date`                              | Partition column for `_Hist` only                   |     | Job run date `yyyy-MM-dd`       | Not present in main table    |

---

### ✅ Business Use Cases

- Support risk scoring models based on customer wealth tier  
- Identify high-net-worth individuals (HNW) and track movement across tiers  
- Enable segmentation in sales and compliance reviews  
- Enhance alerts for unusual activity inconsistent with wealth level  