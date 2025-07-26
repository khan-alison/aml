## 📜 Table: Dim_Channel

This dimension defines the available banking channels such as online, ATM, branch, or mobile. It is used to enrich transactions, detect channel-specific anomalies, and support channel-based reporting and segmentation.

- **Type**: Dimension  
- **CDC Type**: `1.1`  
- **Writer Type**: `scd1`  
- **Primary Key**: `Channel_Code` (from source)  
- **Partitioned By**: `ds_partition_date` (string)  
- **Snapshot Strategy**: Not applicable – overwrite-only (SCD1)

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Channel | Raw Type  | PK  | Standardized/Dim_Channel | Standardized Type | Description                                     | Value of Technical Field       | Note                    |
|------------------|-----------|-----|----------------------------|--------------------|-------------------------------------------------|-------------------------------|-------------------------|
| `Channel_Code`    | STRING    | ✅  | `Channel_Code`            | STRING             | Unique code for the banking channel             |                               | Natural key from source |
| `Channel_Name`    | STRING    |     | `Channel_Name`            | STRING             | Human-readable channel label                    |                               |                         |
| `Is_Active`       | BOOLEAN   |     | `Is_Active`               | BOOLEAN            | Whether this channel is currently in use        |                               | Default = TRUE          |
| `created_at`      | TIMESTAMP |     | `created_at`              | TIMESTAMP          | First seen in source                            | From source                   |                         |
| `updated_at`      | TIMESTAMP |     | `updated_at`              | TIMESTAMP          | Last update in source                           | From source                   |                         |
| **Technical Fields** |       |     |                            |                    |                                                 |                               |                         |
|                   |           |     | `ds_key`                  | STRING             | Surrogate primary key in standardized zone      | `Channel_Code`                | Required in DWH         |
|                   |           |     | `cdc_index`               | INT                | CDC flag (always 1 for SCD1)                    | `1`                          |                         |
|                   |           |     | `cdc_change_type`         | STRING             | CDC event type                                  | `'cdc_insert'`               | Insert-only             |
|                   |           |     | `scd_change_timestamp`    | TIMESTAMP          | Processing timestamp                            | `updated_at` or job time     |                         |
|                   |           |     | `ds_partition_date`       | STRING             | Partition column in format `yyyy-MM-dd`         | Job run date                 | Required                |

---

### ✅ Business Use Cases

- Enrich transactions with originating channel metadata  
- Detect anomalies in channel usage (e.g., high-risk transfers via ATM)  
- Support channel-based segmentation, limits, and policy rules  
- Feed analytics dashboards and model features by channel  