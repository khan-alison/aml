## 📜 Table: Fact_Transaction

This is the core fact table capturing all monetary transactions across the bank’s channels. It includes domestic, cross-border, cash, internal, and interbank transactions. It supports high-volume analytics, alert triggers, and customer behavior modeling.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factAppend`  
- **Primary Key**: `Transaction_ID` (from source)  
- **Partitioned By**: `ds_partition_date` (string)  
- **Snapshot Strategy**: Not applicable – insert-only fact

---

### 📊 Key Columns (Standardize)

| Raw/Fact_Transaction | Raw Type  | PK  | Standardized/Fact_Transaction | Standardized Type | Description                                                | Value of Technical Field         | Note                            |
|----------------------|-----------|-----|-------------------------------|--------------------|------------------------------------------------------------|----------------------------------|---------------------------------|
| `Transaction_ID`     | STRING    | ✅  | `Transaction_ID`             | STRING             | Unique identifier of the transaction                       |                                  | Natural key from source         |
| `Customer_ID`        | STRING    |     | `Customer_ID`                | STRING             | Customer performing the transaction                        |                                  | FK to `Dim_Customer`           |
| `Account_ID`         | STRING    |     | `Account_ID`                 | STRING             | Account from which transaction originated                  |                                  | FK to `Dim_Account`            |
| `Transaction_Date`   | DATE      |     | `Transaction_Date`           | DATE               | Date when transaction occurred                             |                                  | Used for partitioning          |
| `Amount`             | DECIMAL   |     | `Amount`                     | DECIMAL(18,2)      | Amount of the transaction                                 |                                  | In original currency           |
| `Currency_Code`      | STRING    |     | `Currency_Code`              | STRING             | Currency used                                              |                                  | FK to `Dim_Currency`           |
| `Transaction_Type`   | STRING    |     | `Transaction_Type`           | STRING             | Type: cash withdrawal, transfer, etc.                      |                                  | FK to `Dim_Transaction_Type`   |
| `Channel_Code`       | STRING    |     | `Channel_Code`               | STRING             | Channel (ATM, online, etc.)                                |                                  | FK to `Dim_Channel`            |
| `Service_Type_Code`  | STRING    |     | `Service_Type_Code`          | STRING             | Internal classification (e.g., remittance, payment)        |                                  | FK to `Dim_Service_Type`       |
| `Counterparty_ID`    | STRING    |     | `Counterparty_ID`            | STRING             | External or internal counterparty ID                       |                                  | Optional                       |
| `Description`        | STRING    |     | `Description`                | STRING             | Free-text transaction note or reference                    |                                  | Optional                       |
| `created_at`         | TIMESTAMP |     | `created_at`                 | TIMESTAMP          | Time transaction was created                               | From source                      | Used for ds_partition_date     |
| `updated_at`         | TIMESTAMP |     | `updated_at`                 | TIMESTAMP          | Time transaction last updated                              | From source                      | Usually = created_at           |
| **Technical Fields** |           |     |                               |                    |                                                            |                                  |                                 |
|                      |           |     | `ds_key`                     | STRING             | Surrogate key for DWH (for joins/dedup)                    | `Transaction_ID`                 | Required                        |
|                      |           |     | `cdc_index`                  | INT                | CDC record version flag                                    | `1`                              | Always 1 in factAppend         |
|                      |           |     | `cdc_change_type`            | STRING             | CDC change indicator                                       | `'cdc_insert'`                  | Insert-only                     |
|                      |           |     | `scd_change_timestamp`       | TIMESTAMP          | Processing time or ingestion timestamp                     | `created_at` or job time         | For audit                       |
|                      |           |     | `ds_partition_date`          | STRING             | Partition column in format `yyyy-MM-dd`                    | From `Transaction_Date` or job   | Required                        |

---

### ✅ Business Use Cases

- Core input for AML rule detection and velocity modeling  
- Enables transaction volume, value, and frequency analysis  
- Joins with `Dim_Customer`, `Dim_Account`, `Dim_Channel`, and `Alert_Fact`  
- Powers dashboards, peer group comparisons, and scenario modeling  