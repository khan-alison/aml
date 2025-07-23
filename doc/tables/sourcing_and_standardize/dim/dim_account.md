## 📜 Table: Dim_Account

This dimension stores detailed account-level information, including type, currency, branch, open/close status, and customer linkage. It enables enrichment of transactions and balances, and supports product lifecycle analysis and AML profiling.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Account_ID` (from source)  
- **Partitioned By**: `ds_partition_date` (string, in `_Hist` table only)  
- **Snapshot Strategy**: SCD4a – current record in main table, full history in `_Hist`

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Account   | Raw Type  | PK  | Standardized/Dim_Account | Standardized Type | Description                                         | Value of Technical Field         | Note                      |
|-------------------|-----------|-----|----------------------------|--------------------|-----------------------------------------------------|----------------------------------|---------------------------|
| `Account_ID`       | STRING    | ✅  | `Account_ID`              | STRING             | Unique identifier for the account                   |                                  | Natural key from source   |
| `Customer_ID`      | STRING    |     | `Customer_ID`             | STRING             | Owner of the account                                |                                  | FK to `Dim_Customer`      |
| `Account_Type`     | STRING    |     | `Account_Type`            | STRING             | Type of account (e.g., savings, current)            |                                  | Classification            |
| `Currency_Code`    | STRING    |     | `Currency_Code`           | STRING             | Account currency code                               |                                  | FK to `Dim_Currency`      |
| `Branch_Code`      | STRING    |     | `Branch_Code`             | STRING             | Opening branch of the account                       |                                  | FK to `Dim_Branch`        |
| `Open_Date`        | DATE      |     | `Open_Date`               | DATE               | Date the account was opened                         |                                  |                            |
| `Close_Date`       | DATE      |     | `Close_Date`              | DATE               | Date the account was closed (nullable)              |                                  |                            |
| `Account_Status`   | STRING    |     | `Account_Status`          | STRING             | Status (Active, Dormant, Closed, etc.)              |                                  | Lifecycle tracking        |
| `created_at`       | TIMESTAMP |     | `created_at`              | TIMESTAMP          | First seen in source                                | From source                      |                            |
| `updated_at`       | TIMESTAMP |     | `updated_at`              | TIMESTAMP          | Last update seen in source                          | From source                      |                            |
| **Technical Fields** |         |     |                            |                    |                                                     |                                  |                            |
|                   |           |     | `ds_key`                  | STRING             | Surrogate primary key for standardized zone         | `Account_ID`                     | Required in DWH            |
|                   |           |     | `cdc_index`               | INT                | Change capture flag                                 | `1` or `0`                       | 1 = current                |
|                   |           |     | `cdc_change_type`         | STRING             | Type of CDC event                                   | `'cdc_insert'`, `'cdc_update'`  |                            |
|                   |           |     | `scd_change_timestamp`    | TIMESTAMP          | Snapshot timestamp                                  | `updated_at` or job timestamp    |                            |
|                   |           |     | `dtf_start_date`          | DATE               | Validity start date                                 | From `updated_at` or partition   |                            |
|                   |           |     | `dtf_end_date`            | DATE               | Validity end date                                   | NULL if current                  |                            |
|                   |           |     | `dtf_current_flag`        | BOOLEAN            | Current record flag                                 | TRUE/FALSE                       |                            |
|                   |           |     | `ds_partition_date`       | STRING             | Partition column (`yyyy-MM-dd`)                     | Job run date                     | Used in `_Hist` only       |

---

### ✅ Business Use Cases

- Enrich financial facts with account metadata (type, branch, status)  
- Support lifecycle-based fraud rules (e.g., activity on closed accounts)  
- Segment customers by account holdings and activity  
- Enable snapshot tracking of account status for historical profiling  