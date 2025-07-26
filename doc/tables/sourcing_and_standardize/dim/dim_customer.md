## 📜 Table: Dim_Customer

This dimension stores KYC (Know Your Customer) profile details used to evaluate customer risk, perform due diligence, and drive AML monitoring. It supports behavioral segmentation, risk scoring, and identity linkage.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `ds_key`  
- **Partitioned By**: `ds_partition_date` (in `_Hist` table only)  
- **Snapshot Strategy**: Full snapshot daily; `_Hist` stores all versions, main table holds current record

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Customer      | Raw Type  | PK (Source) | Standardized/Dim_Customer   | Standardized Type | Standardized/Dim_Customer_Hist | Description                                         | PK  | Value of Technical Field            | Note                            |
|------------------------|-----------|-------------|-------------------------------|-------------------|----------------------------------|-----------------------------------------------------|-----|-------------------------------------|---------------------------------|
| `Customer_ID`          | STRING    | ✅          | `Customer_ID`                | STRING            | `Customer_ID`                    | Unique customer identifier                          |     |                                     | Natural key from source         |
| `Name`                 | STRING    |             | `Customer_Name`              | STRING            | `Customer_Name`                  | Full name of customer                               |     |                                     |                                 |
| `Date_of_birth`        | DATE      |             | `Date_Of_Birth`              | DATE              | `Date_Of_Birth`                  | Birthdate                                           |     |                                     |                                 |
| `Phone`                | STRING    |             | `Phone_Number`               | STRING            | `Phone_Number`                   | Contact number                                      |     |                                     |                                 |
| `Email`                | STRING    |             | `Email_Address`              | STRING            | `Email_Address`                  | Email address                                       |     |                                     |                                 |
| `Segment_Code`         | STRING    |             | `Segment_Code`               | STRING            | `Segment_Code`                   | Customer segmentation code                          |     |                                     | FK to `Dim_Customer_Segment`   |
| `Industry_Code`        | STRING    |             | `Industry_Code`              | STRING            | `Industry_Code`                  | Code of customer’s working industry                |     |                                     | FK to `Dim_Industry`           |
| `Address`              | STRING    |             | `Address`                    | STRING            | `Address`                        | Current address                                     |     |                                     |                                 |
| `Gender`               | STRING    |             | `Gender`                     | STRING            | `Gender`                         | Gender (e.g. MALE/FEMALE/OTHER)                     |     |                                     |                                 |
| `Nationality`          | STRING    |             | `Nationality`                | STRING            | `Nationality`                    | Country of citizenship                              |     |                                     |                                 |
| `ID_Type`              | STRING    |             | `ID_Type`                    | STRING            | `ID_Type`                        | Passport, National ID, etc.                         |     |                                     |                                 |
| `ID_Number`            | STRING    |             | `ID_Number`                  | STRING            | `ID_Number`                      | Official ID number                                  |     |                                     |                                 |
| `ID_Issue_Date`        | DATE      |             | `ID_Issue_Date`              | DATE              | `ID_Issue_Date`                  | Date ID was issued                                  |     |                                     |                                 |
| `ID_Issue`             | STRING    |             | `ID_Issue_Place`             | STRING            | `ID_Issue_Place`                 | Where the ID was issued                             |     |                                     |                                 |
| `Marital_Status`       | STRING    |             | `Marital_Status`             | STRING            | `Marital_Status`                 | Marital state (Single, Married, etc.)              |     |                                     |                                 |
| `Income_Level`         | STRING    |             | `Income_Level`               | STRING            | `Income_Level`                   | Income classification                              |     |                                     |                                 |
| `Branch_Code`          | STRING    |             | `Branch_Code`                | STRING            | `Branch_Code`                    | Customer onboarding branch                         |     |                                     | FK to `Dim_Branch`              |
| `Customer_Open_Date`   | DATE      |             | `Customer_Open_Date`         | DATE              | `Customer_Open_Date`             | Date customer was onboarded                         |     |                                     |                                 |
| `created_at`           | TIMESTAMP |             | `created_at`                 | TIMESTAMP         | `created_at`                     | First seen in source                                |     | From source                         |                                 |
| `updated_at`           | TIMESTAMP |             | `updated_at`                 | TIMESTAMP         | `updated_at`                     | Last update in source                               |     | From source                         |                                 |
| **Technical Fields**   |           |             |                               |                   |                                  |                                                     |     |                                     |                                 |
|                        |           |             | `ds_key`                     | STRING            | `ds_key`                         | Surrogate primary key in standardized table         | ✅  | `Customer_ID`                       | Required in Standardized zone   |
|                        |           |             | `cdc_change_type`            | STRING            | `cdc_change_type`                | CDC event type                                      |     | `'cdc_insert'` or `'cdc_update'`   | From CDC logic                  |
|                        |           |             | `cdc_index`                  | INT               | `cdc_index`                      | 1 = current, 0 = outdated                           |     | `1`                                 | Used for filtering              |
|                        |           |             | `scd_change_timestamp`       | TIMESTAMP         | `scd_change_timestamp`           | Timestamp of version                                |     | `updated_at` or job time           | Required for audit              |
|                        |           |             | `dtf_start_date`             | DATE              | `dtf_start_date`                 | Start of record validity                            |     | `ds_partition_date`                | For SCD tracking                |
|                        |           |             | `dtf_end_date`               | DATE              | `dtf_end_date`                   | End of record validity                              |     | `NULL`                             | NULL means still active         |
|                        |           |             | `dtf_current_flag`           | BOOLEAN           | `dtf_current_flag`               | Is this the current version?                        |     | `TRUE` or `FALSE`                  | Used in main & `_Hist`          |
|                        |           |             |           | STRING            | `ds_partition_date`              | Partition field (used only in `_Hist`)              |     | Job run date (`yyyy-MM-dd`)       | Only appears in `_Hist` table   |

---

### ✅ Business Use Cases

- Power segmentation and profiling based on demographics and ID info  
- Link customers to accounts, transactions, and risk profiles  
- Enable AML checks for PEP, nationality, and high-risk industries  
- Drive customer-level risk scoring and behavioral baselines