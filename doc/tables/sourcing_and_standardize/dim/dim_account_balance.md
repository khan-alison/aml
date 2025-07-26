## 📜 Table: Dim_Account_Balance

This dimension stores **daily snapshots of account balances** to enable point-in-time analysis of financial behavior. It is essential for AML trend detection, structuring detection, and historical reconstruction of account value.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `ds_key`  
- **Partitioned By**: `ds_partition_date` (in `_Hist` table only)  
- **Snapshot Strategy**: Full daily overwrite to `_Hist`; current view in main table

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Account_Balance | Raw Type  | PK (Source) | Standardized/Dim_Account_Balance | Standardized Type | Standardized/Dim_Account_Balance_Hist | Description                                      | PK  | Value of Technical Field       | Note                         |
|-------------------------|-----------|-------------|----------------------------------|-------------------|----------------------------------------|--------------------------------------------------|-----|-------------------------------|------------------------------|
| `Account_ID`            | STRING    | ✅          | `Account_ID`                     | STRING            | `Account_ID`                           | Unique identifier for the account               |     |                               | FK to `Dim_Account`         |
| `Balance_Date`          | DATE      | ✅          | `Snapshot_Date`                  | DATE              | `Snapshot_Date`                        | Date of the balance snapshot                    |     |                               | Used for time-based joins   |
| `Currency_Code`         | STRING    |             | `Currency_Code`                  | STRING            | `Currency_Code`                        | Currency of the balance                         |     |                               | FK to `Dim_Currency`        |
| `Product_Type_Code`     | STRING    |             | `Product_Type_Code`              | STRING            | `Product_Type_Code`                    | Deposit/Loan type                               |     |                               | FK to `Dim_Deposit`         |
| `Account_Balance`       | DECIMAL   |             | `Account_Balance`                | DECIMAL           | `Account_Balance`                      | Balance amount at snapshot date                 |     |                               |                              |
| `created_at`            | TIMESTAMP |             | `created_at`                     | TIMESTAMP         | `created_at`                           | When balance record was first seen              |     | From source                   |                              |
| `updated_at`            | TIMESTAMP |             | `updated_at`                     | TIMESTAMP         | `updated_at`                           | Last update from source                         |     | From source                   |                              |
|**Technical Field**|
| `ds_key`                |           |             | `ds_key`                         | STRING            | `ds_key`                               | Surrogate primary key                           | ✅  | `md5(Account_ID || Balance_Date)` | Composite business key   |
| `cdc_change_type`       |           |             | `cdc_change_type`                | STRING            | `cdc_change_type`                      | CDC change type (insert/update)                 |     | `'cdc_insert'` or `'cdc_update'` | From CDC logic             |
| `cdc_index`             |           |             | `cdc_index`                      | INT               | `cdc_index`                            | 1 = current, 0 = outdated                       |     | `1`                          | Used in filter logic         |
| `scd_change_timestamp`  |           |             | `scd_change_timestamp`           | TIMESTAMP         | `scd_change_timestamp`                 | Timestamp of this snapshot                      |     | `updated_at` or job run time |                              |
| `dtf_start_date`        |           |             | `dtf_start_date`                 | DATE              | `dtf_start_date`                       | Start date of this version                      |     | `ds_partition_date`          | For SCD4a tracking           |
| `dtf_end_date`          |           |             | `dtf_end_date`                   | DATE              | `dtf_end_date`                         | End date (null if current)                      |     | `NULL`                       | SCD4a tracking               |
| `dtf_current_flag`      |           |             | `dtf_current_flag`               | BOOLEAN           | `dtf_current_flag`                     | Whether this is the latest version              |     | `TRUE` or `FALSE`            | For current/historical split |
| `ds_partition_date`     |           |             |                                  | STRING            | `ds_partition_date`                    | Partition column                                |     | Job run date (yyyy-MM-dd)   | Only in `_Hist`              |

---

### ✅ Business Use Cases

- Monitor sudden balance increases that may indicate placement  
- Support derived metrics like balance volatility or trend scores  
- Drive historical backtesting for transaction-based behavior  
- Enable regulatory audit trails and historical reconstructions