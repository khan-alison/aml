## 📜 Table: Dim_Compliance_Rule_Snapshot

This dimension stores snapshots of AML compliance rules used by the detection engine. Each version includes parameters, thresholds, severity, and business logic for a rule. It provides historical traceability for alert interpretation and audit reviews.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `ds_key`  
- **Main Table**: `Dim_Compliance_Rule_Snapshot` – holds only the latest rule version  
- **History Table**: `Dim_Compliance_Rule_Snapshot_Hist` – stores full version history  
- **Partitioned By**: `ds_partition_date` (in `_Hist` table only)  
- **Snapshot Strategy**: SCD4a – current version in main table, full SCD-tracked history in `_Hist`

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Compliance_Rule_Snapshot | Raw Type  | PK (Source) | Standardized/Dim_Compliance_Rule_Snapshot | Standardized Type | Standardized/Dim_Compliance_Rule_Snapshot_Hist | Description                                           | PK  | Value of Technical Field         | Note                          |
|----------------------------------|-----------|-------------|--------------------------------------------|-------------------|--------------------------------------------------|-------------------------------------------------------|-----|----------------------------------|-------------------------------|
| `Rule_ID`                        | STRING    | ✅          | `Rule_ID`                                  | STRING            | `Rule_ID`                                       | Unique identifier of the AML rule                    |     |                                  | Natural key from source       |
| `Rule_Name`                      | STRING    |             | `Rule_Name`                                | STRING            | `Rule_Name`                                     | Human-readable name of the rule                      |     |                                  |                               |
| `Rule_Type`                      | STRING    |             | `Rule_Type`                                | STRING            | `Rule_Type`                                     | Category (e.g., structuring, smurfing, PEP match)    |     |                                  | ENUM or controlled list       |
| `Rule_Logic`                     | STRING    |             | `Rule_Logic`                               | STRING            | `Rule_Logic`                                    | Free-text or DSL logic defining rule conditions      |     |                                  | Snapshot required             |
| `Severity_Level`                 | STRING    |             | `Severity_Level`                           | STRING            | `Severity_Level`                                | Low, Medium, High                                    |     |                                  | Drives alert level            |
| `Is_Active`                      | BOOLEAN   |             | `Is_Active`                                | BOOLEAN           | `Is_Active`                                     | Whether this rule version is currently in use        |     |                                  |                               |
| `created_at`                     | TIMESTAMP |             | `created_at`                               | TIMESTAMP         | `created_at`                                    | Time the rule version was first registered           |     | From source                      |                               |
| `updated_at`                     | TIMESTAMP |             | `updated_at`                               | TIMESTAMP         | `updated_at`                                    | Last update to the rule version                      |     | From source                      |                               |
| **Technical Fields**             |           |             |                                            |                   |                                                  |                                                       |     |                                  |                               |
|                                  |           |             | `ds_key`                                   | STRING            | `ds_key`                                        | Surrogate primary key                                | ✅  | `Rule_ID`                        | Required for tracking         |
|                                  |           |             | `cdc_index`                                | INT               | `cdc_index`                                     | 1 = current, 0 = outdated                            |     | `1` or `0`                       | Used in SCD logic             |
|                                  |           |             | `cdc_change_type`                          | STRING            | `cdc_change_type`                               | CDC change type                                     |     | `'cdc_insert'`, `'cdc_update'`  | From CDC 1.3                  |
|                                  |           |             | `scd_change_timestamp`                     | TIMESTAMP         | `scd_change_timestamp`                          | Timestamp of this version                           |     | `updated_at` or job time        | Required for audit            |
|                                  |           |             | `dtf_start_date`                           | DATE              | `dtf_start_date`                                | Start of rule version validity                      |     | From `ds_partition_date`        | SCD4a validity tracking       |
|                                  |           |             | `dtf_end_date`                             | DATE              | `dtf_end_date`                                  | End of rule version validity                        |     | NULL if current                  |                              |
|                                  |           |             | `dtf_current_flag`                         | BOOLEAN           | `dtf_current_flag`                              | Indicates whether record is the current version     |     | TRUE/FALSE                       |                              |
|                                  |           |             |                                            |                   | `ds_partition_date`                             | Partition column for historical table only          |     | Job run date (`yyyy-MM-dd`)     | Exists only in `_Hist` table  |

---

### ✅ Business Use Cases

- Ensure transparency of rule changes over time  
- Reconstruct exact logic used to trigger historical alerts  
- Drive compliance reports and regulator-facing documentation  
- Enable rollback, simulation, and testing of rule versions  