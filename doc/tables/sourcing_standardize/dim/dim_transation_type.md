## 📜 Table: Dim_Transaction_Type

This dimension defines the classification and description of each transaction type (e.g., cash withdrawal, online transfer). It is used to categorize transactions in fact tables for AML analysis, fee policy mapping, and reporting.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd2`  
- **Primary Key**: `Transaction_Type_ID`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Maintains a reference list of transaction types used across financial systems and channels.

---

### 📊 Key Columns:

| Raw Column Name         | Raw Type | Standardized Column Name     | Standardized Type | Description                                 | PK  | Note         |
|--------------------------|----------|-------------------------------|--------------------|---------------------------------------------|-----|--------------|
| `Transaction_Type_ID`    | VARCHAR  | `Transaction_Type_ID`         | VARCHAR            | Unique ID for the transaction type          | ✅  | Primary key  |
| `Transaction_Code`       | VARCHAR  | `Transaction_Code`            | VARCHAR            | Internal or standard code (e.g., TR001)     |     | Used for joins |
| `Description`            | VARCHAR  | `Description`                 | VARCHAR            | Human-readable transaction type label       |     |               |

---

### 🧪 Technical Fields (for SCD2 tracking):

| Field Name            | Type       | Description                                   |
|------------------------|------------|-----------------------------------------------|
| `scd_change_type`      | STRING     | `'cdc_insert'`, `'cdc_update'`, `'cdc_delete'`|
| `cdc_index`            | INT        | Row change index                              |
| `scd_change_timestamp` | TIMESTAMP  | Record load timestamp                         |
| `ds_partition_date`    | DATE       | Partition date                                |
| `created_at`           | TIMESTAMP  | Time of creation                              |
| `updated_at`           | TIMESTAMP  | Last modified timestamp                       |
| `dtf_start_date`       | DATE       | SCD2 effective start date                     |
| `dtf_end_date`         | DATE       | SCD2 effective end date                       |
| `dtf_current_flag`     | BOOLEAN    | TRUE if record is currently active            |

---

### ✅ Notes:
- Joins to `Fact_Transaction`, `Fact_Card_Transaction`, etc.
- Important for AML rules like detecting unusual transaction patterns
- Used in dashboard filters and summary reporting
