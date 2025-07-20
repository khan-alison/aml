## 📜 Table: Dim_Party_Role

This dimension defines the type of role a party (individual or organization) can play in a financial or legal context. Common roles include Beneficial Owner, Director, Guarantor, or Signatory. It is used to annotate party relationships and support network-based risk analysis.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd2`  
- **Primary Key**: `Role_ID`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: A controlled vocabulary of relationship roles used in AML party linkage and counterparty networks.

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Party_Role | Raw Type | Standardized/std_Party_Role | Standardized Type | Description                                   | PK  | Note                    |
|--------------------|----------|------------------------------|-------------------|-----------------------------------------------|-----|-------------------------|
| `Role_ID`          | VARCHAR  | `Role_ID`                    | VARCHAR           | Unique identifier for party role              | ✅  | Primary key             |
| `Role_Name`        | VARCHAR  | `Role_Name`                  | VARCHAR           | Name of the role (e.g., Guarantor, Director)  |     | Used in UI/reporting    |
| `Description`      | VARCHAR  | `Description`                | VARCHAR           | Optional narrative explaining the role        |     |                         |
| `created_at`       | TIMESTAMP| `created_at`                 | TIMESTAMP         | Record creation timestamp                     |     | CDC 1.3 required         |
| `updated_at`       | TIMESTAMP| `updated_at`                 | TIMESTAMP         | Last modified timestamp                       |     | CDC 1.3 required         |
|**Technical Fields (for CDC + audit + snapshot logic)**|          |                        |                   |                                               |     |                         |
|                    |          | `scd_change_type`            | STRING            | `'cdc_insert'`, `'cdc_update'`, `'cdc_delete'`|     | CDC 1.3 logic            |
|                    |          | `cdc_index`                  | INT               | Sequence for versioning                       |     | Optional                 |
|                    |          | `scd_change_timestamp`       | TIMESTAMP         | Ingestion timestamp                           |     |                         |
|                    |          | `dtf_start_date`             | DATE              | Start of validity                             |     |                         |
|                    |          | `dtf_end_date`               | DATE              | End of validity                               |     | NULL = currently active  |
|                    |          | `dtf_current_flag`           | BOOLEAN           | TRUE if currently active                      |     |                         |
|                    |          |                              |                   | `ds_partition_date`                           | Partition column for history table             |     | `_Hist` table only       |

---

### ✅ Notes

- Used with `Fact_Party_Linkage`, `Dim_Party`, and external KYC registries  
- Enables role-based screening and beneficial ownership modeling  
- Can be maintained in sync with onboarding questionnaire options  