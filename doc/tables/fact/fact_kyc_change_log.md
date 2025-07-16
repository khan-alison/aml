## 📜 Table: Fact_KYC_Change_Log

This table logs all field-level changes made to a customer's KYC (Know Your Customer) profile. It is essential for regulatory compliance, audit trails, and understanding the history of identity or profile changes.

- **Type**: Fact  
- **CDC Type**: `1.1`  
- **Writer Type**: `factAppend`  
- **Primary Key**: None (append-only log table)  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Captures every KYC field change with previous and new values, timestamp, reason, and who initiated the change.

---

### 🔗 Foreign Keys and Relationships:

| Column           | Referenced Table       | Description |
|------------------|------------------------|-------------|
| `Customer_ID`    | `Dim_Customer`         | Customer affected by the KYC change  |
| `Change_Timestamp`| `Dim_Time`            | When the change occurred             |

---

### 📊 Key Columns:

| Raw Column Name       | Raw Type   | Standardized Column Name | Standardized Type | Description                                     | PK  | Note                    |
|------------------------|------------|---------------------------|--------------------|-------------------------------------------------|-----|-------------------------|
| `Customer_ID`          | VARCHAR    | `Customer_ID`             | VARCHAR            | Identifier of the customer                     |     | FK to `Dim_Customer`    |
| `Change_Field`         | VARCHAR    | `Change_Field`            | VARCHAR            | Name of the field that was modified            |     |                         |
| `Old_Value`            | TEXT       | `Old_Value`               | TEXT               | Previous value before the change               |     |                         |
| `New_Value`            | TEXT       | `New_Value`               | TEXT               | New value after the change                     |     |                         |
| `Change_Timestamp`     | TIMESTAMP  | `Change_Timestamp`        | TIMESTAMP          | When the change occurred                       |     | FK to `Dim_Time`        |
| `Change_Reason`        | VARCHAR    | `Change_Reason`           | VARCHAR            | Reason for making the change                   |     | Optional (if provided)  |
| `Initiated_By`         | VARCHAR    | `Initiated_By`            | VARCHAR            | Staff or process that initiated the change     |     |                         |

---

### 🧪 Technical Fields (for CDC + audit):

| Raw Column Name        | Raw Type | Standardized Column Name | Standardized Type | Description                               | PK  | Note                  |
|------------------------|----------|---------------------------|--------------------|-------------------------------------------|-----|-----------------------|
| `cdc_change_type`      | STRING   | `cdc_change_type`         | STRING             | Always `'cdc_insert'` (append-only)        |     | CDC 1.1 logic         |
| `cdc_index`            | INT      | `cdc_index`               | INT                | Optional index                             |     |                       |
| `scd_change_timestamp` | TIMESTAMP| `scd_change_timestamp`    | TIMESTAMP          | Time record was processed                  |     |                       |
| `ds_partition_date`    | DATE     | `ds_partition_date`       | DATE               | Partitioning date                          |     | From Change_Timestamp |
| `created_at`           | TIMESTAMP| `created_at`              | TIMESTAMP          | Time of insertion                          |     |                       |
| `updated_at`           | TIMESTAMP| `updated_at`              | TIMESTAMP          | Usually null in CDC 1.1                    |     |                       |

---

### ✅ Notes:
- Append-only structure ensures traceable audit trail
- No updates or deletes — every change is a new row
- Used by compliance, onboarding teams, and audit reviewers
