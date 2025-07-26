## 📜 Table: Dim_Customer_Linkage

This dimension defines known or inferred relationships between customers, including family, legal, or transactional links. It supports network analysis, complex fraud detection, and enhanced due diligence of related parties.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `ds_key`  
- **Main Table**: `Dim_Customer_Linkage` – holds only the latest active version  
- **History Table**: `Dim_Customer_Linkage_Hist` – stores full relationship history  
- **Partitioned By**: `ds_partition_date` (in `_Hist` table only)  
- **Snapshot Strategy**: SCD4a – current version in main table, full history in `_Hist`

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Customer_Linkage | Raw Type  | PK (Source) | Standardized/Dim_Customer_Linkage | Standardized Type | Standardized/Dim_Customer_Linkage_Hist | Description                                        | PK  | Value of Technical Field         | Note                          |
|---------------------------|-----------|-------------|------------------------------------|--------------------|----------------------------------------|----------------------------------------------------|-----|----------------------------------|-------------------------------|
| `Linkage_ID`              | STRING    | ✅          | `Linkage_ID`                       | STRING             | `Linkage_ID`                           | Unique identifier for the customer relationship    |     |                                  | Natural key from source       |
| `Customer_ID_1`           | STRING    |             | `Customer_ID_1`                    | STRING             | `Customer_ID_1`                        | First customer in the relationship                 |     |                                  | FK to `Dim_Customer`         |
| `Customer_ID_2`           | STRING    |             | `Customer_ID_2`                    | STRING             | `Customer_ID_2`                        | Second customer in the relationship                |     |                                  | FK to `Dim_Customer`         |
| `Link_Type`               | STRING    |             | `Link_Type`                        | STRING             | `Link_Type`                            | Type of relationship (e.g., family, legal, shared) |     |                                  | Controlled list              |
| `Link_Confidence`         | DECIMAL   |             | `Link_Confidence`                  | DECIMAL(5,2)       | `Link_Confidence`                      | Score representing strength of inferred link       |     |                                  | Optional                     |
| `Is_Active`               | BOOLEAN   |             | `Is_Active`                        | BOOLEAN            | `Is_Active`                            | Whether the relationship is still valid            |     |                                  | Used for filtering           |
| `created_at`              | TIMESTAMP |             | `created_at`                       | TIMESTAMP          | `created_at`                           | When the relationship was first recorded           |     | From source                      |                              |
| `updated_at`              | TIMESTAMP |             | `updated_at`                       | TIMESTAMP          | `updated_at`                           | Last update of the relationship                    |     | From source                      |                              |
| **Technical Fields**      |           |             |                                    |                    |                                        |                                                    |     |                                  |                              |
|                           |           |             | `ds_key`                           | STRING             | `ds_key`                               | Surrogate primary key in standardized zone         | ✅  | `Linkage_ID`                     | Required for SCD4a            |
|                           |           |             | `cdc_index`                        | INT                | `cdc_index`                            | 1 = current, 0 = outdated                          |     | `1` or `0`                       | SCD4a filter flag             |
|                           |           |             | `cdc_change_type`                  | STRING             | `cdc_change_type`                      | CDC event type                                     |     | `'cdc_insert'`, `'cdc_update'`  |                              |
|                           |           |             | `scd_change_timestamp`             | TIMESTAMP          | `scd_change_timestamp`                 | Snapshot timestamp                                 |     | `updated_at` or job time         |                              |
|                           |           |             | `dtf_start_date`                   | DATE               | `dtf_start_date`                       | Start of validity                                  |     | From `updated_at` or partition   |                              |
|                           |           |             | `dtf_end_date`                     | DATE               | `dtf_end_date`                         | End of validity                                    |     | NULL if current                  |                              |
|                           |           |             | `dtf_current_flag`                 | BOOLEAN            | `dtf_current_flag`                     | TRUE if current version                            |     | TRUE/FALSE                       | Required for scd4a            |
|                           |           |             |                                    |                    | `ds_partition_date`                    | Partition column (`yyyy-MM-dd`)                    |     | Job run date                     | Used in `_Hist` only          |

---

### ✅ Business Use Cases

- Identify hidden links between customers to detect collusion  
- Enhance investigations through network analysis and link scoring  
- Support rules that escalate based on proximity to high-risk individuals  
- Aid case management by grouping connected parties  