## 📜 Table: Fact_Risk_Score

This table stores risk scores calculated for each customer on a specific day. It includes scoring details, band categorization, contributing rules, and whether the score was overridden. Used in AML decisioning, segmentation, and model explainability.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factUpsert`  
- **Primary Key**: Composite key – `(Customer_ID, Score_Date)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Contains customer-level risk scores with driving factor explanations. Supports both model-based and rule-based risk assessments.

---

### 🔗 Foreign Keys and Relationships:

| Column         | Referenced Table       | Description |
|----------------|------------------------|-------------|
| `Customer_ID`  | `Dim_Customer`         | Customer associated with the score  |
| `Score_Date`   | `Dim_Time`             | Date when the score was computed    |

---

### 📊 Key Columns:

| Raw Column Name     | Raw Type | Standardized Column Name | Standardized Type | Description                                      | PK  | Note                   |
|---------------------|----------|---------------------------|--------------------|--------------------------------------------------|-----|------------------------|
| `Customer_ID`       | VARCHAR  | `Customer_ID`             | VARCHAR            | Customer identifier                              | ✅  | FK to `Dim_Customer`   |
| `Score_Date`        | DATE     | `Score_Date`              | DATE               | Scoring snapshot date                            | ✅  | FK to `Dim_Time`       |
| `Score_Value`       | DECIMAL  | `Score_Value`             | DECIMAL            | Numerical risk score value                       |     |                        |
| `Score_Band`        | VARCHAR  | `Score_Band`              | VARCHAR            | Categorical band (e.g., Low, Medium, High)       |     | Derived from score     |
| `Driving_Rules`     | TEXT     | `Driving_Rules`           | TEXT               | Text summary of rules contributing to the score |     | JSON or pipe-delimited |
| `Override_Flag`     | BOOLEAN  | `Override_Flag`           | BOOLEAN            | Manual override applied                          |     |                        |

---

### 🧪 Technical Fields (for CDC + audit):

| Raw Column Name        | Raw Type | Standardized Column Name | Standardized Type | Description                               | PK  | Note |
|------------------------|----------|---------------------------|--------------------|-------------------------------------------|-----|------|
| `cdc_change_type`      | STRING   | `cdc_change_type`         | STRING             | `'cdc_insert'` or `'cdc_update'`          |     | CDC 1.3 logic           |
| `cdc_index`            | INT      | `cdc_index`               | INT                | Sequence/order indicator                  |     | Optional                |
| `scd_change_timestamp` | TIMESTAMP| `scd_change_timestamp`    | TIMESTAMP          | Time record was processed                 |     |                          |
| `ds_partition_date`    | DATE     | `ds_partition_date`       | DATE               | Partition column (aligned with Score_Date)|     |                          |
| `created_at`           | TIMESTAMP| `created_at`              | TIMESTAMP          | Insertion time                            |     |                          |
| `updated_at`           | TIMESTAMP| `updated_at`              | TIMESTAMP          | Last update time                          |     |                          |

---

### ✅ Notes:
- Used for risk stratification and triggering alerts
- Compatible with both model-driven and rule-driven scoring logic
- Driving rules support transparency and explainability
