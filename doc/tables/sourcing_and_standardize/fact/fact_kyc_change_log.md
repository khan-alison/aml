## 📜 Table: Fact_KYC_Change_Log

This table logs all field-level changes made to a customer's KYC (Know Your Customer) profile. It is essential for regulatory compliance, audit trails, and understanding the history of identity or profile changes.

- **Type**: Fact  
- **CDC Type**: `1.1`  
- **Writer Type**: `factAppend`  
- **Primary Key**: *(None)*  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Captures every KYC field change with previous and new values, timestamp, reason, and who initiated the change.

---

### 📊 Key Columns (Standardize)

| Raw/Fact_KYC_Change_Log | Raw Type | Standardized/Fact_KYC_Change_Log | Standardized Type | Description                                         | PK  | Note                     |
|--------------------------|----------|-----------------------------------|--------------------|-----------------------------------------------------|-----|--------------------------|
| `Customer_ID`            | VARCHAR  | `Customer_ID`                     | VARCHAR            | Customer whose KYC field was changed                |     | FK to `Dim_Customer`     |
| `Change_Field`           | VARCHAR  | `Change_Field`                    | VARCHAR            | Name of field modified                              |     |                          |
| `Old_Value`              | TEXT     | `Old_Value`                       | TEXT               | Value before the change                             |     |                          |
| `New_Value`              | TEXT     | `New_Value`                       | TEXT               | Value after the change                              |     |                          |
| `Change_Timestamp`       | TIMESTAMP| `Change_Timestamp`                | TIMESTAMP          | When the change occurred                            |     | FK to `Dim_Time`         |
| `Change_Reason`          | VARCHAR  | `Change_Reason`                   | VARCHAR            | Reason for change                                   |     | Optional                 |
| `Initiated_By`           | VARCHAR  | `Initiated_By`                    | VARCHAR            | Staff or process that made the change               |     |                          |

---

### 🧪 Technical Fields (CDC + Audit)

| Standardized Field       | Type       | Description                                     |
|--------------------------|------------|-------------------------------------------------|
| `cdc_change_type`        | STRING     | Always `'cdc_insert'` (CDC 1.1)                 |
| `cdc_index`              | INT        | Optional row sequence number                    |
| `scd_change_timestamp`   | TIMESTAMP  | Time record was processed                       |
| `ds_partition_date`      | DATE       | Partitioning date (usually from `Change_Timestamp`) |
| `cdc_checkpoint_index`   | LONG       | Optional if using streaming                     |

> 🚫 `created_at`, `updated_at` are **not used** in CDC 1.1 pipelines.

---

### ✅ Business Use Cases

- Enables full traceability of customer profile changes  
- Powers compliance reviews and KYC audits  
- Detects reclassification (e.g., nationality changed from high to low risk)  
- Supports behavioral monitoring tied to profile volatility