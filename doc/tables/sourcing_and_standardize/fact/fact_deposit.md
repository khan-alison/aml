## 📜 Table: Fact_Deposit

This fact table captures daily deposit inflows across customer accounts and deposit products. It supports behavioral analysis, AML structuring detection, and fund source tracking.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factAppend`  
- **Primary Key**: `ds_key`  
- **Partitioned By**: `ds_partition_date`  
- **Snapshot Strategy**: *(Not applicable – fact tables do not have `_Hist`)*

---

### 📊 Key Columns (Standardize)

| Raw/Fact_Deposit       | Raw Type  | PK (Source) | Standardized/Fact_Deposit   | Standardized Type | Description                                                   | PK  | Value of Technical Field       | Note                            |
|------------------------|-----------|-------------|------------------------------|-------------------|---------------------------------------------------------------|-----|-------------------------------|---------------------------------|
| `Deposit_ID`           | STRING    | ✅          | `Deposit_ID`                 | STRING            | Unique identifier for deposit event                           |     |                               | Natural key                    |
| `Customer_ID`          | STRING    |             | `Customer_ID`                | STRING            | ID of the depositing customer                                 |     |                               | FK to `Dim_Customer`           |
| `Account_ID`           | STRING    |             | `Account_ID`                 | STRING            | ID of the receiving account                                   |     |                               | FK to `Dim_Account`            |
| `Deposit_Product_Code` | STRING    |             | `Deposit_Product_Code`       | STRING            | Deposit product type code                                     |     |                               | FK to `Dim_Deposit`            |
| `Deposit_Channel_Code` | STRING    |             | `Deposit_Channel_Code`       | STRING            | Deposit channel (e.g., online, branch, mobile)                |     |                               | FK to `Dim_Channel`            |
| `Amount`               | DECIMAL   |             | `Deposit_Amount`             | DECIMAL           | Amount deposited                                              |     |                               |                                 |
| `Currency_Code`        | STRING    |             | `Currency_Code`              | STRING            | Currency of the deposit                                       |     |                               | FK to `Dim_Currency`           |
| `Deposit_Date`         | DATE      |             | `Deposit_Date`               | DATE              | Date of deposit transaction                                   |     |                               |                                 |
| `created_at`           | TIMESTAMP |             | `created_at`                 | TIMESTAMP         | Timestamp deposit was created in source system                |     | From source                   |                                 |
| `updated_at`           | TIMESTAMP |             | `updated_at`                 | TIMESTAMP         | Last updated time in source                                   |     | From source                   |                                 |
|**Technical Field**|
|                        |           |             | `ds_key`                     | STRING            | Surrogate primary key in standardized table                   | ✅  | `md5(Deposit_ID)`            |                                 |
|                        |           |             | `cdc_change_type`            | STRING            | Type of change: insert/update/delete                          |     | `'cdc_insert'` or `'cdc_update'` | From CDC logic              |
|                        |           |             | `cdc_index`                  | INT               | 1 = current, 0 = outdated                                     |     | `1`                          | Used for analytics filtering    |
|                        |           |             | `scd_change_timestamp`       | TIMESTAMP         | Time of change event                                          |     | `updated_at` or job run time |                                 |
|                        |           |             | `ds_partition_date`          | STRING            | Partition field                                               |     | Job date (yyyy-MM-dd)        | Required in all fact tables     |

---

### ✅ Business Use Cases

- Detect structuring: frequent deposits just under reporting thresholds  
- Monitor channel misuse (e.g. branch-heavy large deposits)  
- Verify declared income vs. actual inflows  
- Support SAR generation on suspicious large or foreign deposits