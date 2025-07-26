## 📜 Table: Dim_Transaction_Type

This dimension defines the reference types of transactions (e.g., transfer, withdrawal, deposit). It is used to categorize transaction activity and support filtering, classification, and rule-based AML logic.

- **Type**: Dimension  
- **CDC Type**: `1.1`  
- **Writer Type**: `scd1`  
- **Primary Key**: `Transaction_Type_Code` (from source)  
- **Partitioned By**: `ds_partition_date` (string)  
- **Snapshot Strategy**: Not applicable – overwrite-only (SCD1)

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Transaction_Type | Raw Type  | PK  | Standardized/Dim_Transaction_Type | Standardized Type | Description                                       | Value of Technical Field       | Note                    |
|--------------------------|-----------|-----|-----------------------------------|--------------------|---------------------------------------------------|-------------------------------|-------------------------|
| `Transaction_Type_Code`  | STRING    | ✅  | `Transaction_Type_Code`          | STRING             | Unique transaction type code                      |                               | Natural key from source |
| `Transaction_Type_Name`  | STRING    |     | `Transaction_Type_Name`          | STRING             | Human-readable description of the type            |                               |                         |
| `Is_Active`              | BOOLEAN   |     | `Is_Active`                      | BOOLEAN            | Whether this transaction type is currently valid  |                               | Default = TRUE          |
| `created_at`             | TIMESTAMP |     | `created_at`                     | TIMESTAMP          | First seen in source                              | From source                   |                         |
| `updated_at`             | TIMESTAMP |     | `updated_at`                     | TIMESTAMP          | Last update seen in source                        | From source                   |                         |
| **Technical Fields**     |           |     |                                   |                    |                                                   |                               |                         |
|                          |           |     | `ds_key`                         | STRING             | Surrogate primary key for standardized zone       | `Transaction_Type_Code`      | Required in DWH         |
|                          |           |     | `cdc_index`                      | INT                | Change flag (always 1 in SCD1)                    | `1`                          |                         |
|                          |           |     | `cdc_change_type`                | STRING             | Type of CDC event                                 | `'cdc_insert'`               | Insert-only             |
|                          |           |     | `scd_change_timestamp`           | TIMESTAMP          | Processing time                                   | `updated_at` or job time     |                         |
|                          |           |     | `ds_partition_date`              | STRING             | Partition column in format `yyyy-MM-dd`           | Job run date                 | Required                |

---

### ✅ Business Use Cases

- Categorize transactions for rule-based detection and aggregation  
- Power filters in dashboards and analytics  
- Provide input for derived metrics such as velocity by type  
- Support referential joins in `Fact_Transaction`, `Fact_Forex_Transaction`, etc.  