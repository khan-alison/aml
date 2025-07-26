## 📜 Table: Fact_Deposit

This fact table captures daily deposit inflows across customer accounts and deposit products. It supports behavioral analysis, AML structuring detection, and fund source tracking.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factAppend`  
- **Primary Key**: `ds_key`  
- **Partitioned By**: `ds_partition_date`  
- **Snapshot Strategy**: *(Not applicable – not SCD table)*

---

### 📊 Key Columns (Standardize)

| Raw/Fact_Deposit       | Raw Type  | PK (Source) | Standardized/Fact_Deposit   | Standardized Type | Standardized/Fact_Deposit_Hist | Description                                                   | PK  | Value of Technical Field       | Note                            |
|------------------------|-----------|-------------|------------------------------|-------------------|----------------------------------|---------------------------------------------------------------|-----|-------------------------------|---------------------------------|
| `Deposit_ID`           | STRING    | ✅          | `Deposit_ID`                 | STRING            | `Deposit_ID`                     | Unique identifier for deposit event                           |     |                               | Natural key                    |
| `Customer_ID`          | STRING    |             | `Customer_ID`                | STRING            | `Customer_ID`                    | ID of the depositing customer                                 |     |                               | FK to `Dim_Customer`           |
| `Account_ID`           | STRING    |             | `Account_ID`                 | STRING            | `Account_ID`                     | ID of the receiving account                                   |     |                               | FK to `Dim_Account`            |
| `Deposit_Product_Code` | STRING    |             | `Deposit_Product_Code`       | STRING            | `Deposit_Product_Code`           | Deposit product type code                                     |     |                               | FK to `Dim_Deposit`            |
| `Deposit_Channel_Code` | STRING    |             | `Deposit_Channel_Code`       | STRING            | `Deposit_Channel_Code`           | Deposit channel (e.g., online, branch, mobile)                |     |                               | FK to `Dim_Channel`            |
| `Amount`               | DECIMAL   |             | `Deposit_Amount`             | DECIMAL           | `Deposit_Amount`                 | Amount deposited                                              |     |                               |                                 |
| `Currency_Code`        | STRING    |             | `Currency_Code`              | STRING            | `Currency_Code`                  | Currency of the deposit                                       |     |                               | FK to `Dim_Currency`           |
| `Deposit_Date`         | DATE      |             | `Deposit_Date`               | DATE              | `Deposit_Date`                   | Date of deposit transaction                                   |     |                               |                                 |
| `created_at`           | TIMESTAMP |             | `created_at`                 | TIMESTAMP         | `created_at`                     | Timestamp deposit was created in source system                |     | From source                   |                                 |
| `updated_at`           | TIMESTAMP |             | `updated_at`                 | TIMESTAMP         | `updated_at`                     | Last updated time in source                                   |     | From source                   |                                 |
|**Technical Field**|
| `ds_key`               |           |             | `ds_key`                     | STRING            | `ds_key`                         | Surrogate primary key in standardized table                   | ✅  | `md5(Deposit_ID)`            |                                 |
| `cdc_change_type`      |           |             | `cdc_change_type`            | STRING            | `cdc_change_type`                | Type of change: insert/update/delete                          |     | `'cdc_insert'` or `'cdc_update'` | From CDC logic              |
| `cdc_index`            |           |             | `cdc_index`                  | INT               | `cdc_index`                      | 1 = current, 0 = outdated                                     |     | `1`                          | Used for analytics filtering    |
| `scd_change_timestamp` |           |             | `scd_change_timestamp`       | TIMESTAMP         | `scd_change_timestamp`           | Time of change event                                          |     | `updated_at` or job run time |                                 |
| `ds_partition_date`    |           |             |                              | STRING            | `ds_partition_date`              | Partition field                                               |     | Job date (yyyy-MM-dd)        | Required in all fact tables     |

---

### ✅ Business Use Cases

- Detect structuring: frequent deposits just under reporting thresholds  
- Monitor channel misuse (e.g. branch-heavy large deposits)  
- Verify declared income vs. actual inflows  
- Support SAR generation on suspicious large or foreign deposits