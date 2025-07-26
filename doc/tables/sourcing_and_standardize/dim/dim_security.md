## 📜 Table: Dim_Security

This dimension stores investment securities held by customers, including government bonds, corporate securities, and mutual funds. It supports portfolio monitoring, valuation snapshots, and risk analysis of investment behaviors.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Security_ID` (from source)  
- **Partitioned By**: `ds_partition_date` (string, in `_Hist` table only)  
- **Snapshot Strategy**: SCD4a – current record in main table, full history in `_Hist`

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Security | Raw Type  | Standardized/Dim_Security | Standardized Type | Standardized/Dim_Security_Hist | Description                                            | PK  | Value of Technical Field         |
|------------------|-----------|----------------------------|--------------------|-------------------------------|--------------------------------------------------------|-----|----------------------------------|
| `Security_ID`    | STRING    | `Security_ID`              | STRING             | `Security_ID`                 | Unique identifier for the security instrument          | ✅  | Primary key from source          |
| `Customer_ID`    | STRING    | `Customer_ID`              | STRING             | `Customer_ID`                 | Owner of the security                                  |     | FK to `Dim_Customer`             |
| `Security_Type`  | STRING    | `Security_Type`            | STRING             | `Security_Type`               | Type of security (e.g., bond, stock, fund)             |     | ENUM or reference to code table  |
| `Partner_Code`   | STRING    | `Partner_Code`             | STRING             | `Partner_Code`                | Issuer or intermediary for the security                |     | Optional                         |
| `Currency_Code`  | STRING    | `Currency_Code`            | STRING             | `Currency_Code`               | Denomination currency                                  |     | FK to `Dim_Currency`             |
| `Purchase_Date`  | DATE      | `Purchase_Date`            | DATE               | `Purchase_Date`               | Date when the security was acquired                    |     | Used for age and maturity logic  |
| `created_at`     | TIMESTAMP | `created_at`               | TIMESTAMP          | `created_at`                  | Timestamp of first source appearance                   |     | From source                      |
| `updated_at`     | TIMESTAMP | `updated_at`               | TIMESTAMP          | `updated_at`                  | Timestamp of latest update                             |     | From source                      |
| `ds_key`         | STRING    | `ds_key`                   | STRING             | `ds_key`                      | Surrogate primary key                                  | ✅  | Equal to `Security_ID`           |
| `cdc_index`      | INT       | `cdc_index`                | INT                | `cdc_index`                   | 1 = current, 0 = outdated                              |     | Used in filtering                |
| `cdc_change_type`| STRING    | `cdc_change_type`          | STRING             | `cdc_change_type`             | CDC event type                                         |     | `'cdc_insert'`, `'cdc_update'`   |
| `scd_change_timestamp` | TIMESTAMP | `scd_change_timestamp` | TIMESTAMP        | `scd_change_timestamp`        | Timestamp when change was captured                     |     | From `updated_at` or job time    |
| `dtf_start_date` | DATE      | `dtf_start_date`           | DATE               | `dtf_start_date`              | Start date of record validity                          |     | From `updated_at` or partition   |
| `dtf_end_date`   | DATE      | `dtf_end_date`             | DATE               | `dtf_end_date`                | End date of record validity                            |     | NULL if current                  |
| `dtf_current_flag`| BOOLEAN  | `dtf_current_flag`         | BOOLEAN            | `dtf_current_flag`            | TRUE if record is currently valid                      |     | TRUE/FALSE                       |
| *(only in `_Hist`)* |        |                            |                    | `ds_partition_date`           | Partition column (`yyyy-MM-dd`)                        |     | Only in `_Hist` table            |

---

### ✅ Business Use Cases

- Analyze customer investment behavior over time  
- Detect wealth inconsistencies or unusual investment activity  
- Monitor exposure to specific instruments or issuers  
- Support valuation snapshots and risk scoring models  