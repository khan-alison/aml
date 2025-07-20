## 📜 Table: Dim_PEP_List

This dimension represents the latest list of Politically Exposed Persons (PEPs), including name, position, and jurisdiction. It is used for name screening, enhanced due diligence (EDD), and real-time transaction risk assessments.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd1`  
- **Primary Key**: `National_ID`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Provides a flat list of known or declared PEPs with identification metadata, last verification timestamp, and their official role.

---

### 📊 Key Columns:

| Raw Column Name       | Raw Type | Standardized Column Name | Standardized Type | Description                                    | PK  | Note                    |
|------------------------|----------|---------------------------|--------------------|------------------------------------------------|-----|-------------------------|
| `National_ID`          | VARCHAR  | `National_ID`             | VARCHAR            | National ID or equivalent unique identifier    | ✅  | Primary key             |
| `Name`                | VARCHAR  | `Name`                    | VARCHAR            | Full name of the PEP                          |     | Used in screening        |
| `Country`             | VARCHAR  | `Country`                 | VARCHAR            | Jurisdiction where the person holds office     |     | Maps to `Dim_Country`    |
| `Position`            | VARCHAR  | `Position`                | VARCHAR            | Official or political position held            |     | Can be minister, judge, etc. |
| `Last_Verified_Date`  | DATE     | `Last_Verified_Date`      | DATE               | Date the entry was last validated              |     | Regular update expected  |

---

### 🧪 Technical Fields:

| Field Name            | Type       | Description                                   |
|------------------------|------------|-----------------------------------------------|
| `scd_change_type`      | STRING     | `'cdc_insert'`, `'cdc_update'`                |
| `cdc_index`            | INT        | Optional index                                |
| `scd_change_timestamp` | TIMESTAMP  | Timestamp of last load                        |
| `ds_partition_date`    | DATE       | Partitioning date                             |
| `created_at`           | TIMESTAMP  | Ingestion timestamp                           |
| `updated_at`           | TIMESTAMP  | Time of latest update                         |

---

### ✅ Notes:
- Typically sourced from public or vendor-managed PEP databases
- Should be joined to `Dim_Customer` for flagging and scoring
- Requires regular refresh and audit for regulatory compliance

