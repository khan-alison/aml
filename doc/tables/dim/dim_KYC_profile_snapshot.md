## 📜 Table: Dim_KYC_Profile_Snapshot

This dimension stores full daily snapshots of customer KYC profile information to support point-in-time audit, regulatory compliance, and explainability of onboarding and alert decisions. Built with `CDC 1.3` and `SCD4a`, it captures changes to personally identifiable information and KYC fields without overwriting history.

- **Type**: Dimension  
- **CDC Type**: `1.3` (source has `created_at` and `updated_at`)  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Customer_ID`  
- **Partitioned By**: `ds_partition_date` (in history table)  
- **Snapshot Strategy**: Daily overwrite to history; current view in main

---

### 🧩 Main Table Schema (Latest Snapshot Only)

| Column Name         | Type     | Description                                |
|---------------------|----------|--------------------------------------------|
| `Customer_ID`       | VARCHAR  | Unique customer ID                         |
| `Name`              | VARCHAR  | Full name                                  |
| `DOB`               | DATE     | Date of birth                              |
| `Nationality`       | VARCHAR  | Country of citizenship                     |
| `ID_Type`           | VARCHAR  | Type of identification (e.g., Passport)    |
| `ID_Number`         | VARCHAR  | Identification number                      |
| `Address`           | VARCHAR  | Residential address                        |
| `Income_Level`      | DECIMAL  | Declared income                           |
| `Marital_Status`    | VARCHAR  | Marital status                             |
| `Phone`             | VARCHAR  | Contact number                             |
| `Email`             | VARCHAR  | Email address                              |
| `Customer_Open_Date`| DATE     | Date the customer was onboarded            |
| `PEP_Flag`          | BOOLEAN  | Whether the person is a politically exposed person |

#### 🧪 Technical Fields (Main Table):
| Column Name            | Type       | Description                              |
|------------------------|------------|------------------------------------------|
| `scd_change_type`      | STRING     | 'cdc_insert' or 'cdc_update'             |
| `cdc_index`            | INT        | Optional row version index               |
| `scd_change_timestamp` | TIMESTAMP  | Time snapshot was processed              |
| `dtf_start_date`       | DATE       | Start of snapshot validity               |
| `dtf_end_date`         | DATE       | End of snapshot (null = current)         |
| `dtf_current_flag`     | BOOLEAN    | TRUE = current snapshot                  |

---

### 🗃 History Table Schema (Snapshot per Day)

All fields from main table, **plus:**

| Column Name         | Type     | Description                                |
|---------------------|----------|--------------------------------------------|
| `ds_partition_date` | DATE     | Snapshot ingestion date (partition field)  |

---

### ✅ Business Use Cases
- Reconstruct full KYC profile as it existed on any day
- Identify discrepancies or inconsistencies in declared information
- Support compliance audits and onboarding reviews
- Backtest alerts using historical KYC state
