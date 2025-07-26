## 📜 Table: Fact_Forex_Transaction

This fact table captures all foreign exchange (forex) transactions, including currency pairs, conversion amounts, and applied exchange rates. It supports AML detection scenarios involving currency conversion, cross-border layering, and structuring behavior.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factAppend`  
- **Primary Key**: `ds_key`  
- **Partitioned By**: `ds_partition_date` (string)  
- **Snapshot Strategy**: *(Not applicable – fact tables do not have `_Hist`)*

---

### 📊 Key Columns (Standardize)

| Raw/Fact_Forex_Transaction | Raw Type  | PK (Source) | Standardized/Fact_Forex_Transaction | Standardized Type | Description                                                  | PK  | Value of Technical Field        | Note                            |
|-----------------------------|-----------|-------------|--------------------------------------|--------------------|--------------------------------------------------------------|-----|----------------------------------|---------------------------------|
| `Forex_Transaction_ID`     | STRING    | ✅          | `Forex_Transaction_ID`              | STRING             | Unique ID for the forex transaction                          |     |                                  | Natural key from source         |
| `Customer_ID`              | STRING    |             | `Customer_ID`                       | STRING             | Customer initiating the forex transaction                    |     |                                  | FK to `Dim_Customer`           |
| `Account_ID`               | STRING    |             | `Account_ID`                        | STRING             | Account used for the forex transaction                       |     |                                  | FK to `Dim_Account`            |
| `From_Currency`            | STRING    |             | `From_Currency`                     | STRING             | Currency sold or exchanged from                              |     |                                  | FK to `Dim_Currency`           |
| `To_Currency`              | STRING    |             | `To_Currency`                       | STRING             | Currency bought or exchanged to                              |     |                                  | FK to `Dim_Currency`           |
| `Exchange_Rate`            | DECIMAL   |             | `Exchange_Rate`                     | DECIMAL(18,6)       | Rate applied in the forex conversion                         |     |                                  | May be sourced externally       |
| `Original_Amount`          | DECIMAL   |             | `Original_Amount`                   | DECIMAL(18,2)       | Amount in the original (from) currency                      |     |                                  |                                 |
| `Converted_Amount`         | DECIMAL   |             | `Converted_Amount`                  | DECIMAL(18,2)       | Resulting amount in target (to) currency                    |     |                                  |                                 |
| `Forex_Channel_Code`       | STRING    |             | `Forex_Channel_Code`                | STRING             | Channel of the transaction (e.g., branch, online)           |     |                                  | FK to `Dim_Channel`            |
| `Forex_Date`               | DATE      |             | `Forex_Date`                        | DATE               | Date when forex transaction occurred                        |     |                                  | Transaction effective date     |
| `created_at`               | TIMESTAMP |             | `created_at`                        | TIMESTAMP          | Record creation timestamp from source                       |     | From source                      |                                 |
| `updated_at`               | TIMESTAMP |             | `updated_at`                        | TIMESTAMP          | Last update timestamp from source                           |     | From source                      |                                 |
| **Technical Fields**       |           |             |                                      |                    |                                                              |     |                                  |                                 |
|                             |           |             | `ds_key`                            | STRING             | Surrogate primary key in standardized zone                  | ✅  | `md5(Forex_Transaction_ID)`     | Required for deduplication      |
|                             |           |             | `cdc_change_type`                   | STRING             | CDC event type                                              |     | `'cdc_insert'` / `'cdc_update'` | From CDC engine                 |
|                             |           |             | `cdc_index`                         | INT                | 1 = current, 0 = outdated                                   |     | `1`                             | Required for analytics filter   |
|                             |           |             | `scd_change_timestamp`              | TIMESTAMP          | Change processing timestamp                                 |     | `updated_at` or job timestamp   |                                 |
|                             |           |             | `ds_partition_date`                 | STRING             | Partition column in format `yyyy-MM-dd`                    |     | Job run date                    | Required in all fact tables     |

---

### ✅ Business Use Cases

- Detect excessive or high-value currency conversions  
- Monitor usage of forex for cross-border layering and placement  
- Identify customers frequently transacting in volatile or high-risk currencies  
- Track discrepancies between declared currency needs vs. observed usage  
- Support alerts for forex activity inconsistent with customer profile  