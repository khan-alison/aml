## 📜 Table: Dim_KYC_Event

This dimension tracks individual KYC field changes as discrete events, allowing detailed lineage, rollback, and review of all customer profile modifications. It complements `Fact_KYC_Change_Log` but stores a deduplicated or summarized form for join efficiency.

- **Type**: Dimension  
- **CDC Type**: `1.1`  
- **Writer Type**: `scd1`  
- **Primary Key**: `KYC_Event_ID`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Event-style table tracking field-level KYC updates linked to customer ID and change metadata.

---

### 🔗 Foreign Keys and Relationships:

| Column         | Referenced Table       | Description |
|----------------|------------------------|-------------|
| `Customer_ID`  | `Dim_Customer`         | Customer whose KYC record changed  |
| `Change_Date`  | `Dim_Time`             | Date when the change occurred      |

---

### 📊 Key Columns:

| Raw Column Name     | Raw Type | Standardized Column Name | Standardized Type | Description                              | PK  | Note                |
|----------------------|----------|---------------------------|--------------------|------------------------------------------|-----|---------------------|
| `KYC_Event_ID`       | VARCHAR  | `KYC_Event_ID`            | VARCHAR            | Unique ID of the KYC event               | ✅  | Primary key         |
| `Customer_ID`        | VARCHAR  | `Customer_ID`             | VARCHAR            | Customer reference                        |     | FK to `Dim_Customer`|
| `Change_Type`        | VARCHAR  | `Change_Type`             | VARCHAR            | Type of change (e.g., address, phone)     |     | Business logic tag  |
| `Old_Value`          | TEXT     | `Old_Value`               | TEXT               | Previous value                            |     | PII may exist       |
| `New_Value`          | TEXT     | `New_Value`               | TEXT               | New value after update                    |     |                     |
| `Change_Date`        | DATE     | `Change_Date`             | DATE               | Date of change                            |     | FK to `Dim_Time`    |

---

### 🧪 Technical Fields:

| Field Name            | Type       | Description                                |
|------------------------|------------|--------------------------------------------|
| `cdc_change_type`      | STRING     | `'cdc_insert'` (append-only)               |
| `cdc_index`            | INT        | Row index if needed                        |
| `scd_change_timestamp` | TIMESTAMP  | Record ingestion time                      |
| `ds_partition_date`    | DATE       | Partition date                             |
| `created_at`           | TIMESTAMP  | When the row was created                   |
| `updated_at`           | TIMESTAMP  | Usually NULL (since it is append-only)     |

---

### ✅ Notes:
- Mirrors `Fact_KYC_Change_Log` for light joins in enrichment pipelines
- Designed for point-in-time KYC rollback, lineage, and AML traceability
- Can be filtered by `Change_Type` for profiling changes (e.g., address volatility)
