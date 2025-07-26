## 📜 Table: Dim_Account

This dimension stores detailed account-level information, including type, currency, branch, open/close status, and customer linkage. It enables enrichment of transactions and balances, and supports product lifecycle analysis and AML profiling.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `ds_key`  
- **Partitioned By**: `ds_partition_date` (in `_Hist` table only)  
- **Snapshot Strategy**: SCD4a – current record in main table, full history in `_Hist`

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Account   | Raw Type  | PK (Source) | Standardized/Dim_Account | Standardized Type | Standardized/Dim_Account_Hist | Description                                         | PK  | Value of Technical Field         | Note                      |
|-------------------|-----------|-------------|----------------------------|--------------------|-------------------------------|-----------------------------------------------------|-----|----------------------------------|---------------------------|
| `Account_ID`       | STRING    | ✅          | `Account_ID`              | STRING             | `Account_ID`                  | Unique identifier for the account                   |     |                                  | Natural key from source   |
| `Customer_ID`      | STRING    |             | `Customer_ID`             | STRING             | `Customer_ID`                 | Owner of the account                                |     |                                  | FK to `Dim_Customer`      |
| `Account_Type`     | STRING    |             | `Account_Type`            | STRING             | `Account_Type`                | Type of account (e.g., savings, current)            |     |                                  | Classification            |
| `Currency_Code`    | STRING    |             | `Currency_Code`           | STRING             | `Currency_Code`               | Account currency code                               |     |                                  | FK to `Dim_Currency`      |
| `Branch_Code`      | STRING    |             | `Branch_Code`             | STRING             | `Branch_Code`                 | Opening branch of the account                       |     |                                  | FK to `Dim_Branch`        |
| `Open_Date`        | DATE      |             | `Open_Date`               | DATE               | `Open_Date`                   | Date the account was opened                         |     |                                  |                            |
| `Close_Date`       | DATE      |             | `Close_Date`              | DATE               | `Close_Date`                  | Date the account was closed (nullable)              |     |                                  |                            |
| `Account_Status`   | STRING    |             | `Account_Status`          | STRING             | `Account_Status`              | Status (Active, Dormant, Closed, etc.)              |     |                                  | Lifecycle tracking        |
| `created_at`       | TIMESTAMP |             | `created_at`              | TIMESTAMP          | `created_at`                  | First seen in source                                |     | From source                      |                            |
| `updated_at`       | TIMESTAMP |             | `updated_at`              | TIMESTAMP          | `updated_at`                  | Last update seen in source                          |     | From source                      |                            |
|**Technical Fields**|           |             |                            |                    |                               |                                                     |     |                                  |                            |
|                   |           |             | `ds_key`                  | STRING             | `ds_key`                      | Surrogate primary key for standardized zone         | ✅  | `Account_ID`                     | Required in main + hist    |
|                   |           |             | `cdc_change_type`         | STRING             | `cdc_change_type`             | Type of CDC event                                   |     | `'cdc_insert'`, `'cdc_update'`  | From CDC 1.3               |
|                   |           |             | `cdc_index`               | INT                | `cdc_index`                   | Change capture flag                                 |     | `1` or `0`                       | 1 = current                |
|                   |           |             | `scd_change_timestamp`    | TIMESTAMP          | `scd_change_timestamp`        | Snapshot timestamp                                  |     | `updated_at` or job time        | For audit trail            |
|                   |           |             | `dtf_start_date`          | DATE               | `dtf_start_date`              | Validity start date                                 |     | From `ds_partition_date`        | Required in scd4a          |
|                   |           |             | `dtf_end_date`            | DATE               | `dtf_end_date`                | Validity end date                                   |     | NULL if current                  |                            |
|                   |           |             | `dtf_current_flag`        | BOOLEAN            | `dtf_current_flag`            | Current record flag                                 |     | TRUE or FALSE                    |                            |
|                   |           |             |                            |                    | `ds_partition_date`           | Partition column (`yyyy-MM-dd`)                     |     | Job run date                     | Only in `_Hist` table      |

---

### ✅ Business Use Cases

- Enrich financial facts with account metadata (type, branch, status)  
- Support lifecycle-based fraud rules (e.g., activity on closed accounts)  
- Segment customers by account holdings and activity  
- Enable snapshot tracking of account status for historical profiling