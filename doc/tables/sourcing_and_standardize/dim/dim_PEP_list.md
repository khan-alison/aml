## 📜 Table: Dim_PEP_List

This dimension represents the latest list of Politically Exposed Persons (PEPs), including name, position, and jurisdiction. It is used for name screening, enhanced due diligence (EDD), and real-time transaction risk assessments.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd1`  
- **Primary Key**: `National_ID`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Provides a flat list of known or declared PEPs with identification metadata, last verification timestamp, and their official role.

---

### 📊 Key Columns (Standardize)

| Raw/Dim_PEP_List   | Raw Type | Standardized/std_PEP_List | Standardized Type | Description                                       | PK  | Note                     |
|--------------------|----------|----------------------------|-------------------|---------------------------------------------------|-----|--------------------------|
| `National_ID`      | VARCHAR  | `National_ID`              | VARCHAR           | National ID or unique identifier of the PEP       | ✅  | Primary key              |
| `Name`             | VARCHAR  | `Name`                     | VARCHAR           | Full name of the PEP                              |     | Used in screening         |
| `Country`          | VARCHAR  | `Country`                  | VARCHAR           | Country or jurisdiction where the PEP holds office|     | FK to `Dim_Country`       |
| `Position`         | VARCHAR  | `Position`                 | VARCHAR           | Title or political position                       |     | Minister, Judge, etc.     |
| `Last_Verified_Date`| DATE    | `Last_Verified_Date`       | DATE              | When this record was last confirmed or updated    |     | Refresh needed regularly  |
| `created_at`       | TIMESTAMP| `created_at`               | TIMESTAMP         | Timestamp when row was ingested                   |     | Required for CDC 1.3      |
| `updated_at`       | TIMESTAMP| `updated_at`               | TIMESTAMP         | Last updated timestamp from source                |     | Required for CDC 1.3      |
| **Technical Fields (for CDC + audit)** |          |                        |                   |                                                   |     |                          |
|                    |          | `scd_change_type`          | STRING            | `'cdc_insert'` or `'cdc_update'`                 |     | CDC 1.3 logic              |
|                    |          | `cdc_index`                | INT               | Optional monotonic change order                  |     |                          |
|                    |          | `scd_change_timestamp`     | TIMESTAMP         | Time of snapshot ingestion                        |     |                          |
|                    |          | `ds_partition_date`        | DATE              | Partition date used for storage                   |     | Required                   |

---

### ✅ Notes

- Typically sourced from government or vendor-maintained watchlists  
- Supports join with `Dim_Customer` on ID or name for real-time alerting  
- Enables scoring models that raise risk based on PEP exposure  
- Maintained via periodic batch loads with validation audit trail  