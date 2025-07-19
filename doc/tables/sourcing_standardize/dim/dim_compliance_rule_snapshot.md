## 📜 Table: Dim_Compliance_Rule_Snapshot

This dimension captures the full state of compliance detection rules in effect on any given day. Using `SCD4a`, it maintains the latest version in the main table and daily full snapshots in the history table. Designed to support model explainability, audit trail, and rollback validation.

- **Type**: Dimension  
- **CDC Type**: `1.3` (with `created_at`, `updated_at` at source)  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Rule_ID`  
- **Partitioned By**: `ds_partition_date` (in history table)  
- **Snapshot Strategy**: Full rule snapshot daily; main shows current configuration

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Compliance_Rule_Snapshot | Raw Type | Standardized/std_Compliance_Rule_Snapshot | Standardized Type | Standardized/std_Compliance_Rule_Snapshot_Hist | Description                                      | PK  | Note                             |
|----------------------------------|----------|-------------------------------------------|-------------------|--------------------------------------------------|--------------------------------------------------|-----|----------------------------------|
| `Rule_ID`                        | VARCHAR  | `Rule_ID`                                 | VARCHAR           | `Rule_ID`                                        | Unique identifier for each compliance rule       | ✅  |                                  |
| `Rule_Name`                      | VARCHAR  | `Rule_Name`                               | VARCHAR           | `Rule_Name`                                     | Human-readable name of the rule                  |     |                                  |
| `Rule_SQL`                       | TEXT     | `Rule_SQL`                                | TEXT              | `Rule_SQL`                                      | Full SQL or expression logic for the rule        |     |                                  |
| `Severity_Level`                 | VARCHAR  | `Severity_Level`                          | VARCHAR           | `Severity_Level`                                | Risk level triggered (e.g., LOW, HIGH)           |     |                                  |
| `Thresholds`                     | VARCHAR  | `Thresholds`                              | VARCHAR           | `Thresholds`                                    | Parameters or rule thresholds                    |     |                                  |
| `Effective_Date`                 | DATE     | `Effective_Date`                          | DATE              | `Effective_Date`                                | When the rule version became active              |     |                                  |
| `Rule_Group`                     | VARCHAR  | `Rule_Group`                              | VARCHAR           | `Rule_Group`                                    | Logical group (e.g., Transaction, KYC)           |     |                                  |
| `Is_Enabled`                     | BOOLEAN  | `Is_Enabled`                              | BOOLEAN           | `Is_Enabled`                                    | Whether the rule is currently active             |     |                                  |
|Technical Fields (for CDC + audit + snapshot logic)|
|                  |          | `scd_change_type`             | STRING    | `scd_change_type`             | `'cdc_insert'` or `'cdc_update'`                    |     | CDC 1.3 logic                  |
|                  |          | `cdc_index`                   | INT       | `cdc_index`                   | Change order index (optional)                        |     |                               |
|                  |          | `scd_change_timestamp`        | TIMESTAMP | `scd_change_timestamp`        | Timestamp of ingestion                               |     |                               |
|                  |          | `dtf_start_date`              | DATE      | `dtf_start_date`              | Snapshot start date                                  |     |                               |
|                  |          | `dtf_end_date`                | DATE      | `dtf_end_date`                | Snapshot end date (null = currently active)          |     |                               |
|                  |          | `dtf_current_flag`            | BOOLEAN   | `dtf_current_flag`            | TRUE if current active version                       |     |                               |
|                  |          |                               |           | `ds_partition_date`           | Partition date for history table only                |     | `_Hist` table only            |

---

### ✅ Business Use Cases

- Track what rule logic and thresholds were applied on any given day  
- Explain why a customer was flagged based on past rule versions  
- Detect and test rule tuning impact by version  
- Provide audit logs for model governance and regulatory validation