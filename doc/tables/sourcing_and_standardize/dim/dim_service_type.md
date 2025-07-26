## 📜 Table: Dim_Service_Type

This dimension contains the classification of services provided by the bank, such as payments, collections, transfers, and remittances. It supports operational grouping, transaction tagging, and compliance categorization.

- **Type**: Dimension  
- **CDC Type**: `1.1`  
- **Writer Type**: `scd1`  
- **Primary Key**: `Service_Type_Code` (from source)  
- **Partitioned By**: `ds_partition_date` (string)  
- **Snapshot Strategy**: Not applicable – overwrite-only (SCD1)

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Service_Type | Raw Type  | PK  | Standardized/Dim_Service_Type | Standardized Type | Description                                      | Value of Technical Field       | Note                    |
|----------------------|-----------|-----|-------------------------------|--------------------|--------------------------------------------------|-------------------------------|-------------------------|
| `Service_Type_Code`  | STRING    | ✅  | `Service_Type_Code`          | STRING             | Unique code for the service category             |                               | Natural key from source |
| `Service_Type_Name`  | STRING    |     | `Service_Type_Name`          | STRING             | Descriptive name for the service type            |                               |                         |
| `Is_Active`          | BOOLEAN   |     | `Is_Active`                  | BOOLEAN            | Whether this service type is currently in use    |                               | Default = TRUE          |
| `created_at`         | TIMESTAMP |     | `created_at`                 | TIMESTAMP          | First seen in source                             | From source                   |                         |
| `updated_at`         | TIMESTAMP |     | `updated_at`                 | TIMESTAMP          | Last update in source                            | From source                   |                         |
| **Technical Fields** |           |     |                               |                    |                                                  |                               |                         |
|                      |           |     | `ds_key`                     | STRING             | Surrogate key for the standardized zone          | `Service_Type_Code`           | Required                |
|                      |           |     | `cdc_index`                  | INT                | CDC flag (always 1 for SCD1)                     | `1`                          |                         |
|                      |           |     | `cdc_change_type`            | STRING             | CDC event type                                   | `'cdc_insert'`               |                         |
|                      |           |     | `scd_change_timestamp`       | TIMESTAMP          | Processing or ingestion timestamp                | `updated_at` or job time     |                         |
|                      |           |     | `ds_partition_date`          | STRING             | Partition column in format `yyyy-MM-dd`          | Job run date                 | Required                |

---

### ✅ Business Use Cases

- Standardize classification of services across transaction data  
- Power rule logic and analytical segmentation  
- Enable filtering of transaction flows by service type  
- Support joins with `Fact_Transaction`, `Fact_Funds_Transfer`, etc.  