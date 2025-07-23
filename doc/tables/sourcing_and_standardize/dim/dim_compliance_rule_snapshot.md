## 📜 Table: Dim_Compliance_Rule_Snapshot

This dimension stores snapshots of AML compliance rules used by the detection engine. Each version includes parameters, thresholds, severity, and business logic for a rule. It provides historical traceability for alert interpretation and audit reviews.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Rule_ID` (from source)  
- **Partitioned By**: `ds_partition_date` (string, in `_Hist` table only)  
- **Snapshot Strategy**: SCD4a – current version in main table, full history in `_Hist`

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Compliance_Rule_Snapshot | Raw Type  | PK  | Standardized/Dim_Compliance_Rule_Snapshot | Standardized Type | Description                                           | Value of Technical Field         | Note                          |
|----------------------------------|-----------|-----|--------------------------------------------|--------------------|-------------------------------------------------------|----------------------------------|-------------------------------|
| `Rule_ID`                        | STRING    | ✅  | `Rule_ID`                                  | STRING             | Unique identifier of the AML rule                    |                                  | Natural key from source       |
| `Rule_Name`                      | STRING    |     | `Rule_Name`                                | STRING             | Human-readable name of the rule                      |                                  |                               |
| `Rule_Type`                      | STRING    |     | `Rule_Type`                                | STRING             | Category (e.g., structuring, smurfing, PEP match)    |                                  | ENUM or controlled list       |
| `Rule_Logic`                     | STRING    |     | `Rule_Logic`                               | STRING             | Free-text or DSL logic defining rule conditions      |                                  | Snapshot required             |
| `Severity_Level`                 | STRING    |     | `Severity_Level`                           | STRING             | Low, Medium, High                                    |                                  | Drives alert level            |
| `Is_Active`                      | BOOLEAN   |     | `Is_Active`                                | BOOLEAN            | Whether this rule version is currently in use        |                                  |                              |
| `created_at`                     | TIMESTAMP |     | `created_at`                               | TIMESTAMP          | Time the rule version was first registered           | From source                      |                              |
| `updated_at`                     | TIMESTAMP |     | `updated_at`                               | TIMESTAMP          | Last update to the rule version                      | From source                      |                              |
| **Technical Fields**             |           |     |                                            |                    |                                                       |                                  |                              |
|                                  |           |     | `ds_key`                                   | STRING             | Surrogate primary key in standardized zone           | `Rule_ID`                        | Required for tracking         |
|                                  |           |     | `cdc_index`                                | INT                | 1 = current, 0 = outdated                            | `1` or `0`                       | Used in SCD logic             |
|                                  |           |     | `cdc_change_type`                          | STRING             | CDC change type                                      | `'cdc_insert'`, `'cdc_update'`  |                              |
|                                  |           |     | `scd_change_timestamp`                     | TIMESTAMP          | Change detection timestamp                           | `updated_at` or job time         |                              |
|                                  |           |     | `dtf_start_date`                           | DATE               | Start of rule version validity                       | From `updated_at` or partition   |                              |
|                                  |           |     | `dtf_end_date`                             | DATE               | End of rule version validity                         | NULL if current                  |                              |
|                                  |           |     | `dtf_current_flag`                         | BOOLEAN            | TRUE if current version                              | TRUE/FALSE                       |                              |
|                                  |           |     | `ds_partition_date`                        | STRING             | Partition column (`yyyy-MM-dd`)                      | Job run date                     | Only used in `_Hist`          |

---

### ✅ Business Use Cases

- Ensure transparency of rule changes over time  
- Reconstruct exact logic used to trigger historical alerts  
- Drive compliance reports and regulator-facing documentation  
- Enable rollback, simulation, and testing of rule versions  