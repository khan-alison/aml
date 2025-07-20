## 📜 Table: Dim_Customer

This dimension table captures customer master data for AML and KYC purposes, including identity, contact details, PEP flags, industry, and address information. It is enriched with technical indicators to detect patterns like synthetic identity or fraud rings.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Customer_ID`  
- **Partitioned By**: `ds_partition_date` (in history table only)  
- **Description**: Central customer registry to support transaction mapping, KYC profiling, segmentation, and fraud detection.

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Customer | Raw Type | Standardized/std_Customer | Standardized Type | Standardized/std_Customer_Hist | Description                                             | PK  | Note                         |
|------------------|----------|----------------------------|-------------------|-------------------------------|---------------------------------------------------------|-----|------------------------------|
| `Customer_ID`     | VARCHAR  | `Customer_ID`              | VARCHAR           | `Customer_ID`                | Unique customer identifier                              | ✅  |                              |
| `Name`            | VARCHAR  | `Name`                     | VARCHAR           | `Name`                       | Full name of customer                                   |     |                              |
| `DOB`             | DATE     | `DOB`                      | DATE              | `DOB`                        | Date of birth                                           |     |                              |
| `Nationality`     | VARCHAR  | `Nationality`              | VARCHAR           | `Nationality`                | Country of citizenship                                  |     |                              |
| `Income_Level`    | DECIMAL  | `Income_Level`             | DECIMAL           | `Income_Level`               | Declared income level                                   |     |                              |
| `PEP_Flag`        | BOOLEAN  | `PEP_Flag`                 | BOOLEAN           | `PEP_Flag`                   | Politically exposed person indicator                    |     |                              |
| `Marital_Status`  | VARCHAR  | `Marital_Status`           | VARCHAR           | `Marital_Status`             | Marital status                                          |     |                              |
| `Industry_Code`   | VARCHAR  | `Industry_Code`            | VARCHAR           | `Industry_Code`              | Code for customer's occupation                          |     |                              |
| `ID_Type`         | VARCHAR  | `ID_Type`                  | VARCHAR           | `ID_Type`                    | Type of government ID                                   |     |                              |
| `ID_Number`       | VARCHAR  | `ID_Number`                | VARCHAR           | `ID_Number`                  | ID/passport number                                      |     | Used in AML linkage          |
| `Address`         | VARCHAR  | `Address`                  | VARCHAR           | `Address`                    | Residential address                                     |     | Shared linkage flag          |
| `Phone`           | VARCHAR  | `Phone`                    | VARCHAR           | `Phone`                      | Contact number                                          |     |                              |
| `Email`           | VARCHAR  | `Email`                    | VARCHAR           | `Email`                      | Email address                                           |     |                              |
| `Customer_Open_Date` | DATE | `Customer_Open_Date`       | DATE              | `Customer_Open_Date`         | Date customer joined                                    |     |                              |
| `Branch_ID`       | VARCHAR  | `Branch_ID`                | VARCHAR           | `Branch_ID`                  | Branch where account opened                             |     | FK to `Dim_Branch`           |
| *(Derived)*       | *(N/A)*  | `f_duplicate_id_flag`      | BOOLEAN           | `f_duplicate_id_flag`        | TRUE if same ID shared across multiple customers        |     | AML flag                     |
| *(Derived)*       | *(N/A)*  | `f_shared_address_flag`    | BOOLEAN           | `f_shared_address_flag`      | TRUE if address shared by 3+ customers                  |     | AML flag                     |
| `created_at`      | TIMESTAMP| `created_at`               | TIMESTAMP         | `created_at`                 | Time of initial record creation (from source)           |     | Required for CDC 1.3         |
| `updated_at`      | TIMESTAMP| `updated_at`               | TIMESTAMP         | `updated_at`                 | Time of most recent update (from source)                |     | Required for CDC 1.3         |
|**Technical Fields (for CDC + audit + snapshot logic)**| | | | | | | |
|                  |          | `scd_change_type`           | STRING            | `scd_change_type`            | `'cdc_insert'` or `'cdc_update'`                        |     | CDC 1.3                      |
|                  |          | `cdc_index`                 | INT               | `cdc_index`                  | Monotonic ingestion checkpoint                          |     | Optional                     |
|                  |          | `scd_change_timestamp`      | TIMESTAMP         | `scd_change_timestamp`       | Timestamp of change ingestion                           |     |                              |
|                  |          | `dtf_start_date`            | DATE              | `dtf_start_date`             | Start of snapshot validity                              |     |                              |
|                  |          | `dtf_end_date`              | DATE              | `dtf_end_date`               | End of snapshot validity (NULL = current)               |     |                              |
|                  |          | `dtf_current_flag`          | BOOLEAN           | `dtf_current_flag`           | TRUE if currently active                                |     |                              |
|                  |          |                             |                   | `ds_partition_date`          | Partitioning column (history table only)                |     | `_Hist` table only           |

---

### 🚩 Related AML Scenarios (Standardize → Insight)

| AML Scenario Name                        | Flag at Standardize       | Used in Insight |
|------------------------------------------|----------------------------|------------------|
| Multiple Customers Linked to Same ID     | `f_duplicate_id_flag`      | ✅ Yes           |
| Multiple Customers Sharing Same Address  | `f_shared_address_flag`    | ✅ Yes           |

---

### 🧠 Flag Logic Definitions

| Flag Name                | Type    | Logic                                                             |
|--------------------------|---------|--------------------------------------------------------------------|
| `f_duplicate_id_flag`    | BOOLEAN | TRUE if `ID_Number` appears in ≥ 2 distinct `Customer_ID`s         |
| `f_shared_address_flag`  | BOOLEAN | TRUE if `Address` is shared by ≥ 3 `Customer_ID`s                 |

---

### ✅ Notes

- Used to detect synthetic identities, fake clusters, or money mule networks  
- Source system must contain `created_at` and `updated_at` for CDC 1.3  
- Flags are computed in `Standardize` layer  