## 📜 Table: Dim_Identity_Document

This dimension stores customer identity documentation such as national IDs, passports, or driver’s licenses. It supports identity verification, PEP/sanctions screening, and historical audits.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Document_ID` (from source)  
- **Partitioned By**: `ds_partition_date` (string, in `_Hist` table only)  
- **Snapshot Strategy**: SCD4a – current version in main table, full history in `_Hist`

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Identity_Document | Raw Type  | PK  | Standardized/Dim_Identity_Document | Standardized Type | Description                                              | Value of Technical Field         | Note                          |
|---------------------------|-----------|-----|-------------------------------------|--------------------|----------------------------------------------------------|----------------------------------|-------------------------------|
| `Document_ID`             | STRING    | ✅  | `Document_ID`                       | STRING             | Unique identifier for the identity document             |                                  | Primary key from source       |
| `Customer_ID`             | STRING    |     | `Customer_ID`                       | STRING             | Customer who owns the document                          |                                  | FK to `Dim_Customer`         |
| `Document_Type`           | STRING    |     | `Document_Type`                     | STRING             | Passport, National ID, Driver’s License, etc.           |                                  | Classification                |
| `Document_Number`         | STRING    |     | `Document_Number`                   | STRING             | Official number on the document                         |                                  | Personally identifiable       |
| `Issue_Date`              | DATE      |     | `Issue_Date`                        | DATE               | Date when document was issued                           |                                  | Used in document validity     |
| `Expiry_Date`             | DATE      |     | `Expiry_Date`                       | DATE               | Document expiration date                                |                                  | Nullable                      |
| `Issued_By`               | STRING    |     | `Issued_By`                         | STRING             | Authority or location issuing the document              |                                  | Can be country or agency      |
| `created_at`              | TIMESTAMP |     | `created_at`                        | TIMESTAMP          | Timestamp from source creation                          | From source                      |                               |
| `updated_at`              | TIMESTAMP |     | `updated_at`                        | TIMESTAMP          | Last update from source                                 | From source                      |                               |
| **Technical Fields**      |           |     |                                     |                    |                                                          |                                  |                               |
|                           |           |     | `ds_key`                            | STRING             | Surrogate primary key for standardized zone             | `Document_ID`                    | Required for all SCD4a tables |
|                           |           |     | `cdc_index`                         | INT                | 1 = current, 0 = outdated                               | `1` or `0`                       | Used to filter current rows   |
|                           |           |     | `cdc_change_type`                   | STRING             | Type of change                                          | `'cdc_insert'` or `'cdc_update'`| From CDC event logic          |
|                           |           |     | `scd_change_timestamp`              | TIMESTAMP          | Timestamp of change application                         | `updated_at` or job time         |                               |
|                           |           |     | `dtf_start_date`                    | DATE               | Validity start                                          | From `updated_at` or partition   |                               |
|                           |           |     | `dtf_end_date`                      | DATE               | Validity end                                            | NULL if current                  |                               |
|                           |           |     | `dtf_current_flag`                  | BOOLEAN            | Indicates if record is current                          | TRUE/FALSE                       | Used in snapshot joins        |
|                           |           |     | `ds_partition_date`                 | STRING             | Partition column in `yyyy-MM-dd` format                | Job run date                     | Used in `_Hist` table only    |

---

### ✅ Business Use Cases

- Screen for expired or duplicate identity documents  
- Link customers with multiple verified ID types  
- Trace document changes across time for audit purposes  
- Trigger alerts for invalid or soon-to-expire documents  