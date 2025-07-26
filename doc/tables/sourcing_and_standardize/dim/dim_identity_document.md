## 📜 Table: Dim_Identity_Document

This dimension stores customer identity documentation such as national IDs, passports, or driver’s licenses. It supports identity verification, PEP/sanctions screening, and historical audits.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `ds_key`  
- **Main Table**: `Dim_Identity_Document` – current valid documents  
- **History Table**: `Dim_Identity_Document_Hist` – full change history  
- **Partitioned By**: `ds_partition_date` (in `_Hist` only)  
- **Snapshot Strategy**: SCD4a – latest version in main, audit trail in `_Hist`

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Identity_Document | Raw Type  | PK (Source) | Standardized/Dim_Identity_Document | Standardized Type | Standardized/Dim_Identity_Document_Hist | Description                                              | PK  | Value of Technical Field         | Note                          |
|---------------------------|-----------|-------------|-------------------------------------|--------------------|------------------------------------------|----------------------------------------------------------|-----|----------------------------------|-------------------------------|
| `Document_ID`             | STRING    | ✅          | `Document_ID`                       | STRING             | `Document_ID`                            | Unique identifier for the identity document             |     |                                  | Primary key from source       |
| `Customer_ID`             | STRING    |             | `Customer_ID`                       | STRING             | `Customer_ID`                            | Customer who owns the document                          |     |                                  | FK to `Dim_Customer`         |
| `Document_Type`           | STRING    |             | `Document_Type`                     | STRING             | `Document_Type`                          | Passport, National ID, Driver’s License, etc.           |     |                                  | Classification                |
| `Document_Number`         | STRING    |             | `Document_Number`                   | STRING             | `Document_Number`                        | Official number on the document                         |     |                                  | Personally identifiable       |
| `Issue_Date`              | DATE      |             | `Issue_Date`                        | DATE               | `Issue_Date`                             | Date when document was issued                           |     |                                  | Used in document validity     |
| `Expiry_Date`             | DATE      |             | `Expiry_Date`                       | DATE               | `Expiry_Date`                            | Document expiration date                                |     |                                  | Nullable                      |
| `Issued_By`               | STRING    |             | `Issued_By`                         | STRING             | `Issued_By`                              | Authority or location issuing the document              |     |                                  | Can be country or agency      |
| `created_at`              | TIMESTAMP |             | `created_at`                        | TIMESTAMP          | `created_at`                             | Timestamp from source creation                          |     | From source                      |                               |
| `updated_at`              | TIMESTAMP |             | `updated_at`                        | TIMESTAMP          | `updated_at`                             | Last update from source                                 |     | From source                      |                               |
| **Technical Fields**      |           |             |                                     |                    |                                          |                                                          |     |                                  |                               |
|                           |           |             | `ds_key`                            | STRING             | `ds_key`                                 | Surrogate primary key for standardized zone             | ✅  | `Document_ID`                    | Required for all SCD4a tables |
|                           |           |             | `cdc_index`                         | INT                | `cdc_index`                              | 1 = current, 0 = outdated                               |     | `1` or `0`                       | Used to filter current rows   |
|                           |           |             | `cdc_change_type`                   | STRING             | `cdc_change_type`                        | Type of change                                          |     | `'cdc_insert'`, `'cdc_update'`  | From CDC event logic          |
|                           |           |             | `scd_change_timestamp`              | TIMESTAMP          | `scd_change_timestamp`                   | Timestamp of change application                         |     | `updated_at` or job time         |                               |
|                           |           |             | `dtf_start_date`                    | DATE               | `dtf_start_date`                         | Validity start                                          |     | From `updated_at` or partition   |                               |
|                           |           |             | `dtf_end_date`                      | DATE               | `dtf_end_date`                           | Validity end                                            |     | NULL if current                  |                               |
|                           |           |             | `dtf_current_flag`                  | BOOLEAN            | `dtf_current_flag`                       | Indicates if record is current                          |     | TRUE/FALSE                       | Used in snapshot joins        |
|                           |           |             |                                     |                    | `ds_partition_date`                      | Partition column in `yyyy-MM-dd` format                |     | Job run date                     | **Used in `_Hist` only**      |

---

### ✅ Business Use Cases

- Screen for expired or duplicate identity documents  
- Link customers with multiple verified ID types  
- Trace document changes across time for audit purposes  
- Trigger alerts for invalid or soon-to-expire documents  