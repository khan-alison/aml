## 📜 Table: Fact_Risk_Score

This table stores risk scores calculated for each customer on a specific day. It includes scoring details, band categorization, contributing rules, and whether the score was overridden. Used in AML decisioning, segmentation, and model explainability.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factUpsert`  
- **Primary Key**: Composite key – `(Customer_ID, Score_Date)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Contains customer-level risk scores with driving factor explanations. Supports both model-based and rule-based risk assessments.

---

### 📊 Key Columns (Standardize)

| Raw/Fact_Risk_Score   | Raw Type | Standardized/Fact_Risk_Score   | Standardized Type | Description                                      | PK  | Note                         |
|------------------------|----------|----------------------------------|--------------------|--------------------------------------------------|-----|------------------------------|
| `Customer_ID`          | VARCHAR  | `Customer_ID`                   | VARCHAR            | Customer identifier                              | ✅  | FK to `Dim_Customer`         |
| `Score_Date`           | DATE     | `Score_Date`                    | DATE               | Date the risk score was calculated               | ✅  | FK to `Dim_Time`             |
| `Score_Value`          | DECIMAL  | `Score_Value`                   | DECIMAL            | Risk score (numeric)                             |     | Used in banding logic        |
| `Score_Band`           | VARCHAR  | `Score_Band`                    | VARCHAR            | Risk level category (e.g., LOW, MEDIUM, HIGH)    |     | Derived from score thresholds|
| `Driving_Rules`        | TEXT     | `Driving_Rules`                 | TEXT               | Description or list of contributing rules        |     | JSON, pipe-delimited, or text|
| `Override_Flag`        | BOOLEAN  | `Override_Flag`                 | BOOLEAN            | TRUE if score manually overridden                |     | Regulatory audit relevance   |
|Technical Fields (Standardize)|
|                        |          | `cdc_change_type`               | STRING             | `'cdc_insert'` or `'cdc_update'`                |     | CDC 1.3 logic                 |
|                        |          | `cdc_index`                     | INT                | Change index for deduplication                   |     | Optional                     |
|                        |          | `scd_change_timestamp`          | TIMESTAMP          | Load timestamp into lake                         |     |                              |
|                        |          | `ds_partition_date`             | DATE               | Partitioning field, usually = `Score_Date`       |     |                              |
|                        |          | `created_at`                    | TIMESTAMP          | Initial creation timestamp                       |     |                              |
|                        |          | `updated_at`                    | TIMESTAMP          | Last update timestamp                            |     |                              |

---

### ✅ Notes
- Enables daily customer risk profiling  
- Compatible with scoring models and rule-based aggregations  
- `Driving_Rules` improves model transparency and auditability  