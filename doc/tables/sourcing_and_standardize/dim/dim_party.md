## 📜 Table: Dim_Party

This dimension captures detailed reference information for external and internal parties involved in financial transactions, including individuals, organizations, vendors, and counterparties. It supports AML peer analysis, counterparty screening, and linkage detection.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd2`  
- **Primary Key**: `Party_ID`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Stores metadata for all known entities engaged in transactions or relationships, with flags indicating customer linkage and registration details.

---

### 📊 Key Columns:

| Raw Column Name         | Raw Type | Standardized Column Name | Standardized Type | Description                                       | PK  | Note                  |
|--------------------------|----------|---------------------------|--------------------|---------------------------------------------------|-----|-----------------------|
| `Party_ID`               | VARCHAR  | `Party_ID`                | VARCHAR            | Unique party identifier                          | ✅  | Primary key           |
| `Party_Type`            | VARCHAR  | `Party_Type`              | VARCHAR            | Type (e.g., INDIVIDUAL, CORPORATE, GOVERNMENT)   |     | Categorical           |
| `Party_Name`            | VARCHAR  | `Party_Name`              | VARCHAR            | Name of the party                                |     | Screening use         |
| `Registration_Number`   | VARCHAR  | `Registration_Number`     | VARCHAR            | Business or personal ID number                   |     | Can be sensitive (PII) |
| `Country`               | VARCHAR  | `Country`                 | VARCHAR            | Country of registration or residence             |     | FK to `Dim_Country`    |
| `Address`               | VARCHAR  | `Address`                 | VARCHAR            | Registered or known address                      |     | Can be PII             |
| `Status`                | VARCHAR  | `Status`                  | VARCHAR            | ACTIVE, INACTIVE, CLOSED                         |     | Operational use        |
| `Is_Customer_Flag`      | BOOLEAN  | `Is_Customer_Flag`        | BOOLEAN            | TRUE if also present in `Dim_Customer`           |     | Linkage to customers   |

---

### 🧪 Technical Fields (for SCD2 tracking):

| Field Name            | Type       | Description                                   |
|------------------------|------------|-----------------------------------------------|
| `scd_change_type`      | STRING     | `'cdc_insert'`, `'cdc_update'`, `'cdc_delete'`|
| `cdc_index`            | INT        | Row index for ordering changes                |
| `scd_change_timestamp` | TIMESTAMP  | Timestamp of ingestion                        |
| `ds_partition_date`    | DATE       | Partition date for table                      |
| `created_at`           | TIMESTAMP  | Record creation timestamp                     |
| `updated_at`           | TIMESTAMP  | Record last modified timestamp                |
| `dtf_start_date`       | DATE       | SCD2 start date                               |
| `dtf_end_date`         | DATE       | SCD2 end date                                 |
| `dtf_current_flag`     | BOOLEAN    | TRUE = record currently active                |

---

### ✅ Notes:
- Joins with `Fact_Party_Linkage`, `Fact_Transaction_Peer_Pair`, and alerts
- Enables identification of related parties, shell companies, or duplicate identities
- Can be loaded from internal registries and external watchlists
