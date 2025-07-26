## 📜 Table: Dim_Customer_Asset_Ownership

This dimension defines the link between customers and the assets they own (e.g., vehicles, properties, securities). It supports risk profiling, ownership enrichment in alerts, and financial exposure analysis. The data changes over time and is managed using SCD4a logic.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `ds_key`  
- **Main Table**: `Dim_Customer_Asset_Ownership` – holds current version only  
- **History Table**: `Dim_Customer_Asset_Ownership_Hist` – full version history with partitioning  
- **Partitioned By**: `ds_partition_date` (in `_Hist` table only)  
- **Snapshot Strategy**: SCD4a – current record in main table, historical versions in `_Hist`

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Customer_Asset_Ownership | Raw Type  | PK (Source) | Standardized/Dim_Customer_Asset_Ownership | Standardized Type | Standardized/Dim_Customer_Asset_Ownership_Hist | Description                                              | PK  | Value of Technical Field         | Note                          |
|----------------------------------|-----------|-------------|-------------------------------------------|-------------------|--------------------------------------------------|----------------------------------------------------------|-----|----------------------------------|-------------------------------|
| `Customer_ID`                    | STRING    | ✅          | `Customer_ID`                             | STRING            | `Customer_ID`                                   | Customer who owns the asset                             |     |                                  | FK to `Dim_Customer`         |
| `Asset_ID`                       | STRING    | ✅          | `Asset_ID`                                | STRING            | `Asset_ID`                                      | Identifier of the owned asset                           |     |                                  | FK to `Dim_Asset`            |
| `Ownership_Type`                | STRING    |             | `Ownership_Type`                          | STRING            | `Ownership_Type`                                | Sole, Joint, Guarantor, etc.                            |     |                                  | Classification                |
| `Ownership_Percentage`          | DECIMAL   |             | `Ownership_Percentage`                    | DECIMAL(5,2)      | `Ownership_Percentage`                          | Percentage of ownership held by the customer            |     |                                  | May be < 100% or NULL        |
| `Ownership_Start_Date`          | DATE      |             | `Ownership_Start_Date`                    | DATE              | `Ownership_Start_Date`                          | When the asset ownership started                        |     |                                  | Used in history logic        |
| `Ownership_End_Date`            | DATE      |             | `Ownership_End_Date`                      | DATE              | `Ownership_End_Date`                            | When the asset ownership ended (nullable)               |     |                                  | Optional                     |
| `created_at`                    | TIMESTAMP |             | `created_at`                              | TIMESTAMP         | `created_at`                                    | First seen in source                                    |     | From source                      |                              |
| `updated_at`                    | TIMESTAMP |             | `updated_at`                              | TIMESTAMP         | `updated_at`                                    | Last update seen from source                            |     | From source                      |                              |
| **Technical Fields**            |           |             |                                           |                   |                                                  |                                                          |     |                                  |                              |
|                                  |           |             | `ds_key`                                   | STRING            | `ds_key`                                        | Surrogate primary key                                   | ✅  | `md5(Customer_ID || Asset_ID)`  | Required for SCD4a            |
|                                  |           |             | `cdc_index`                                | INT               | `cdc_index`                                     | 1 = current, 0 = outdated                               |     | `1` or `0`                       | Filtering logic              |
|                                  |           |             | `cdc_change_type`                          | STRING            | `cdc_change_type`                               | Type of CDC event                                       |     | `'cdc_insert'`, `'cdc_update'`  | From CDC 1.3                 |
|                                  |           |             | `scd_change_timestamp`                     | TIMESTAMP         | `scd_change_timestamp`                          | When the change was processed                           |     | `updated_at` or job timestamp    |                              |
|                                  |           |             | `dtf_start_date`                           | DATE              | `dtf_start_date`                                | Start of record validity                                |     | Derived from partition or event |                              |
|                                  |           |             | `dtf_end_date`                             | DATE              | `dtf_end_date`                                  | End of record validity (null if current)                |     | NULL if current                  |                              |
|                                  |           |             | `dtf_current_flag`                         | BOOLEAN            | `dtf_current_flag`                              | Indicates whether this is the current version           |     | TRUE/FALSE                       |                              |
|                                  |           |             |                                            |                   | `ds_partition_date`                             | Partitioning column for history table only             |     | Job date (yyyy-MM-dd)            | Only exists in `_Hist`       |

---

### ✅ Business Use Cases

- Identify and quantify customer ownership across assets  
- Detect high-value individuals based on jointly held or hidden assets  
- Support scenarios like pledge fraud, shell ownership, and nominee structures  
- Enable enhanced due diligence for wealthy individuals or businesses  