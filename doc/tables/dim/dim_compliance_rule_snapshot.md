## 📜 Table: Dim_Compliance_Rule_Snapshot

This dimension captures the full state of compliance detection rules in effect on any given day. Using `SCD4a`, it maintains the latest version in the main table and daily full snapshots in the history table. Designed to support model explainability, audit trail, and rollback validation.

- **Type**: Dimension  
- **CDC Type**: `1.3` (with `created_at`, `updated_at` at source)  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Rule_ID`  
- **Partitioned By**: `ds_partition_date` (history table)  
- **Snapshot Strategy**: Full rule snapshot daily; main shows current configuration

---

### 🧩 Main Table Schema (Latest Version Only)

| Column Name         | Type     | Description                                  |
|---------------------|----------|----------------------------------------------|
| `Rule_ID`           | VARCHAR  | Unique identifier for each compliance rule   |
| `Rule_Name`         | VARCHAR  | Human-readable name of the rule              |
| `Rule_SQL`          | TEXT     | Full SQL or expression logic for the rule    |
| `Severity_Level`    | VARCHAR  | Risk level triggered (e.g., LOW, HIGH)       |
| `Thresholds`        | VARCHAR  | Rule parameters/thresholds in use            |
| `Effective_Date`    | DATE     | When the rule version became active          |
| `Rule_Group`        | VARCHAR  | Logical group (e.g., Transaction, KYC)       |
| `Is_Enabled`        | BOOLEAN  | Whether the rule is currently active         |

#### 🧪 Technical Fields (Main Table):
| Column Name            | Type       | Description                                  |
|------------------------|------------|----------------------------------------------|
| `scd_change_type`      | STRING     | 'cdc_insert' or 'cdc_update'                 |
| `cdc_index`            | INT        | Optional order/version counter               |
| `scd_change_timestamp` | TIMESTAMP  | Time of snapshot ingestion                   |
| `dtf_start_date`       | DATE       | Start of this rule version                   |
| `dtf_end_date`         | DATE       | NULL if current version                      |
| `dtf_current_flag`     | BOOLEAN    | TRUE = active rule version                   |

---

### 🗃 History Table Schema (Daily Snapshots)

Contains all fields from the main table, **plus:**

| Column Name          | Type     | Description                                  |
|----------------------|----------|----------------------------------------------|
| `ds_partition_date`  | DATE     | Snapshot ingestion date (partition field)    |

---

### ✅ Business Use Cases
- Track what rule logic and thresholds were applied on any given day
- Explain why a customer was flagged based on past rule versions
- Detect and test rule tuning impact by version
- Provide audit logs for model governance and regulatory validation
