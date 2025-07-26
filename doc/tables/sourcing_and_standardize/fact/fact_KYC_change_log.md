## 📜 Table: Fact_KYC_Change_Log

This fact table captures all individual field-level changes made to a customer’s KYC profile. It enables reconstruction of historical states, compliance traceability, and auditing of modifications that may indicate manipulation or fraud.

- **Type**: Fact  
- **CDC Type**: `1.1`  
- **Writer Type**: `factAppend`  
- **Primary Key**: `ds_key`  
- **Partitioned By**: `ds_partition_date`  
- **Snapshot Strategy**: *(Not applicable – fact tables do not have `_Hist`)*

---

### 📊 Key Columns (Standardize)

| Raw/Fact_KYC_Change_Log | Raw Type  | PK (Source) | Standardized/Fact_KYC_Change_Log | Standardized Type | Description                                                  | PK  | Value of Technical Field              | Note                            |
|--------------------------|-----------|-------------|-----------------------------------|--------------------|--------------------------------------------------------------|-----|--------------------------------------|---------------------------------|
| `Change_ID`              | STRING    | ✅          | `Change_ID`                       | STRING             | Unique identifier of the KYC change                         |     |                                      | Natural key                     |
| `Customer_ID`            | STRING    |             | `Customer_ID`                     | STRING             | Customer affected by the change                             |     |                                      | FK to `Dim_Customer`           |
| `Changed_Field`          | STRING    |             | `Changed_Field`                   | STRING             | Field that was changed (e.g., Address, Risk_Level)          |     |                                      | ENUM/controlled list           |
| `Old_Value`              | STRING    |             | `Old_Value`                       | STRING             | Value before the change                                     |     |                                      | Nullable                       |
| `New_Value`              | STRING    |             | `New_Value`                       | STRING             | Value after the change                                      |     |                                      |                                 |
| `Changed_By`             | STRING    |             | `Changed_By`                      | STRING             | User or system that triggered the change                    |     |                                      | Optional                        |
| `Change_Timestamp`       | TIMESTAMP |             | `Change_Timestamp`                | TIMESTAMP          | Timestamp of change as recorded in source                   |     | From source                           | Often equals `scd_change_ts`    |
| **Technical Field**      |           |             |                                   |                    |                                                              |     |                                      |                                 |
|                          |           |             | `ds_key`                          | STRING             | Surrogate key for standardized zone                         | ✅  | `md5(Change_ID)`                     | Required                        |
|                          |           |             | `cdc_change_type`                | STRING             | CDC change type (only `cdc_insert` expected)               |     | `'cdc_insert'`                       | CDC 1.1                         |
|                          |           |             | `cdc_index`                      | INT                | CDC index flag                                              |     | `1`                                 | Only current rows in factAppend |
|                          |           |             | `scd_change_timestamp`           | TIMESTAMP          | When change was processed                                   |     | `Change_Timestamp` or job time       |                                 |
|                          |           |             | `ds_partition_date`              | STRING             | Partition column in format `yyyy-MM-dd`                    |     | Job run date                         | Required                        |

---

### ✅ Business Use Cases

- Reconstruct exact KYC state for any point in time  
- Provide audit logs for changes by field, user, and time  
- Flag suspicious field manipulations tied to AML triggers  
- Enable backtesting of rule behavior based on prior KYC data  