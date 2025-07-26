## 📜 Table: Dim_Employment

This dimension tracks employment history of customers, used in behavioral profiling, creditworthiness assessments, and risk segmentation. It supports slow-changing capture of occupational details over time.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `ds_key`  
- **Main Table**: `Dim_Employment` – stores current job info  
- **History Table**: `Dim_Employment_Hist` – stores full employment history  
- **Partitioned By**: `ds_partition_date` (only in `_Hist` table)  
- **Snapshot Strategy**: SCD4a – latest version in main, traceable audit in `_Hist`

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Employment    | Raw Type  | PK (Source) | Standardized/Dim_Employment | Standardized Type | Standardized/Dim_Employment_Hist | Description                                             | PK  | Value of Technical Field         | Note                            |
|------------------------|-----------|-------------|-------------------------------|--------------------|----------------------------------|---------------------------------------------------------|-----|----------------------------------|---------------------------------|
| `Employment_ID`        | STRING    | ✅          | `Employment_ID`              | STRING             | `Employment_ID`                  | Unique ID of the employment record                      |     |                                  | Primary key from source         |
| `Customer_ID`          | STRING    |             | `Customer_ID`                | STRING             | `Customer_ID`                    | Customer linked to this job                             |     |                                  | FK to `Dim_Customer`           |
| `Company_Name`         | STRING    |             | `Company_Name`               | STRING             | `Company_Name`                   | Employer's name                                         |     |                                  |                                 |
| `Industry_Code`        | STRING    |             | `Industry_Code`              | STRING             | `Industry_Code`                  | Industry of employment                                  |     |                                  | FK to `Dim_Industry`           |
| `Position_Title`       | STRING    |             | `Position_Title`             | STRING             | `Position_Title`                 | Job title or role                                       |     |                                  |                                 |
| `Employment_Type`      | STRING    |             | `Employment_Type`            | STRING             | `Employment_Type`                | Full-Time, Contract, etc.                               |     |                                  |                                 |
| `Start_Date`           | DATE      |             | `Start_Date`                 | DATE               | `Start_Date`                     | Employment start date                                   |     |                                  | Used in history logic          |
| `End_Date`             | DATE      |             | `End_Date`                   | DATE               | `End_Date`                       | Employment end date (nullable)                          |     |                                  |                                 |
| `created_at`           | TIMESTAMP |             | `created_at`                 | TIMESTAMP          | `created_at`                     | First seen in source                                    |     | From source                      |                                 |
| `updated_at`           | TIMESTAMP |             | `updated_at`                 | TIMESTAMP          | `updated_at`                     | Last seen update from source                            |     | From source                      |                                 |
| **Technical Fields**   |           |             |                               |                    |                                  |                                                         |     |                                  |                                 |
|                        |           |             | `ds_key`                     | STRING             | `ds_key`                         | Surrogate primary key in standardized zone              | ✅  | `Employment_ID`                  | Required for scd4a             |
|                        |           |             | `cdc_index`                  | INT                | `cdc_index`                      | Current record flag                                     |     | `1` or `0`                       | 1 = current version             |
|                        |           |             | `cdc_change_type`            | STRING             | `cdc_change_type`                | Type of change detected                                 |     | `'cdc_insert'`, `'cdc_update'`  |                                 |
|                        |           |             | `scd_change_timestamp`       | TIMESTAMP          | `scd_change_timestamp`           | Snapshot creation time                                  |     | `updated_at` or job time         |                                 |
|                        |           |             | `dtf_start_date`             | DATE               | `dtf_start_date`                 | Start of snapshot validity                              |     | From `updated_at` or partition   |                                 |
|                        |           |             | `dtf_end_date`               | DATE               | `dtf_end_date`                   | End of snapshot validity                                |     | NULL if current                  |                                 |
|                        |           |             | `dtf_current_flag`           | BOOLEAN            | `dtf_current_flag`               | TRUE if currently valid                                 |     | TRUE/FALSE                       |                                 |
|                        |           |             |                              |                    | `ds_partition_date`              | Partition column (`yyyy-MM-dd`)                         |     | Job run date                     | **Used in `_Hist` only**        |

---

### ✅ Business Use Cases

- Analyze career stability and income potential  
- Detect abrupt employment changes linked to risk triggers  
- Enhance customer segmentation for credit products  
- Identify employment in high-risk or high-reward sectors  