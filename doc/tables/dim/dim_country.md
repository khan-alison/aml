## 📜 Table: Dim_Country

This dimension table stores reference data for countries, including names, codes, and compliance-related attributes such as risk level and sanction status. It is used in AML systems to evaluate jurisdictional risk, support transaction screening, and generate reports.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd2`  
- **Primary Key**: `Country_Code`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Contains country-level metadata, enabling risk scoring, jurisdictional filtering, and regulatory screening logic.

---

### 📊 Key Columns:

| Raw Column Name     | Raw Type | Standardized Column Name | Standardized Type | Description                                 | PK  | Note               |
|----------------------|----------|---------------------------|--------------------|---------------------------------------------|-----|--------------------|
| `Country_Code`       | VARCHAR  | `Country_Code`            | VARCHAR            | ISO country code or internal equivalent     | ✅  | Primary key        |
| `Country_Name`       | VARCHAR  | `Country_Name`            | VARCHAR            | Official name of the country                |     |                    |
| `Risk_Level`         | VARCHAR  | `Risk_Level`              | VARCHAR            | High/Medium/Low – used in jurisdiction scoring |     | Controlled vocabulary |
| `Sanctioned_Flag`    | BOOLEAN  | `Sanctioned_Flag`         | BOOLEAN            | TRUE if the country is under sanctions      |     | Used in blacklist screening |

---

### 🧪 Technical Fields (for SCD2 tracking):

| Field Name            | Type       | Description                                   |
|------------------------|------------|-----------------------------------------------|
| `scd_change_type`      | STRING     | `'cdc_insert'`, `'cdc_update'`, `'cdc_delete'`|
| `cdc_index`            | INT        | Row change order index                        |
| `scd_change_timestamp` | TIMESTAMP  | Record ingestion or update timestamp          |
| `ds_partition_date`    | DATE       | Partitioning column                           |
| `created_at`           | TIMESTAMP  | Initial load timestamp                        |
| `updated_at`           | TIMESTAMP  | Last update timestamp                         |
| `dtf_start_date`       | DATE       | Validity start (SCD2 logic)                   |
| `dtf_end_date`         | DATE       | Validity end                                  |
| `dtf_current_flag`     | BOOLEAN    | TRUE = currently active row                   |

---

### ✅ Notes:
- Used in rules like: "Transactions from sanctioned or high-risk countries"
- Can be mapped to FATF or internal jurisdictional rating models
- Joins to `Fact_Transaction`, `Dim_Customer`, `Fact_Alert`, etc.
