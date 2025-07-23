## 📜 Table: Dim_Customer_Asset_Ownership

This dimension defines the link between customers and the assets they own (e.g., vehicles, properties, securities). It supports risk profiling, ownership enrichment in alerts, and financial exposure analysis. The data changes over time and is managed using SCD4a logic.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Customer_ID` + `Asset_ID` (from source)  
- **Partitioned By**: `ds_partition_date` (string, in `_Hist` table only)  
- **Snapshot Strategy**: SCD4a – latest record in main table, full history in `_Hist`

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Customer_Asset_Ownership | Raw Type  | PK  | Standardized/Dim_Customer_Asset_Ownership | Standardized Type | Description                                              | Value of Technical Field         | Note                          |
|----------------------------------|-----------|-----|-------------------------------------------|--------------------|----------------------------------------------------------|----------------------------------|-------------------------------|
| `Customer_ID`                    | STRING    | ✅  | `Customer_ID`                             | STRING             | Customer who owns the asset                             |                                  | FK to `Dim_Customer`         |
| `Asset_ID`                       | STRING    | ✅  | `Asset_ID`                                | STRING             | Identifier of the owned asset                           |                                  | FK to `Dim_Asset`            |
| `Ownership_Type`                | STRING    |     | `Ownership_Type`                          | STRING             | Sole, Joint, Guarantor, etc.                            |                                  | Classification                |
| `Ownership_Percentage`          | DECIMAL   |     | `Ownership_Percentage`                    | DECIMAL(5,2)       | Percentage of ownership held by the customer            |                                  | May be < 100% or NULL        |
| `Ownership_Start_Date`          | DATE      |     | `Ownership_Start_Date`                    | DATE               | When the asset ownership started                        |                                  | Used in history logic        |
| `Ownership_End_Date`            | DATE      |     | `Ownership_End_Date`                      | DATE               | When the asset ownership ended (if applicable)          |                                  | Nullable                     |
| `created_at`                    | TIMESTAMP |     | `created_at`                              | TIMESTAMP          | First seen in source                                    | From source                      |                              |
| `updated_at`                    | TIMESTAMP |     | `updated_at`                              | TIMESTAMP          | Last seen update from source                            | From source                      |                              |
| **Technical Fields**            |           |     |                                           |                    |                                                          |                                  |                              |
|                                  |           |     | `ds_key`                                   | STRING             | Surrogate primary key in Standardized zone              | `md5(Customer_ID || Asset_ID)`  | Required in SCD4a             |
|                                  |           |     | `cdc_index`                                | INT                | Current record indicator                                | `1` or `0`                       | 1 = current                  |
|                                  |           |     | `cdc_change_type`                          | STRING             | Type of CDC event                                       | `'cdc_insert'`, `'cdc_update'`  |                              |
|                                  |           |     | `scd_change_timestamp`                     | TIMESTAMP          | When the change was processed                           | `updated_at` or job timestamp    |                              |
|                                  |           |     | `dtf_start_date`                           | DATE               | Start of validity period                                | From `updated_at` or job date    |                              |
|                                  |           |     | `dtf_end_date`                             | DATE               | End of validity period                                  | NULL if current                  |                              |
|                                  |           |     | `dtf_current_flag`                         | BOOLEAN            | TRUE if currently valid                                 | TRUE/FALSE                       |                              |
|                                  |           |     | `ds_partition_date`                        | STRING             | Partition column (yyyy-MM-dd)                           | Job run date                     | Only used in `_Hist`         |

---

### ✅ Business Use Cases

- Identify and quantify customer ownership across assets  
- Detect high-value individuals based on jointly held or hidden assets  
- Support scenarios like pledge fraud, shell ownership, and nominee structures  
- Enable enhanced due diligence for wealthy individuals or businesses  