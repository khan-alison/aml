## 📜 Table: Dim_Customer

This dimension table stores detailed KYC and demographic attributes of each customer. It acts as a central reference in AML systems, linking to transaction, loan, and alert facts. Changes are tracked using Slowly Changing Dimension Type 2 (SCD2).

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd2`  
- **Primary Key**: `Customer_ID` (business key) + surrogate key (e.g., `Dim_Customer_ID`)  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Holds the latest and historical customer profile attributes with SCD2 tracking logic.

---

### 🔗 Foreign Keys and Relationships:

| Column         | Referenced Table       | Description |
|----------------|------------------------|-------------|
| `Branch_ID`    | `Dim_Branch`           | Home branch of the customer  |

---

### 📊 Key Columns:

| Raw Column Name         | Raw Type | Standardized Column Name | Standardized Type | Description                               | PK  | Note                    |
|--------------------------|----------|---------------------------|--------------------|-------------------------------------------|-----|-------------------------|
| `Customer_ID`            | VARCHAR  | `Customer_ID`             | VARCHAR            | Unique customer identifier                | ✅  | Business key            |
| `Name`                   | VARCHAR  | `Name`                    | VARCHAR            | Full name of the customer                 |     |                         |
| `DOB`                    | DATE     | `DOB`                     | DATE               | Date of birth                            |     |                         |
| `Nationality`            | VARCHAR  | `Nationality`             | VARCHAR            | Country of citizenship                   |     |                         |
| `Income_Level`           | DECIMAL  | `Income_Level`            | DECIMAL            | Declared or inferred income level        |     |                         |
| `PEP_Flag`               | BOOLEAN  | `PEP_Flag`                | BOOLEAN            | Politically exposed person indicator     |     |                         |
| `Marital_Status`         | VARCHAR  | `Marital_Status`          | VARCHAR            | Single, Married, Divorced, etc.          |     |                         |
| `Industry_Code`          | VARCHAR  | `Industry_Code`           | VARCHAR            | Customer's industry sector               |     |                         |
| `ID_Type`                | VARCHAR  | `ID_Type`                 | VARCHAR            | Type of ID (e.g., Passport, ID Card)     |     |                         |
| `ID_Number`              | VARCHAR  | `ID_Number`               | VARCHAR            | Official ID number                       |     | Sensitive (PII)         |
| `Address`                | VARCHAR  | `Address`                 | VARCHAR            | Registered residential address           |     | PII                    |
| `Phone`                  | VARCHAR  | `Phone`                   | VARCHAR            | Phone number                             |     | PII                    |
| `Email`                  | VARCHAR  | `Email`                   | VARCHAR            | Email address                            |     | PII                    |
| `Customer_Open_Date`     | DATE     | `Customer_Open_Date`      | DATE               | Date customer was onboarded              |     |                         |
| `Branch_ID`              | VARCHAR  | `Branch_ID`               | VARCHAR            | Branch managing the relationship         |     | FK to `Dim_Branch`      |

---

### 🧪 Technical Fields (for SCD2 tracking):

| Field Name            | Type       | Description                                   |
|------------------------|------------|-----------------------------------------------|
| `scd_change_type`      | STRING     | `'cdc_insert'`, `'cdc_update'`, `'cdc_delete'`|
| `cdc_index`            | INT        | Sequence index for ordering changes           |
| `scd_change_timestamp` | TIMESTAMP  | Time of SCD2 record capture                  |
| `ds_partition_date`    | DATE       | Partition column                             |
| `created_at`           | TIMESTAMP  | Record creation time                         |
| `updated_at`           | TIMESTAMP  | Last update time (if any)                    |
| `dtf_start_date`       | DATE       | SCD2 start date                              |
| `dtf_end_date`         | DATE       | SCD2 end date                                |
| `dtf_current_flag`     | BOOLEAN    | TRUE if row is currently active              |

---

### ✅ Notes:
- Implements SCD2 for full change history tracking
- Contains PII fields — ensure proper masking and role-based access
- Used by AML analysts, KYC compliance, and customer segmentation
```
