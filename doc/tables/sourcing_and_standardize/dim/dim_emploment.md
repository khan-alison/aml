## 📜 Table: Dim_Employment

This dimension tracks employment history of customers, used in behavioral profiling, creditworthiness assessments, and risk segmentation. It supports slow-changing capture of occupational details over time.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Employment_ID` (from source)  
- **Partitioned By**: `ds_partition_date` (string, in `_Hist` table only)  
- **Snapshot Strategy**: SCD4a – latest record in main table, full history in `_Hist`

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Employment    | Raw Type  | PK  | Standardized/Dim_Employment | Standardized Type | Description                                             | Value of Technical Field         | Note                            |
|------------------------|-----------|-----|-------------------------------|--------------------|---------------------------------------------------------|----------------------------------|---------------------------------|
| `Employment_ID`        | STRING    | ✅  | `Employment_ID`              | STRING             | Unique ID of the employment record                      |                                  | Primary key from source         |
| `Customer_ID`          | STRING    |     | `Customer_ID`                | STRING             | Customer linked to this job                             |                                  | FK to `Dim_Customer`           |
| `Company_Name`         | STRING    |     | `Company_Name`               | STRING             | Employer's name                                         |                                  |                                 |
| `Industry_Code`        | STRING    |     | `Industry_Code`              | STRING             | Industry of employment                                  |                                  | FK to `Dim_Industry`           |
| `Position_Title`       | STRING    |     | `Position_Title`             | STRING             | Job title or role                                       |                                  |                                 |
| `Employment_Type`      | STRING    |     | `Employment_Type`            | STRING             | Full-Time, Contract, etc.                               |                                  |                                 |
| `Start_Date`           | DATE      |     | `Start_Date`                 | DATE               | Employment start date                                   |                                  | Used in history logic          |
| `End_Date`             | DATE      |     | `End_Date`                   | DATE               | Employment end date (nullable)                          |                                  |                                 |
| `created_at`           | TIMESTAMP |     | `created_at`                 | TIMESTAMP          | First seen in source                                    | From source                      |                                 |
| `updated_at`           | TIMESTAMP |     | `updated_at`                 | TIMESTAMP          | Last seen update from source                            | From source                      |                                 |
| **Technical Fields**   |           |     |                               |                    |                                                         |                                  |                                 |
|                        |           |     | `ds_key`                     | STRING             | Surrogate primary key in standardized zone              | `Employment_ID`                  | Required for all scd4a tables   |
|                        |           |     | `cdc_index`                  | INT                | Current record flag                                     | `1` or `0`                       | 1 = current version             |
|                        |           |     | `cdc_change_type`            | STRING             | Type of change detected                                 | `'cdc_insert'`, `'cdc_update'`  |                                 |
|                        |           |     | `scd_change_timestamp`       | TIMESTAMP          | Snapshot creation time                                  | `updated_at` or job time         |                                 |
|                        |           |     | `dtf_start_date`             | DATE               | Start of snapshot validity                              | From `updated_at` or partition   |                                 |
|                        |           |     | `dtf_end_date`               | DATE               | End of snapshot validity                                | NULL if current                  |                                 |
|                        |           |     | `dtf_current_flag`           | BOOLEAN            | TRUE if currently valid                                 | TRUE/FALSE                       |                                 |
|                        |           |     | `ds_partition_date`          | STRING             | Partition column in format `yyyy-MM-dd`                 | Job run date                     | Only used in `_Hist`            |

---

### ✅ Business Use Cases

- Analyze career stability and income potential  
- Detect abrupt employment changes linked to risk triggers  
- Enhance customer segmentation for credit products  
- Identify employment in high-risk or high-reward sectors  