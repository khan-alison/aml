## 📜 Table: Dim_KYC_Event

This dimension tracks individual KYC field changes as discrete events, allowing detailed lineage, rollback, and review of all customer profile modifications. It complements `Fact_KYC_Change_Log` but stores a deduplicated or summarized form for join efficiency.

- **Type**: Dimension  
- **CDC Type**: `1.1`  
- **Writer Type**: `scd1`  
- **Primary Key**: `KYC_Event_ID`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Event-style table tracking field-level KYC updates linked to customer ID and change metadata.

---

### 📊 Key Columns (Standardize)

| Raw/Dim_KYC_Event | Raw Type | Standardized/std_KYC_Event | Standardized Type | Description                                  | PK  | Note                       |
|-------------------|----------|-----------------------------|--------------------|----------------------------------------------|-----|----------------------------|
| `KYC_Event_ID`    | VARCHAR  | `KYC_Event_ID`              | VARCHAR            | Unique ID of the KYC event                   | ✅  | Primary key                |
| `Customer_ID`     | VARCHAR  | `Customer_ID`               | VARCHAR            | Customer reference                           |     | FK to `Dim_Customer`       |
| `Change_Type`     | VARCHAR  | `Change_Type`               | VARCHAR            | Type of change (e.g., address, phone)        |     | Business logic tag         |
| `Old_Value`       | TEXT     | `Old_Value`                 | TEXT               | Previous value                               |     | May contain PII            |
| `New_Value`       | TEXT     | `New_Value`                 | TEXT               | New value after update                       |     |                            |
| `Change_Date`     | DATE     | `Change_Date`               | DATE               | Date of change                               |     | FK to `Dim_Time`           |
| **Technical Fields (for CDC + audit)** |          |                         |                    |                                              |     |                            |
|                   |          | `cdc_change_type`           | STRING             | `'cdc_insert'` only                          |     | CDC 1.1 logic               |
|                   |          | `cdc_index`                 | INT                | Row index if needed                          |     | Optional                   |
|                   |          | `scd_change_timestamp`      | TIMESTAMP          | Record ingestion time                        |     | Audit trace                 |
|                   |          | `ds_partition_date`         | DATE               | Partition date                               |     | Required                    |

---

### ✅ Notes

- This is a **CDC Type 1.1** table → **append-only** with no updates or deletes  
- `created_at` and `updated_at` are **not required** and excluded from schema  
- Enables **efficient enrichment joins** and **KYC field-level auditing**  
- Can be joined with `Dim_Customer` to trace changes across segments  
- Can be filtered on `Change_Type` to model volatility of customer behavior  
- Ideal for feeding lineage dashboards, rollback tools, or case investigation layers