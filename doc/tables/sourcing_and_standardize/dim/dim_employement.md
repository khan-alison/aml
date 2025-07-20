## 📜 Table: Dim_Employment

This dimension table captures declared or verified employment information linked to each customer. It supports income validation, segmentation, and risk profiling for AML systems.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Employer_ID`  
- **Partitioned By**: `ds_partition_date` (in history table only)  
- **Snapshot Strategy**: Snapshot overwrite into history with active row retained in main table

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Employment | Raw Type | Standardized/std_Employment | Standardized Type | Standardized/std_Employment_Hist | Description                               | PK  | Note                      |
|--------------------|----------|------------------------------|-------------------|-----------------------------------|-------------------------------------------|-----|---------------------------|
| `Employer_ID`      | VARCHAR  | `Employer_ID`               | VARCHAR           | `Employer_ID`                    | Unique employment record ID               | ✅  |                           |
| `Customer_ID`      | VARCHAR  | `Customer_ID`               | VARCHAR           | `Customer_ID`                    | Customer who holds this employment        |     | FK to `Dim_Customer`      |
| `Job_Title`        | VARCHAR  | `Job_Title`                 | VARCHAR           | `Job_Title`                      | Role or designation                       |     |                           |
| `Company_Name`     | VARCHAR  | `Company_Name`              | VARCHAR           | `Company_Name`                   | Employer’s name                           |     |                           |
| `Industry`         | VARCHAR  | `Industry`                  | VARCHAR           | `Industry`                       | Industry classification                   |     |                           |
| `Income_Source`    | VARCHAR  | `Income_Source`             | VARCHAR           | `Income_Source`                  | Salary, Pension, Freelance, etc.          |     | Categorical                |
| `Verification_Date`| DATE     | `Verification_Date`         | DATE              | `Verification_Date`              | When the employment was verified          |     | Used in AML checks         |
| `created_at`       | TIMESTAMP| `created_at`                | TIMESTAMP         | `created_at`                     | Source system creation timestamp          |     | From source (CDC 1.3)      |
| `updated_at`       | TIMESTAMP| `updated_at`                | TIMESTAMP         | `updated_at`                     | Source system last update timestamp       |     | From source (CDC 1.3)      |
| **Technical Fields (for CDC + audit + snapshot logic)** |          |                          |                   |                                   |                                           |     |                           |
|                    |          | `scd_change_type`           | STRING            | `scd_change_type`                | `'cdc_insert'`, `'cdc_update'`            |     | CDC 1.3 logic              |
|                    |          | `cdc_index`                 | INT               | `cdc_index`                      | Row ingestion order                       |     | Optional                  |
|                    |          | `scd_change_timestamp`      | TIMESTAMP         | `scd_change_timestamp`           | When the CDC event was processed          |     |                           |
|                    |          | `dtf_start_date`            | DATE              | `dtf_start_date`                 | Start of snapshot validity                |     |                           |
|                    |          | `dtf_end_date`              | DATE              | `dtf_end_date`                   | End of snapshot validity                  |     | NULL = current            |
|                    |          | `dtf_current_flag`          | BOOLEAN           | `dtf_current_flag`               | TRUE if this is the currently valid version |   |                           |
|                    |          |                             |                   | `ds_partition_date`              | Partition date (history table only)       |     | `_Hist` table only        |