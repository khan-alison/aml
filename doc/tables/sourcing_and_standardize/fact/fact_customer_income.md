## 📜 Table: Fact_Customer_Income

This fact table records **verified inflows** such as salary, dividends, or other income sources credited to a customer. It supports financial capability analysis, income-debt comparison, and behavioral anomaly detection in AML systems.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factAppend`  
- **Primary Key**: `ds_key`  
- **Partitioned By**: `ds_partition_date`  
- **Snapshot Strategy**: *(Not applicable – not SCD)*

---

### 📊 Key Columns (Standardize)

| Raw/Fact_Customer_Income | Raw Type  | PK (Source) | Standardized/Fact_Customer_Income | Standardized Type | Standardized/Fact_Customer_Income_Hist | Description                                      | PK  | Value of Technical Field       | Note                          |
|--------------------------|-----------|-------------|-----------------------------------|-------------------|-----------------------------------------|--------------------------------------------------|-----|-------------------------------|-------------------------------|
| `Income_ID`              | STRING    | ✅          | `Income_ID`                       | STRING            | `Income_ID`                             | Unique identifier of the income inflow           |     |                               | Natural key                  |
| `Customer_ID`            | STRING    |             | `Customer_ID`                     | STRING            | `Customer_ID`                           | ID of the receiving customer                     |     |                               | FK to `Dim_Customer`         |
| `Income_Date`            | DATE      |             | `Income_Date`                     | DATE              | `Income_Date`                           | Date of income inflow                            |     |                               | FK to `Dim_Time` (optional)  |
| `Income_Type_Code`       | STRING    |             | `Income_Type_Code`                | STRING            | `Income_Type_Code`                      | Salary, dividend, etc.                           |     |                               | FK to `Dim_Income_Type`      |
| `Amount`                 | DECIMAL   |             | `Income_Amount`                   | DECIMAL           | `Income_Amount`                         | Amount received                                  |     |                               |                               |
| `Currency_Code`          | STRING    |             | `Currency_Code`                   | STRING            | `Currency_Code`                         | Currency in which income was received            |     |                               | FK to `Dim_Currency`         |
| `Payment_Channel`        | STRING    |             | `Payment_Channel`                 | STRING            | `Payment_Channel`                       | Transfer, cash, salary portal, etc.              |     |                               | FK to `Dim_Channel` (optional) |
| `Description`            | STRING    |             | `Description`                     | STRING            | `Description`                           | Free-text field with additional info             |     |                               | Optional metadata            |
| `created_at`             | TIMESTAMP |             | `created_at`                      | TIMESTAMP         | `created_at`                            | When this income was created in the source       |     | From source                   |                               |
| `updated_at`             | TIMESTAMP |             | `updated_at`                      | TIMESTAMP         | `updated_at`                            | When last updated in source                      |     | From source                   |                               |
|**Technical Field**|
| `ds_key`                 |           |             | `ds_key`                          | STRING            | `ds_key`                                | Surrogate key for income record                  | ✅  | `md5(Income_ID)`             |                               |
| `cdc_change_type`        |           |             | `cdc_change_type`                 | STRING            | `cdc_change_type`                       | Insert/update/delete indicator                   |     | `'cdc_insert'` or `'cdc_update'` | From CDC logic             |
| `cdc_index`              |           |             | `cdc_index`                       | INT               | `cdc_index`                             | 1 = current, 0 = outdated                         |     | `1`                          | Used for filtering            |
| `scd_change_timestamp`   |           |             | `scd_change_timestamp`            | TIMESTAMP         | `scd_change_timestamp`                  | Time of this version or ingestion                |     | `updated_at` or job time     |                               |
| `ds_partition_date`      |           |             |                                   | STRING            | `ds_partition_date`                     | Partition column for fact ingestion              |     | Job date (yyyy-MM-dd)        | Required for all fact tables  |

---

### ✅ Business Use Cases

- Compare income against loan repayments or withdrawals  
- Detect sudden, unexplained increases in income inflows  
- Feed into customer risk scores and financial behavior baselines  
- Identify discrepancies between declared income and real inflows