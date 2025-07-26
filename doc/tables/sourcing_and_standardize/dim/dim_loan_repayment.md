## 📜 Table: Dim_Loan_Repayment

This dimension captures **repayment records and schedules** for loans. It enables historical reconstruction of repayment patterns, early payoff detection, and delinquency risk assessment. It supports AML behavior analytics and credit monitoring.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `ds_key`  
- **Partitioned By**: `ds_partition_date` (in `_Hist` table only)  
- **Snapshot Strategy**: Full overwrite per load; `_Hist` retains full version history

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Loan_Repayment | Raw Type  | PK (Source) | Standardized/Dim_Loan_Repayment | Standardized Type | Standardized/Dim_Loan_Repayment_Hist | Description                                    | PK  | Value of Technical Field       | Note                          |
|------------------------|-----------|-------------|----------------------------------|-------------------|----------------------------------------|------------------------------------------------|-----|-------------------------------|-------------------------------|
| `Loan_ID`              | STRING    | ✅          | `Loan_ID`                        | STRING            | `Loan_ID`                              | Identifier of the loan                         |     |                               | FK to `Dim_Loan`             |
| `Repayment_Date`       | DATE      | ✅          | `Repayment_Date`                 | DATE              | `Repayment_Date`                       | Date the repayment was due or made             |     |                               | Granularity of the snapshot  |
| `Repayment_Amount`     | DECIMAL   |             | `Repayment_Amount`               | DECIMAL           | `Repayment_Amount`                     | Total amount repaid on this date               |     |                               |                              |
| `Principal_Amount`     | DECIMAL   |             | `Principal_Amount`               | DECIMAL           | `Principal_Amount`                     | Portion allocated to principal                 |     |                               |                              |
| `Interest_Amount`      | DECIMAL   |             | `Interest_Amount`                | DECIMAL           | `Interest_Amount`                      | Portion allocated to interest                  |     |                               |                              |
| `Currency_Code`        | STRING    |             | `Currency_Code`                  | STRING            | `Currency_Code`                        | Repayment currency                             |     |                               | FK to `Dim_Currency`         |
| `Payment_Channel`      | STRING    |             | `Payment_Channel`                | STRING            | `Payment_Channel`                      | Online, branch, auto-debit, etc.               |     |                               | FK to `Dim_Channel` (if exists) |
| `Repayment_Status`     | STRING    |             | `Repayment_Status`               | STRING            | `Repayment_Status`                     | Status: FULL, PARTIAL, MISSED                  |     |                               |                              |
| `created_at`           | TIMESTAMP |             | `created_at`                     | TIMESTAMP         | `created_at`                           | When this repayment entry was created          |     | From source                   |                              |
| `updated_at`           | TIMESTAMP |             | `updated_at`                     | TIMESTAMP         | `updated_at`                           | Last updated timestamp                         |     | From source                   |                              |
|**Technical Field**|
| `ds_key`               |           |             | `ds_key`                         | STRING            | `ds_key`                               | Surrogate primary key                          | ✅  | `md5(Loan_ID || Repayment_Date)` | Composite of Loan & Date |
| `cdc_change_type`      |           |             | `cdc_change_type`                | STRING            | `cdc_change_type`                      | Insert/update/delete flag                      |     | `'cdc_insert'` or `'cdc_update'` | From CDC logic             |
| `cdc_index`            |           |             | `cdc_index`                      | INT               | `cdc_index`                            | 1 = current, 0 = outdated                      |     | `1`                          | Used for filtering current   |
| `scd_change_timestamp` |           |             | `scd_change_timestamp`           | TIMESTAMP         | `scd_change_timestamp`                 | When this version was recorded                 |     | `updated_at` or job time     |                              |
| `dtf_start_date`       |           |             | `dtf_start_date`                 | DATE              | `dtf_start_date`                       | Effective from                                 |     | `ds_partition_date`          |                              |
| `dtf_end_date`         |           |             | `dtf_end_date`                   | DATE              | `dtf_end_date`                         | Valid until (NULL if current)                  |     | `NULL`                       | SCD4a tracking               |
| `dtf_current_flag`     |           |             | `dtf_current_flag`               | BOOLEAN           | `dtf_current_flag`                     | Is this the current version?                   |     | `TRUE` or `FALSE`            | Used in `_Hist` table        |
| `ds_partition_date`    |           |             |                                  | STRING            | `ds_partition_date`                    | Partition column                               |     | Job run date (yyyy-MM-dd)   | Only in `_Hist`              |

---

### ✅ Business Use Cases

- Detect early loan repayment vs scheduled  
- Flag missed or partial repayments for credit risk scoring  
- Analyze repayment behavior for AML anomalies (e.g. large cash payments)  
- Support regulatory timelines and historical audits of loan performance