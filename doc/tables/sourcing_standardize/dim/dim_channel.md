## 📜 Table: Dim_Channel

This dimension defines all banking service channels through which transactions or services are delivered, including digital and non-digital mediums. It supports downstream reporting, segmentation, and AML risk profiling.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd2`  
- **Primary Key**: `Channel_ID`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Classifies customer interaction channels such as Mobile Banking, Branch, ATM, etc., and flags whether the channel is digital.

---

### 📊 Key Columns:

| Raw Column Name     | Raw Type | Standardized Column Name | Standardized Type | Description                                | PK  | Note         |
|----------------------|----------|---------------------------|--------------------|--------------------------------------------|-----|--------------|
| `Channel_ID`         | VARCHAR  | `Channel_ID`              | VARCHAR            | Unique identifier for the channel          | ✅  | Primary key  |
| `Channel_Code`       | VARCHAR  | `Channel_Code`            | VARCHAR            | System or internal code                    |     | Used in joins |
| `Channel_Name`       | VARCHAR  | `Channel_Name`            | VARCHAR            | Readable name for the channel              |     | UI/display    |
| `Digital_Flag`       | BOOLEAN  | `Digital_Flag`            | BOOLEAN            | TRUE = digital channel (e.g., online, app) |     | Classification |

---

### 🧪 Technical Fields (for SCD2 tracking):

| Field Name            | Type       | Description                                   |
|------------------------|------------|-----------------------------------------------|
| `scd_change_type`      | STRING     | `'cdc_insert'`, `'cdc_update'`, `'cdc_delete'`|
| `cdc_index`            | INT        | Change sequence index                         |
| `scd_change_timestamp` | TIMESTAMP  | Timestamp of record update/load               |
| `ds_partition_date`    | DATE       | Partitioning column                           |
| `created_at`           | TIMESTAMP  | First creation timestamp                      |
| `updated_at`           | TIMESTAMP  | Most recent update timestamp                  |
| `dtf_start_date`       | DATE       | Start of current version (SCD2)               |
| `dtf_end_date`         | DATE       | End of version                                |
| `dtf_current_flag`     | BOOLEAN    | TRUE = active version                         |

---

### ✅ Notes:
- Helps in channel usage analytics, fraud monitoring by entry point, and risk-based segmentation
- Commonly joins with `Fact_Transaction`, `Fact_Card_Transaction`, and alert triggers
