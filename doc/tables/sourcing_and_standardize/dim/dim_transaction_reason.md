## 📜 Table: Dim_Transaction_Reason

This dimension table defines the underlying business or behavioral reasons for financial transactions. It supports AML risk tagging, transaction classification, and contextual enrichment of suspicious activity patterns.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd2`  
- **Primary Key**: `Reason_Code`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Controlled vocabulary of transaction reasons (e.g., salary, donation, loan repayment) with associated risk levels.

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Transaction_Reason | Raw Type | Standardized/std_Transaction_Reason | Standardized Type | Standardized/std_Transaction_Reason_Hist | Description                                     | PK  | Note                     |
|----------------------------|----------|-------------------------------------|-------------------|-------------------------------------------|-------------------------------------------------|-----|--------------------------|
| `Reason_Code`              | VARCHAR  | `Reason_Code`                       | VARCHAR           | `Reason_Code`                              | Code representing reason for transaction        | ✅  | Primary key              |
| `Reason_Desc`              | VARCHAR  | `Reason_Desc`                       | VARCHAR           | `Reason_Desc`                              | Description of transaction purpose              |     | Used for classification  |
| `Risk_Level`               | VARCHAR  | `Risk_Level`                        | VARCHAR           | `Risk_Level`                               | LOW, MEDIUM, HIGH (risk severity)               |     | Links to `Dim_Risk_Level` |
| `created_at`               | TIMESTAMP| `created_at`                        | TIMESTAMP         | `created_at`                               | Record creation timestamp                       |     | From source system        |
| `updated_at`               | TIMESTAMP| `updated_at`                        | TIMESTAMP         | `updated_at`                               | Record last modified timestamp                  |     | Required for CDC 1.3      |
|Technical Fields (for CDC + audit + snapshot logic)|
|                            |          | `scd_change_type`                   | STRING            | `scd_change_type`                          | `'cdc_insert'`, `'cdc_update'`, `'cdc_delete'` |     | SCD2 logic                |
|                            |          | `cdc_index`                         | INT               | `cdc_index`                                | Ingestion order checkpoint                      |     | Optional                  |
|                            |          | `scd_change_timestamp`              | TIMESTAMP         | `scd_change_timestamp`                     | Timestamp of CDC ingestion                      |     | Required                  |
|                            |          | `dtf_start_date`                    | DATE              | `dtf_start_date`                           | Version start validity                          |     |                          |
|                            |          | `dtf_end_date`                      | DATE              | `dtf_end_date`                             | Version end validity (NULL = active)            |     |                          |
|                            |          | `dtf_current_flag`                  | BOOLEAN           | `dtf_current_flag`                         | TRUE = current active version                   |     |                          |
|                            |          |                                     |                   | `ds_partition_date`                        | Partition column for history table              |     | `_Hist` table only        |

---

### ✅ Business Use Cases

- Classify transactions by behavioral intent for AML profiling  
- Join with `Fact_Transaction` to contextualize suspicious patterns  
- Tag high-risk transaction types (e.g., offshore transfers, cash deposits)  
- Use in scoring and alert generation for unusual or misaligned transaction justifications