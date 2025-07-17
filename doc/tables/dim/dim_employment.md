## 📜 Table: Dim_Employment

This dimension captures declared or verified employment information of a customer, including employer details, income source, and industry classification. Implemented with `CDC 1.3` and `SCD4a`, it enables full daily snapshots while allowing detection of incremental changes from the source.

- **Type**: Dimension  
- **CDC Type**: `1.3` (source has `created_at` and `updated_at`)  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Employer_ID`  
- **Partitioned By**: `ds_partition_date` (in history table)  
- **Snapshot Strategy**: Daily overwrite to history; current view in main

---

### 🧩 Main Table Schema (Latest Snapshot Only)

| Column Name         | Type     | Description                                |
|---------------------|----------|--------------------------------------------|
| `Employer_ID`       | VARCHAR  | Unique employer/job reference ID           |
| `Customer_ID`       | VARCHAR  | Linked customer                            |
| `Job_Title`         | VARCHAR  | Job title at the company                   |
| `Company_Name`      | VARCHAR  | Employer name                              |
| `Industry`          | VARCHAR  | Sector or industry classification          |
| `Income_Source`     | VARCHAR  | Type of income (e.g., SALARY, FREELANCE)   |
| `Verification_Date` | DATE     | When the employment was last verified      |

#### 🧪 Technical Fields (Main Table):
| Column Name            | Type       | Description                              |
|------------------------|------------|------------------------------------------|
| `scd_change_type`      | STRING     | 'cdc_insert' or 'cdc_update'             |
| `cdc_index`            | INT        | Optional row version index               |
| `scd_change_timestamp` | TIMESTAMP  | Ingestion time of snapshot               |
| `dtf_start_date`       | DATE       | Snapshot start date                      |
| `dtf_end_date`         | DATE       | NULL = current snapshot                  |
| `dtf_current_flag`     | BOOLEAN    | TRUE = currently valid snapshot          |

---

### 🗃 History Table Schema (Snapshot per Day)

Same columns as main, **plus:**

| Column Name         | Type     | Description                                |
|---------------------|----------|--------------------------------------------|
| `ds_partition_date` | DATE     | Partition = snapshot ingestion date        |

---

### ✅ Business Use Cases
- Track when a customer changed employer or industry
- Analyze trends in job title changes, unemployment risk
- Power ML features based on income source stability and employer patterns
- Provide audit trails for EDD/Onboarding review processes
