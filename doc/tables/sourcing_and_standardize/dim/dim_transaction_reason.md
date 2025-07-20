## 📜 Table: Dim_Employment

This dimension stores employment information associated with each customer, including employer, industry, and income verification metadata. It is essential for income estimation, risk profiling, and enhanced due diligence (EDD).

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd2`  
- **Primary Key**: `Employer_ID`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Captures customer employment data over time, supporting income modeling and customer segmentation.

---

### 🔗 Foreign Keys and Relationships:

| Column         | Referenced Table       | Description |
|----------------|------------------------|-------------|
| `Customer_ID`  | `Dim_Customer`         | The individual with this employment record  |

---

### 📊 Key Columns:

| Raw Column Name     | Raw Type | Standardized Column Name | Standardized Type | Description                                   | PK  | Note               |
|----------------------|----------|---------------------------|--------------------|-----------------------------------------------|-----|--------------------|
| `Employer_ID`        | VARCHAR  | `Employer_ID`             | VARCHAR            | Unique ID for the employment record           | ✅  | Primary key        |
| `Customer_ID`        | VARCHAR  | `Customer_ID`             | VARCHAR            | FK to customer being employed                 |     | FK to `Dim_Customer` |
| `Job_Title`          | VARCHAR  | `Job_Title`               | VARCHAR            | Customer’s role or position                   |     |                     |
| `Company_Name`       | VARCHAR  | `Company_Name`            | VARCHAR            | Employer organization name                    |     |                     |
| `Industry`           | VARCHAR  | `Industry`                | VARCHAR            | Sector or economic domain of the company      |     | Standardized value   |
| `Income_Source`      | VARCHAR  | `Income_Source`           | VARCHAR            | Declared income stream (e.g., salary, bonus)  |     |                     |
| `Verification_Date`  | DATE     | `Verification_Date`       | DATE               | When this information was verified            |     | Can align with KYC audit |

---

### 🧪 Technical Fields (for SCD2 tracking):

| Field Name            | Type       | Description                                   |
|------------------------|------------|-----------------------------------------------|
| `scd_change_type`      | STRING     | `'cdc_insert'`, `'cdc_update'`, `'cdc_delete'`|
| `cdc_index`            | INT        | Change tracking index                         |
| `scd_change_timestamp` | TIMESTAMP  | Timestamp of record load/update               |
| `ds_partition_date`    | DATE       | Partition field                               |
| `created_at`           | TIMESTAMP  | When record was created                       |
| `updated_at`           | TIMESTAMP  | When record was last updated                  |
| `dtf_start_date`       | DATE       | Valid-from date (SCD2)                        |
| `dtf_end_date`         | DATE       | Valid-until date                              |
| `dtf_current_flag`     | BOOLEAN    | TRUE if currently active record               |

---

### ✅ Notes:
- Joins with `Dim_Customer`, `Fact_Customer_Income`, and onboarding KYC
- Can be used in rules like: “Unverified employment with high-risk income type”
- Helps enrich income estimation models for segmenting salaried vs non-salaried

