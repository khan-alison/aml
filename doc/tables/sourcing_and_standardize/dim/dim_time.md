## 📜 Table: Dim_Time

This is a static dimension used to represent calendar time. It includes days, months, quarters, and years, and is used for partitioning, time-based aggregation, and reporting filters across the AML platform.

- **Type**: Dimension  
- **CDC Type**: `0.0`  
- **Writer Type**: `static`  
- **Primary Key**: `Date_Key` (from source)  
- **Partitioned By**: `ds_partition_date` (string)  
- **Snapshot Strategy**: Not applicable – static reference table

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Time   | Raw Type  | PK  | Standardized/Dim_Time | Standardized Type | Description                                   | Value of Technical Field       | Note                        |
|----------------|-----------|-----|-------------------------|--------------------|-----------------------------------------------|-------------------------------|-----------------------------|
| `Date_Key`      | STRING    | ✅  | `Date_Key`              | STRING             | Unique date key in `yyyyMMdd` format           |                               | Natural key (e.g., 20240723)|
| `Date`          | DATE      |     | `Date`                  | DATE               | Actual date                                    |                               |                            |
| `Day`           | INT       |     | `Day`                   | INT                | Day of the month                               |                               |                            |
| `Month`         | INT       |     | `Month`                 | INT                | Month number (1–12)                            |                               |                            |
| `Quarter`       | STRING    |     | `Quarter`               | STRING             | Quarter name (e.g., Q1, Q2)                    |                               |                            |
| `Year`          | INT       |     | `Year`                  | INT                | Calendar year                                  |                               |                            |
| `Weekday_Name`  | STRING    |     | `Weekday_Name`          | STRING             | Day of the week (e.g., Monday)                 |                               |                            |
| `Is_Weekend`    | BOOLEAN   |     | `Is_Weekend`            | BOOLEAN            | TRUE if Saturday/Sunday                        |                               |                            |
| **Technical Fields** |       |     |                         |                    |                                               |                               |                            |
|                |           |     | `ds_key`                | STRING             | Surrogate primary key                          | `Date_Key`                   | Required in DWH             |
|                |           |     | `cdc_index`             | INT                | CDC flag (static = always 1)                   | `1`                          |                            |
|                |           |     | `cdc_change_type`       | STRING             | CDC event type                                 | `'cdc_insert'`               | Static load                 |
|                |           |     | `scd_change_timestamp`  | TIMESTAMP          | Timestamp of static load                       | Job run time                 |                            |
|                |           |     | `ds_partition_date`     | STRING             | Partition column (`yyyy-MM-dd`)                | Job run date                 | Required                    |

---

### ✅ Business Use Cases

- Support partitioning across fact tables  
- Enable consistent time-based grouping and rollups  
- Power calendar filters and time intelligence in reports  
- Required for joins with all transactional data  
