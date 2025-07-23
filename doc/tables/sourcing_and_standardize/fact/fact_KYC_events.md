## 📜 Table: Fact_KYC_Event

This fact table logs KYC-related events such as onboarding, periodic reviews, customer updates, and closures. Each row represents a distinct compliance action on a customer profile. The table is insert-only and used for traceability, monitoring, and escalation workflows.

- **Type**: Fact  
- **CDC Type**: `1.1`  
- **Writer Type**: `factAppend`  
- **Primary Key**: `KYC_Event_ID` (from source)  
- **Partitioned By**: `ds_partition_date` (string)  
- **Snapshot Strategy**: None – insert-only event log with no history

---

### 📊 Key Columns (Standardize)

| Raw/Fact_KYC_Event | Raw Type  | PK  | Standardized/Fact_KYC_Event | Standardized Type | Description                                                 | Value of Technical Field               | Note                           |
|--------------------|-----------|-----|------------------------------|--------------------|-------------------------------------------------------------|----------------------------------------|--------------------------------|
| `KYC_Event_ID`     | STRING    | ✅  | `KYC_Event_ID`               | STRING             | Unique identifier for the KYC event                         |                                        | Primary key, used for tracking |
| `Customer_ID`      | STRING    |     | `Customer_ID`                | STRING             | Customer associated with the event                          |                                        | FK to `Dim_Customer`           |
| `Event_Type`       | STRING    |     | `Event_Type`                 | STRING             | Onboarding, Review, Update, Closure                         |                                        | FK to `Dim_KYC_Event_Type`     |
| `Event_Date`       | DATE      |     | `Event_Date`                 | DATE               | Date when the event occurred                                |                                        | Business date                  |
| `Reviewer_ID`      | STRING    |     | `Reviewer_ID`                | STRING             | Internal reviewer or compliance officer                     |                                        | FK to `Dim_Employee` (optional)|
| `Review_Channel`   | STRING    |     | `Review_Channel`             | STRING             | Channel used (e.g., Online, Branch, Mobile)                 |                                        |                                |
| `Review_Result`    | STRING    |     | `Review_Result`              | STRING             | Outcome (e.g., Pass, Escalated, Rejected, Flagged)          |                                        |                                |
| `created_at`       | TIMESTAMP |     | `created_at`                 | TIMESTAMP          | Timestamp of event creation from source                     | From source                             |                                |
| **Technical Fields** |         |     |                              |                    |                                                             |                                        |                                |
|                    |           |     | `ds_key`                     | STRING             | Surrogate primary key for standardized zone                | `KYC_Event_ID`                          | Required in all fact tables    |
|                    |           |     | `cdc_index`                  | INT                | Current record flag in insert-only log                     | `1`                                     | Always 1 for factAppend        |
|                    |           |     | `cdc_change_type`            | STRING             | Type of CDC change event                                   | `'cdc_insert'`                          | Used for audit logic           |
|                    |           |     | `scd_change_timestamp`       | TIMESTAMP          | Timestamp of ETL ingestion                                 | `created_at`                            | From source or job timestamp   |
|                    |           |     | `ds_partition_date`          | STRING             | Partition column in format `yyyy-MM-dd`                    | `to_date(Event_Date)` or job run date  | Required for partitioning      |

---

### ✅ Business Use Cases

- Maintain full audit trail of all KYC actions  
- Detect customers with high KYC frequency or escalations  
- Analyze reviewer or channel-level performance  
- Trigger alerting and investigation workflows from flagged results  