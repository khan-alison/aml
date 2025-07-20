## 📜 Table: Fact_KYC_Change_Log

This table logs all field-level changes made to a customer's KYC (Know Your Customer) profile. It is essential for regulatory compliance, audit trails, and understanding the history of identity or profile changes.

- **Type**: Fact  
- **CDC Type**: `1.1` (append-only with no updates or deletes)  
- **Writer Type**: `factAppend`  
- **Primary Key**: *(None)*  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Captures every KYC field change with previous and new values, timestamp, reason, and who initiated the change.

---

### 📊 Key Columns (Standardize)

| Raw/Fact_KYC_Change_Log | Raw Type | Standardized/Fact_KYC_Change_Log | Standardized Type | Description                                            | PK  | Note                          |
|--------------------------|----------|-----------------------------------|--------------------|--------------------------------------------------------|-----|-------------------------------|
| `Customer_ID`            | VARCHAR  | `Customer_ID`                     | VARCHAR            | ID of customer whose KYC field was changed             |     | FK to `Dim_Customer`          |
| `Change_Field`           | VARCHAR  | `Change_Field`                    | VARCHAR            | Name of the field that was modified                    |     |                               |
| `Old_Value`              | TEXT     | `Old_Value`                       | TEXT               | Previous value before the change                       |     |                               |
| `New_Value`              | TEXT     | `New_Value`                       | TEXT               | New value after the change                             |     |                               |
| `Change_Timestamp`       | TIMESTAMP| `Change_Timestamp`                | TIMESTAMP          | When the change occurred                               |     | FK to `Dim_Time`              |
| `Change_Reason`          | VARCHAR  | `Change_Reason`                   | VARCHAR            | Reason for making the change                           |     | Optional                      |
| `Initiated_By`           | VARCHAR  | `Initiated_By`                    | VARCHAR            | Staff or process that initiated the change             |     |                               |
|                          |          | `cdc_change_type`                 | STRING             | Always `'cdc_insert'` – append-only event              |     | CDC 1.1 logic                 |
|                          |          | `cdc_index`                       | INT                | Optional change index                                  |     |                               |
|                          |          | `scd_change_timestamp`           | TIMESTAMP          | Time when the change record was processed              |     |                               |
|                          |          | `ds_partition_date`              | DATE               | Partitioning column (from `Change_Timestamp`)          |     |                               |
|                          |          | `created_at`                     | TIMESTAMP          | Insert time                                            |     |                               |
|                          |          | `updated_at`                     | TIMESTAMP          | Typically null in CDC 1.1                              |     |                               |

---

### ✅ Business Use Cases

- Enables full traceability of customer profile changes  
- Powers compliance reviews and KYC audits  
- Supports regression detection (e.g., high-risk nationality → low-risk change)  
- Ensures no customer changes go undocumented or overwritten