## 📜 Table: Dim_Party

This dimension captures detailed reference information for external and internal parties involved in financial transactions, including individuals, organizations, vendors, and counterparties. It supports AML peer analysis, counterparty screening, and linkage detection.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd2`  
- **Primary Key**: `Party_ID`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Stores metadata for all known entities engaged in transactions or relationships, with flags indicating customer linkage and registration details.

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Party       | Raw Type | Standardized/std_Party   | Standardized Type | Description                                      | PK  | Note                    |
|---------------------|----------|---------------------------|-------------------|--------------------------------------------------|-----|-------------------------|
| `Party_ID`          | VARCHAR  | `Party_ID`                | VARCHAR           | Unique party identifier                          | ✅  | Primary key             |
| `Party_Type`        | VARCHAR  | `Party_Type`              | VARCHAR           | INDIVIDUAL, CORPORATE, GOVERNMENT, etc.          |     | Category classification |
| `Party_Name`        | VARCHAR  | `Party_Name`              | VARCHAR           | Name of the party                                |     | Used in screening       |
| `Registration_Number`| VARCHAR | `Registration_Number`     | VARCHAR           | Business or personal ID number                   |     | May be PII              |
| `Country`           | VARCHAR  | `Country`                 | VARCHAR           | Country of residence or registration             |     | FK to `Dim_Country`     |
| `Address`           | VARCHAR  | `Address`                 | VARCHAR           | Registered or known address                      |     | PII / location-based    |
| `Status`            | VARCHAR  | `Status`                  | VARCHAR           | ACTIVE, INACTIVE, CLOSED                         |     | Lifecycle indicator     |
| `Is_Customer_Flag`  | BOOLEAN  | `Is_Customer_Flag`        | BOOLEAN           | TRUE if this party also appears in `Dim_Customer`|     | Customer linkage         |
| `created_at`        | TIMESTAMP| `created_at`              | TIMESTAMP         | Source system creation time                      |     | CDC 1.3 requirement      |
| `updated_at`        | TIMESTAMP| `updated_at`              | TIMESTAMP         | Source system last modified time                 |     | CDC 1.3 requirement      |
|**Technical Fields (for CDC + audit + snapshot logic)**|          |                         |                   |                                                  |     |                         |
|                     |          | `scd_change_type`         | STRING            | `'cdc_insert'`, `'cdc_update'`, `'cdc_delete'`   |     | SCD2 tracking            |
|                     |          | `cdc_index`               | INT               | Row version sequencing                           |     | Optional                 |
|                     |          | `scd_change_timestamp`    | TIMESTAMP         | Ingestion timestamp                              |     |                         |
|                     |          | `dtf_start_date`          | DATE              | Start of current version                         |     |                         |
|                     |          | `dtf_end_date`            | DATE              | End of version (NULL = current)                  |     |                         |
|                     |          | `dtf_current_flag`        | BOOLEAN           | TRUE = currently active version                  |     |                         |


---

### ✅ Notes

- Joins with `Fact_Party_Linkage`, `Fact_Transaction_Peer_Pair`, and alerts  
- Enables identification of related parties, shell companies, or duplicate identities  
- Can be loaded from internal registries and external watchlists  