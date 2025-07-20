## 📜 Table: Dim_Account

This dimension table defines each customer account in the banking system. It includes status, account type, and lifecycle dates. It supports analytical joins with all transaction, balance, and product fact tables.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd2`  
- **Primary Key**: `Account_ID` (business key) + surrogate key (optional)  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Maintains current and historical view of bank account attributes using SCD2 tracking.

---

### 🔗 Foreign Keys and Relationships:

| Column         | Referenced Table       | Description                              |
|----------------|------------------------|------------------------------------------|
| `Customer_ID`  | `Dim_Customer`         | Owner of the account                     |
| `Branch_ID`    | `Dim_Branch`           | Branch where the account was opened      |

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Account     | Raw Type | Standardized/Std_Account     | Standardized Type | Description                                  | PK  | Note                    |
|---------------------|----------|-------------------------------|-------------------|----------------------------------------------|-----|-------------------------|
| `Account_ID`        | VARCHAR  | `Account_ID`                  | VARCHAR           | Unique account identifier                    | ✅  | Business key            |
| `Customer_ID`       | VARCHAR  | `Customer_ID`                 | VARCHAR           | Customer who owns the account                |     | FK to `Dim_Customer`    |
| `Account_Type`      | VARCHAR  | `Account_Type`                | VARCHAR           | Savings, Current, Term Deposit, etc.         |     |                         |
| `Open_Date`         | DATE     | `Open_Date`                   | DATE              | Account creation date                        |     |                         |
| `Close_Date`        | DATE     | `Close_Date`                  | DATE              | Closure date (if closed)                     |     |                         |
| `Account_Status`    | VARCHAR  | `Account_Status`              | VARCHAR           | Status (e.g., ACTIVE, INACTIVE, CLOSED)      |     |                         |
| `Currency`          | VARCHAR  | `Currency`                    | VARCHAR           | Currency in which account is operated        |     |                         |
| `Branch_ID`         | VARCHAR  | `Branch_ID`                   | VARCHAR           | Branch managing the account                  |     | FK to `Dim_Branch`      |
|Technical Fields (for CDC + audit)|
| *(N/A)*             | *(N/A)*  | `scd_change_type`             | STRING            | `'cdc_insert'`, `'cdc_update'`, `'cdc_delete'` |
| *(N/A)*             | *(N/A)*  | `cdc_index`                   | INT               | Monotonic ingestion index                    |
| *(N/A)*             | *(N/A)*  | `scd_change_timestamp`        | TIMESTAMP         | Time record was processed                    |
| *(N/A)*             | *(N/A)*  | `ds_partition_date`           | DATE              | Partition date                               |
| *(N/A)*             | *(N/A)*  | `created_at`                  | TIMESTAMP         | Time record was created                      |
| *(N/A)*             | *(N/A)*  | `updated_at`                  | TIMESTAMP         | Time of last update                          |
| *(N/A)*             | *(N/A)*  | `dtf_start_date`              | DATE              | SCD2 effective start date                    |
| *(N/A)*             | *(N/A)*  | `dtf_end_date`                | DATE              | SCD2 effective end date                      |
| *(N/A)*             | *(N/A)*  | `dtf_current_flag`            | BOOLEAN           | TRUE if row is active                        |

---

### ✅ Notes:
- SCD2 tracking helps identify account changes over time  
- Supports transaction lineage, account closure trends, and regulatory tracking  
- Access to sensitive information (status, close date) may be restricted  