## 📜 Table: Dim_Customer

This dimension stores KYC (Know Your Customer) profile details used to evaluate customer risk, perform due diligence, and drive AML monitoring. It supports behavioral segmentation, risk scoring, and identity linkage.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Customer_ID` (from source)  
- **Partitioned By**: `ds_partition_date` (in `_Hist` table only)  
- **Snapshot Strategy**: Full snapshot daily; `_Hist` stores all versions, main table holds current record.

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Customer      | Raw Type  | PK  | Standardized/Dim_Customer   | Standardized Type | Description                                         | Value of Technical Field            | Note                            |
|------------------------|-----------|-----|-------------------------------|-------------------|-----------------------------------------------------|-------------------------------------|---------------------------------|
| `Customer_ID`          | VARCHAR   | ✅  | `Customer_ID`                | VARCHAR           | Unique customer identifier                          |                                     | Natural key from source         |
| `Name`                 | STRING    |     | `Customer_Name`              | STRING            | Full name of customer                               |                                     |                                 |
| `Date_of_birth`        | DATE      |     | `Date_Of_Birth`              | DATE              | Birthdate                                           |                                     |                                 |
| `Phone`                | STRING    |     | `Phone_Number`               | STRING            | Contact number                                      |                                     |                                 |
| `Email`                | STRING    |     | `Email_Address`              | STRING            | Email address                                       |                                     |                                 |
| `Segment_Code`         | STRING    |     | `Segment_Code`               | STRING            | Customer segmentation code                          |                                     | FK to `Dim_Customer_Segment`   |
| `Industry_Code`        | STRING    |     | `Industry_Code`              | STRING            | Code of customer’s working industry                |                                     | FK to `Dim_Industry`           |
| `Address`              | STRING    |     | `Address`                    | STRING            | Current address                                     |                                     |                                 |
| `Gender`               | STRING    |     | `Gender`                     | STRING            | Gender (e.g. MALE/FEMALE/OTHER)                     |                                     |                                 |
| `Nationality`          | STRING    |     | `Nationality`                | STRING            | Country of citizenship                              |                                     |                                 |
| `ID_Type`              | STRING    |     | `ID_Type`                    | STRING            | Passport, National ID, etc.                         |                                     |                                 |
| `ID_Number`            | STRING    |     | `ID_Number`                  | STRING            | Official ID number                                  |                                     |                                 |
| `ID_Issue_Date`        | DATE      |     | `ID_Issue_Date`              | DATE              | Date ID was issued                                  |                                     |                                 |
| `ID_Issue`             | STRING    |     | `ID_Issue_Place`             | STRING            | Where the ID was issued                             |                                     |                                 |
| `Marital_Status`       | STRING    |     | `Marital_Status`             | STRING            | Marital state (Single, Married, etc.)              |                                     |                                 |
| `Income_Level`         | STRING    |     | `Income_Level`               | STRING            | Income classification                              |                                     |                                 |
| `Branch_Code`          | STRING    |     | `Branch_Code`                | STRING            | Customer onboarding branch                         |                                     | FK to `Dim_Branch`              |
| `Customer_Open_Date`   | DATE      |     | `Customer_Open_Date`         | DATE              | Date customer was onboarded                         |                                     |                                 |
| `created_at`           | TIMESTAMP |     | `created_at`                 | TIMESTAMP         | First seen in source                                | From source                         |                                 |
| `updated_at`           | TIMESTAMP |     | `updated_at`                 | TIMESTAMP         | Last seen update in source                          | From source                         |                                 |
| **Technical Fields**   |           |     |                               |                   |                                                     |                                     |                                 |
|                        |           |     | `ds_key`                     | STRING            | Surrogate primary key in standardized zone          | `Customer_ID`                       | Required in Standardized zone   |
|                        |           |     | `cdc_change_type`            | STRING            | Type of change from CDC event                       | `'cdc_insert'` or `'cdc_update'`   | From CDC logic                  |
|                        |           |     | `cdc_index`                  | INT               | 1 = current, 0 = outdated                           | `1`                                 | Used for filtering              |
|                        |           |     | `scd_change_timestamp`       | TIMESTAMP         | Snapshot timestamp                                  | `updated_at` or job run time        | Used in audit trail             |
|                        |           |     | `dtf_start_date`             | DATE              | Start of snapshot validity                          | `cast(ds_partition_date as date)`  | From partition logic            |
|                        |           |     | `dtf_end_date`               | DATE              | End of snapshot validity (nullable)                 | `NULL`                              | NULL means still active         |
|                        |           |     | `dtf_current_flag`           | BOOLEAN           | Indicates current version                           | TRUE/FALSE                          | Based on CDC merge              |
|                        |           |     | `ds_partition_date`          | STRING            | Partition column in format yyyy-MM-dd               | Job run date                        | Only used in `_Hist`            |

---

### ✅ Business Use Cases

- Power segmentation and profiling based on demographics and ID info  
- Link customers to accounts, transactions, and risk profiles  
- Enable AML checks for PEP, nationality, and high-risk industries  
- Drive customer-level risk scoring and behavioral baselines  