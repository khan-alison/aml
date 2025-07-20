## 📜 Table: Dim_Customer_Asset_Ownership

This bridge dimension defines the relationship between customers and their declared or verified assets. It supports modeling of joint ownership, beneficial ownership, and legal title for asset-based risk and wealth profiling.

- **Type**: Dimension (Bridge/Link)  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd2`  
- **Primary Key**: Composite — (`Customer_ID`, `Asset_ID`, `Declaration_Date`)  
- **Partitioned By**: *(N/A)*  
- **Description**: Tracks ownership relationships between customers and assets, including percentage split and declaration metadata.

---

### 🔗 Foreign Keys and Relationships:

| Column         | Referenced Table  | Description                        |
|----------------|-------------------|------------------------------------|
| `Customer_ID`  | `Dim_Customer`    | Owner or co-owner of the asset     |
| `Asset_ID`     | `Dim_Asset`       | Asset being referenced             |

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Customer_Asset_Ownership | Raw Type | Standardized/Dim_Customer_Asset_Ownership | Standardized Type | Description                                  | PK  | Note                         |
|----------------------------------|----------|--------------------------------------------|--------------------|----------------------------------------------|-----|------------------------------|
| `Customer_ID`                    | VARCHAR  | `Customer_ID`                               | VARCHAR            | Linked customer ID                           | ✅  | FK to `Dim_Customer`         |
| `Asset_ID`                       | VARCHAR  | `Asset_ID`                                  | VARCHAR            | Linked asset ID                              | ✅  | FK to `Dim_Asset`            |
| `Ownership_Type`                 | VARCHAR  | `Ownership_Type`                            | VARCHAR            | Type (SOLE, JOINT, BENEFICIAL)               |     | Controlled vocabulary        |
| `Ownership_Percentage`           | DECIMAL  | `Ownership_Percentage`                      | DECIMAL            | Percent of ownership                         |     | Must sum to ≤ 100% per asset |
| `Declaration_Date`               | DATE     | `Declaration_Date`                          | DATE               | When ownership was declared or validated     | ✅  | Part of PK                   |
| `created_at`                     | TIMESTAMP| `created_at`                                | TIMESTAMP          | Time of initial record creation in source    |     | From source (CDC 1.3)        |
| `updated_at`                     | TIMESTAMP| `updated_at`                                | TIMESTAMP          | Last update time in source                   |     | From source (CDC 1.3)        |
| **Technical Fields (for CDC + audit)**       |          |                                            |                    |                                              |     |                              |
|                                  |          | `scd_change_type`                           | STRING             | `'cdc_insert'`, `'cdc_update'`, `'cdc_delete'` |     | SCD2 tracking                |
|                                  |          | `cdc_index`                                 | INT                | Change index for ordering                    |     | Optional                     |
|                                  |          | `scd_change_timestamp`                      | TIMESTAMP          | When change was captured                     |     | Technical field              |
|                                  |          | `dtf_start_date`                            | DATE               | Start of ownership period                    |     | Technical field              |
|                                  |          | `dtf_end_date`                              | DATE               | End of ownership period                      |     | Technical field              |
|                                  |          | `dtf_current_flag`                          | BOOLEAN            | TRUE = current version                       |     | Technical field              |

---

### ✅ Notes:
- Used to derive asset-to-customer exposure for LTV and net worth  
- Enables tracing beneficial ownership in AML and onboarding  
- Helps handle partial or co-owned assets for reporting and model enrichment