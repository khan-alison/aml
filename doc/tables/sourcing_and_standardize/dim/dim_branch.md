## 📜 Table: Dim_Branch

This dimension stores metadata about each bank branch, including location, region, and operational status. It supports transaction geolocation, KYC validation, and regional segmentation for AML analytics.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd2`  
- **Primary Key**: `Branch_ID`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Maintains SCD2 history of each branch’s operational and regional attributes.

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Branch | Raw Type | Standardized/Dim_Branch | Standardized Type | Description                                     | PK  | Note                       |
|----------------|----------|--------------------------|-------------------|-------------------------------------------------|-----|----------------------------|
| `Branch_ID`     | VARCHAR  | `Branch_ID`              | VARCHAR           | Unique branch identifier                        | ✅  | Primary key                |
| `Branch_Name`   | VARCHAR  | `Branch_Name`            | VARCHAR           | Human-readable name of the branch               |     |                            |
| `Region`        | VARCHAR  | `Region`                 | VARCHAR           | Geographical region (e.g., North, Central)      |     |                            |
| `Province`      | VARCHAR  | `Province`               | VARCHAR           | Province where branch is located                |     |                            |
| `Status`        | VARCHAR  | `Status`                 | VARCHAR           | ACTIVE, CLOSED, or UNDER_MAINTENANCE            |     | Lifecycle status           |
| `Open_Date`     | DATE     | `Open_Date`              | DATE              | Date when branch was established                |     |                            |
| `Close_Date`    | DATE     | `Close_Date`             | DATE              | Date when branch was decommissioned             |     | Nullable                   |
| `created_at`    | TIMESTAMP| `created_at`             | TIMESTAMP         | Timestamp when record was created in source     |     | From source (CDC 1.3)      |
| `updated_at`    | TIMESTAMP| `updated_at`             | TIMESTAMP         | Timestamp when record was last updated in source|     | From source (CDC 1.3)      |
| **Technical Fields (for CDC + audit + snapshot logic)** |          |                          |                   |                                                 |     |                            |
|                 |          | `scd_change_type`         | STRING            | `'cdc_insert'` / `'cdc_update'`                 |     | CDC 1.3 logic              |
|                 |          | `cdc_index`               | INT               | Ingestion sequence index                        |     | Optional                   |
|                 |          | `scd_change_timestamp`    | TIMESTAMP         | Snapshot load timestamp                         |     | Technical field            |
|                 |          | `dtf_start_date`          | DATE              | Effective start date                            |     | Technical field            |
|                 |          | `dtf_end_date`            | DATE              | Effective end date (NULL = current)             |     | Technical field            |
|                 |          | `dtf_current_flag`        | BOOLEAN           | TRUE = currently valid                          |     | Technical field            |


---

### ✅ Notes

- Branch dimensions enable regional AML segmentation and reporting  
- Helps geolocate source of high-risk transactions  
- SCD2 allows us to trace history of branch status changes for audit purposes

---

➡️ **Next Table:** `Dim_Currency`