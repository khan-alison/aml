## 📜 Table: Dim_KYC_Profile_Snapshot

This dimension stores full daily snapshots of customer KYC profile information to support point-in-time audit, regulatory compliance, and explainability of onboarding and alert decisions. Built with `CDC 1.3` and `SCD4a`, it captures changes to personally identifiable information and KYC fields without overwriting history.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Customer_ID`  
- **Partitioned By**: `ds_partition_date` (in history table)  
- **Snapshot Strategy**: Daily overwrite to history; current view in main

---

### 📊 Key Columns (Standardize)

| Raw/Dim_KYC_Profile_Snapshot | Raw Type | Standardized/std_KYC_Profile_Snapshot | Standardized Type | Standardized/std_KYC_Profile_Snapshot_Hist | Description                                   | PK  | Note                        |
|------------------------------|----------|----------------------------------------|-------------------|---------------------------------------------|-----------------------------------------------|-----|-----------------------------|
| `Customer_ID`               | VARCHAR  | `Customer_ID`                          | VARCHAR           | `Customer_ID`                               | Unique customer ID                            | ✅  |                             |
| `Name`                      | VARCHAR  | `Name`                                 | VARCHAR           | `Name`                                      | Full name                                     |     | PII                         |
| `DOB`                       | DATE     | `DOB`                                  | DATE              | `DOB`                                       | Date of birth                                 |     |                             |
| `Nationality`               | VARCHAR  | `Nationality`                          | VARCHAR           | `Nationality`                               | Country of citizenship                        |     |                             |
| `ID_Type`                   | VARCHAR  | `ID_Type`                              | VARCHAR           | `ID_Type`                                   | Type of identification (e.g., Passport)       |     |                             |
| `ID_Number`                 | VARCHAR  | `ID_Number`                            | VARCHAR           | `ID_Number`                                 | Identification number                         |     | PII                         |
| `Address`                   | VARCHAR  | `Address`                              | VARCHAR           | `Address`                                   | Residential address                           |     | PII                         |
| `Income_Level`              | DECIMAL  | `Income_Level`                         | DECIMAL           | `Income_Level`                              | Declared income                               |     |                             |
| `Marital_Status`            | VARCHAR  | `Marital_Status`                       | VARCHAR           | `Marital_Status`                            | Marital status                                |     |                             |
| `Phone`                     | VARCHAR  | `Phone`                                | VARCHAR           | `Phone`                                     | Contact number                                |     |                             |
| `Email`                     | VARCHAR  | `Email`                                | VARCHAR           | `Email`                                     | Email address                                 |     |                             |
| `Customer_Open_Date`        | DATE     | `Customer_Open_Date`                   | DATE              | `Customer_Open_Date`                        | Date the customer was onboarded               |     |                             |
| `PEP_Flag`                  | BOOLEAN  | `PEP_Flag`                             | BOOLEAN           | `PEP_Flag`                                  | Politically Exposed Person flag               |     | Regulatory watch            |
|Technical Fields (for CDC + audit + snapshot logic)|
|                              |          | `scd_change_type`                      | STRING            | `scd_change_type`                           | `'cdc_insert'` or `'cdc_update'`              |     | CDC 1.3 logic                |
|                              |          | `cdc_index`                            | INT               | `cdc_index`                                 | Change index (optional)                       |     |                             |
|                              |          | `scd_change_timestamp`                 | TIMESTAMP         | `scd_change_timestamp`                      | Ingestion timestamp                           |     |                             |
|                              |          | `dtf_start_date`                       | DATE              | `dtf_start_date`                            | Snapshot validity start date                  |     |                             |
|                              |          | `dtf_end_date`                         | DATE              | `dtf_end_date`                              | Snapshot end date (NULL = current)            |     |                             |
|                              |          | `dtf_current_flag`                     | BOOLEAN           | `dtf_current_flag`                          | TRUE = currently active snapshot              |     |                             |
|                              |          |                                         |                  | `ds_partition_date`                         | Partition column in `_hist` table only        |     |                             |

---

### ✅ Business Use Cases

- Reconstruct full KYC profile as it existed on any day  
- Identify discrepancies or inconsistencies in declared information  
- Support compliance audits and onboarding reviews  
- Backtest alerts using historical KYC state