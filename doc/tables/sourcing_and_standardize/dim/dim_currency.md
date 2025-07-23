## 📜 Table: Dim_Currency

This dimension contains reference data for currencies, including ISO codes, currency names, and official exchange rates. It is used in transaction normalization, reporting, and FX-based risk calculations.

- **Type**: Dimension  
- **CDC Type**: `1.1`  
- **Writer Type**: `scd1`  
- **Primary Key**: `Currency_Code` (from source)  
- **Partitioned By**: `ds_partition_date` (string)  
- **Snapshot Strategy**: Not applicable – overwrite only (SCD1)

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Currency | Raw Type  | PK  | Standardized/Dim_Currency | Standardized Type | Description                                         | Value of Technical Field       | Note                      |
|------------------|-----------|-----|-----------------------------|--------------------|-----------------------------------------------------|-------------------------------|---------------------------|
| `Currency_Code`  | STRING    | ✅  | `Currency_Code`            | STRING             | ISO 4217 currency code                              |                               | Natural key from source   |
| `Currency_Name`  | STRING    |     | `Currency_Name`            | STRING             | Full name of the currency                          |                               |                           |
| `Country_Code`   | STRING    |     | `Country_Code`             | STRING             | Country using this currency                         |                               | FK to `Dim_Country`       |
| `FX_Rate_to_USD` | DECIMAL   |     | `FX_Rate_to_USD`           | DECIMAL(18,6)      | Exchange rate to USD                                |                               | Optional                   |
| `Is_Active`      | BOOLEAN   |     | `Is_Active`                | BOOLEAN            | Whether this currency is currently in use           |                               | Default = TRUE            |
| `created_at`     | TIMESTAMP |     | `created_at`               | TIMESTAMP          | First seen in source                                | From source                   |                           |
| `updated_at`     | TIMESTAMP |     | `updated_at`               | TIMESTAMP          | Last seen update in source                          | From source                   |                           |
| **Technical Fields** |       |     |                             |                    |                                                     |                               |                           |
|                  |           |     | `ds_key`                   | STRING             | Surrogate primary key for standardized zone         | `Currency_Code`              | Required in DWH           |
|                  |           |     | `cdc_index`                | INT                | Change capture flag (always 1 in SCD1)              | `1`                          |                           |
|                  |           |     | `cdc_change_type`          | STRING             | CDC event type                                      | `'cdc_insert'`               | Insert-only               |
|                  |           |     | `scd_change_timestamp`     | TIMESTAMP          | Time of ETL processing                              | `updated_at` or job time     |                           |
|                  |           |     | `ds_partition_date`        | STRING             | Partition column (`yyyy-MM-dd`)                     | Job run date                 | Required                  |

---

### ✅ Business Use Cases

- Normalize monetary values across transaction systems  
- Drive multi-currency dashboards and FX exposure models  
- Power AML rules that compare USD equivalents  
- Ensure referential consistency in all financial facts  