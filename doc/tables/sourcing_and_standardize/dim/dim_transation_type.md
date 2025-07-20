## 📜 Table: Dim_Transaction_Type

This dimension defines the classification and description of each transaction type (e.g., cash withdrawal, online transfer). It is used to categorize transactions in fact tables for AML analysis, fee policy mapping, and reporting.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd2`  
- **Primary Key**: `Transaction_Type_ID`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Maintains a reference list of transaction types used across financial systems and channels.

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Transaction_Type | Raw Type | Standardized/std_Transaction_Type | Standardized Type | Standardized/std_Transaction_Type_Hist | Description                                 | PK  | Note          |
|---------------------------|----------|-----------------------------------|-------------------|-----------------------------------------|---------------------------------------------|-----|---------------|
| `Transaction_Type_ID`     | VARCHAR  | `Transaction_Type_ID`             | VARCHAR           | `Transaction_Type_ID`                   | Unique ID for the transaction type          | ✅  | Primary key   |
| `Transaction_Code`        | VARCHAR  | `Transaction_Code`                | VARCHAR           | `Transaction_Code`                      | Internal or external code (e.g., TR001)     |     | Used in joins |
| `Description`             | VARCHAR  | `Description`                     | VARCHAR           | `Description`                           | Human-readable transaction type label       |     |               |
| `created_at`              | TIMESTAMP| `created_at`                      | TIMESTAMP         | `created_at`                             | Record creation timestamp                   |     | CDC 1.3        |
| `updated_at`              | TIMESTAMP| `updated_at`                      | TIMESTAMP         | `updated_at`                             | Last modified timestamp                     |     | CDC 1.3        |
|Technical Fields (for CDC + audit + snapshot logic)|
|                           |          | `scd_change_type`                 | STRING            | `scd_change_type`                        | `'cdc_insert'`, `'cdc_update'`, `'cdc_delete'` |     | SCD2 tracking |
|                           |          | `cdc_index`                       | INT               | `cdc_index`                              | Ingestion index                             |     | Optional       |
|                           |          | `scd_change_timestamp`           | TIMESTAMP         | `scd_change_timestamp`                   | Time of ingestion                           |     | Audit field    |
|                           |          | `dtf_start_date`                 | DATE              | `dtf_start_date`                         | SCD2 effective start date                   |     |                |
|                           |          | `dtf_end_date`                   | DATE              | `dtf_end_date`                           | SCD2 effective end date                     |     | NULL = active  |
|                           |          | `dtf_current_flag`               | BOOLEAN           | `dtf_current_flag`                       | TRUE = currently active version             |     |                |
|                           |          |                                  |                   | `ds_partition_date`                      | Partition field for history table           |     | `_Hist` only   |

---

### ✅ Business Use Cases

- Categorize transactions for rule-based AML detection  
- Join with `Fact_Transaction` or `Fact_Card_Transaction`  
- Filter dashboards by transaction types  
- Identify uncommon or suspicious transaction behavior