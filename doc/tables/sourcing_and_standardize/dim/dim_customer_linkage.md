## 📜 Table: Dim_Customer_Linkage

This dimension defines known or inferred relationships between customers, including family, legal, or transactional links. It supports network analysis, complex fraud detection, and enhanced due diligence of related parties.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Linkage_ID` (from source)  
- **Partitioned By**: `ds_partition_date` (string, in `_Hist` table only)  
- **Snapshot Strategy**: SCD4a – current version in main table, full history in `_Hist`

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Customer_Linkage | Raw Type  | PK  | Standardized/Dim_Customer_Linkage | Standardized Type | Description                                        | Value of Technical Field         | Note                          |
|---------------------------|-----------|-----|------------------------------------|--------------------|----------------------------------------------------|----------------------------------|-------------------------------|
| `Linkage_ID`              | STRING    | ✅  | `Linkage_ID`                       | STRING             | Unique identifier for the customer relationship    |                                  | Natural key from source       |
| `Customer_ID_1`           | STRING    |     | `Customer_ID_1`                    | STRING             | First customer in the relationship                 |                                  | FK to `Dim_Customer`         |
| `Customer_ID_2`           | STRING    |     | `Customer_ID_2`                    | STRING             | Second customer in the relationship                |                                  | FK to `Dim_Customer`         |
| `Link_Type`               | STRING    |     | `Link_Type`                        | STRING             | Type of relationship (e.g., family, legal, shared) |                                  | Controlled list              |
| `Link_Confidence`         | DECIMAL   |     | `Link_Confidence`                  | DECIMAL(5,2)       | Score representing strength of inferred link       |                                  | Optional                     |
| `Is_Active`               | BOOLEAN   |     | `Is_Active`                        | BOOLEAN            | Whether the relationship is still valid            |                                  | Used for filtering           |
| `created_at`              | TIMESTAMP |     | `created_at`                       | TIMESTAMP          | When the relationship was first recorded           | From source                      |                              |
| `updated_at`              | TIMESTAMP |     | `updated_at`                       | TIMESTAMP          | Last update of the relationship                    | From source                      |                              |
| **Technical Fields**      |           |     |                                    |                    |                                                    |                                  |                              |
|                           |           |     | `ds_key`                           | STRING             | Surrogate primary key in standardized zone         | `Linkage_ID`                     | Required for scd4a            |
|                           |           |     | `cdc_index`                        | INT                | 1 = current, 0 = outdated                          | `1` or `0`                       | SCD4a filter flag             |
|                           |           |     | `cdc_change_type`                  | STRING             | CDC event type                                     | `'cdc_insert'`, `'cdc_update'`  |                              |
|                           |           |     | `scd_change_timestamp`             | TIMESTAMP          | Snapshot timestamp                                 | `updated_at` or job time         |                              |
|                           |           |     | `dtf_start_date`                   | DATE               | Start of validity                                  | From `updated_at` or partition   |                              |
|                           |           |     | `dtf_end_date`                     | DATE               | End of validity                                    | NULL if current                  |                              |
|                           |           |     | `dtf_current_flag`                 | BOOLEAN            | TRUE if current version                            | TRUE/FALSE                       | Required for scd4a            |
|                           |           |     | `ds_partition_date`                | STRING             | Partition column (`yyyy-MM-dd`)                    | Job run date                     | Used in `_Hist` only          |

---

### ✅ Business Use Cases

- Identify hidden links between customers to detect collusion  
- Enhance investigations through network analysis and link scoring  
- Support rules that escalate based on proximity to high-risk individuals  
- Aid case management by grouping connected parties  