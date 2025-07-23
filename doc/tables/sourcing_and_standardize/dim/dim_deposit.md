## 📜 Table: Dim_Deposit

This dimension provides reference information about deposit products, such as term types, interest conditions, and product codes. It is used to enrich customer holdings, analyze product usage, and support rule logic related to deposits.

- **Type**: Dimension  
- **CDC Type**: `1.1`  
- **Writer Type**: `scd1`  
- **Primary Key**: `Deposit_Product_Code` (from source)  
- **Partitioned By**: `ds_partition_date` (string)  
- **Snapshot Strategy**: Not applicable – overwrite only (SCD1)

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Deposit       | Raw Type  | PK  | Standardized/Dim_Deposit    | Standardized Type | Description                                               | Value of Technical Field       | Note                    |
|------------------------|-----------|-----|-------------------------------|--------------------|-----------------------------------------------------------|-------------------------------|-------------------------|
| `Deposit_Product_Code` | STRING    | ✅  | `Deposit_Product_Code`       | STRING             | Unique product code for the deposit product               |                               | Natural key from source |
| `Deposit_Name`         | STRING    |     | `Deposit_Name`               | STRING             | Marketing name or title of the deposit product            |                               |                         |
| `Deposit_Type`         | STRING    |     | `Deposit_Type`               | STRING             | Type: term deposit, savings, current, etc.                |                               |                         |
| `Currency_Code`        | STRING    |     | `Currency_Code`              | STRING             | Currency used for the deposit                             |                               | FK to `Dim_Currency`    |
| `Interest_Term`        | STRING    |     | `Interest_Term`              | STRING             | Monthly, quarterly, end-of-term, etc.                     |                               |                         |
| `Is_Active`            | BOOLEAN   |     | `Is_Active`                  | BOOLEAN            | Whether the product is currently offered                  |                               | Default = TRUE          |
| `created_at`           | TIMESTAMP |     | `created_at`                 | TIMESTAMP          | Timestamp when first seen in source                       | From source                   |                         |
| `updated_at`           | TIMESTAMP |     | `updated_at`                 | TIMESTAMP          | Last seen update from source                              | From source                   |                         |
| **Technical Fields**   |           |     |                               |                    |                                                           |                               |                         |
|                        |           |     | `ds_key`                     | STRING             | Surrogate primary key for standardized zone               | `Deposit_Product_Code`        | Required in DWH         |
|                        |           |     | `cdc_index`                  | INT                | Change capture flag (always 1 in SCD1)                    | `1`                          |                         |
|                        |           |     | `cdc_change_type`            | STRING             | CDC event type                                            | `'cdc_insert'`               | Insert-only             |
|                        |           |     | `scd_change_timestamp`       | TIMESTAMP          | Processing timestamp                                      | `updated_at` or job time     |                         |
|                        |           |     | `ds_partition_date`          | STRING             | Partition column (`yyyy-MM-dd`)                           | Job run date                 | Required                 |

---

### ✅ Business Use Cases

- Lookup metadata for enrichment of deposit accounts  
- Segment products by type or currency for risk analysis  
- Drive logic for interest accrual, maturity alerts, and limits  
- Ensure deposit records align to regulated product catalog  