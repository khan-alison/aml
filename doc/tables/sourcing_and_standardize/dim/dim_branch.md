## 📜 Table: Dim_Branch

This dimension stores the official bank branch directory, including unique codes, names, addresses, and operational status. It supports enrichment of customer, account, and transaction data, and enables regional analysis and regulatory reporting.

- **Type**: Dimension  
- **CDC Type**: `1.1`  
- **Writer Type**: `scd1`  
- **Primary Key**: `Branch_Code` (from source)  
- **Partitioned By**: `ds_partition_date` (string)  
- **Snapshot Strategy**: Not applicable – overwrite only (SCD1)

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Branch | Raw Type  | PK  | Standardized/Dim_Branch | Standardized Type | Description                                    | Value of Technical Field       | Note                    |
|----------------|-----------|-----|---------------------------|--------------------|------------------------------------------------|-------------------------------|-------------------------|
| `Branch_Code`  | STRING    | ✅  | `Branch_Code`            | STRING             | Unique branch code used across the bank        |                               | Natural key from source |
| `Branch_Name`  | STRING    |     | `Branch_Name`            | STRING             | Official name of the branch                    |                               |                         |
| `Region`       | STRING    |     | `Region`                 | STRING             | Geographic region of the branch                |                               | Optional                 |
| `Address`      | STRING    |     | `Address`                | STRING             | Physical address of the branch                 |                               |                         |
| `Is_Active`    | BOOLEAN   |     | `Is_Active`              | BOOLEAN            | Whether the branch is currently operational    |                               | Default = TRUE          |
| `created_at`   | TIMESTAMP |     | `created_at`             | TIMESTAMP          | Timestamp when the record was first seen       | From source                   |                         |
| `updated_at`   | TIMESTAMP |     | `updated_at`             | TIMESTAMP          | Timestamp of the last update from the source   | From source                   |                         |
| **Technical Fields** |     |     |                          |                    |                                                |                               |                         |
|                |           |     | `ds_key`                 | STRING             | Surrogate primary key for standardized zone    | `Branch_Code`                | Required in DWH         |
|                |           |     | `cdc_index`              | INT                | Current record flag                            | `1`                          | Always 1 in scd1         |
|                |           |     | `cdc_change_type`        | STRING             | CDC event type                                 | `'cdc_insert'`               | Insert-only              |
|                |           |     | `scd_change_timestamp`   | TIMESTAMP          | Processing time                                | `updated_at` or job timestamp |                         |
|                |           |     | `ds_partition_date`      | STRING             | Partition column (`yyyy-MM-dd`)                | Job run date                 | Required                 |

---

### ✅ Business Use Cases

- Enrich customer and account data with branch metadata  
- Segment accounts by region for performance and risk reporting  
- Identify inactive or closed branches for compliance analysis  
- Support location-based alerts and case assignment in AML systems  