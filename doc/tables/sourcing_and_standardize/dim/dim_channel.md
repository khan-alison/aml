## 📜 Table: Dim_Channel

This dimension defines all banking service channels through which transactions or services are delivered, including digital and non-digital mediums. It supports downstream reporting, segmentation, and AML risk profiling.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd2`  
- **Primary Key**: `Channel_ID`  
- **Partitioned By**: *(N/A)*  
- **Description**: Classifies customer interaction channels such as Mobile Banking, Branch, ATM, etc., and flags whether the channel is digital.

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Channel     | Raw Type | Standardized/Dim_Channel  | Standardized Type | Description                                 | PK  | Note                    |
|---------------------|----------|----------------------------|--------------------|---------------------------------------------|-----|-------------------------|
| `Channel_ID`        | VARCHAR  | `Channel_ID`               | VARCHAR            | Unique identifier for the channel           | ✅  | Primary key             |
| `Channel_Code`      | VARCHAR  | `Channel_Code`             | VARCHAR            | System or internal code                     |     | Used in joins           |
| `Channel_Name`      | VARCHAR  | `Channel_Name`             | VARCHAR            | Readable name for the channel               |     | UI/display name         |
| `Digital_Flag`      | BOOLEAN  | `Digital_Flag`             | BOOLEAN            | TRUE = digital channel (e.g., online, app)  |     | Digital classification  |
| `created_at`        | TIMESTAMP| `created_at`               | TIMESTAMP          | First creation timestamp in source          |     | From source (CDC 1.3)   |
| `updated_at`        | TIMESTAMP| `updated_at`               | TIMESTAMP          | Last update timestamp in source             |     | From source (CDC 1.3)   |
| **Technical Fields (for CDC + audit)** |          |                    |                    |                                             |     |                         |
|                     |          | `scd_change_type`          | STRING             | `'cdc_insert'`, `'cdc_update'`, `'cdc_delete'` |     | SCD2 logic              |
|                     |          | `cdc_index`                | INT                | Change sequence index                       |     | Optional                |
|                     |          | `scd_change_timestamp`     | TIMESTAMP          | Timestamp of record update/load             |     | Technical field          |
|                     |          | `dtf_start_date`           | DATE               | Start of current version (SCD2)             |     | Technical field          |
|                     |          | `dtf_end_date`             | DATE               | End of version validity                     |     | Technical field          |
|                     |          | `dtf_current_flag`         | BOOLEAN            | TRUE = currently valid version              |     | Technical field          |

---

### ✅ Notes

- Helps in channel usage analytics, fraud monitoring by entry point, and risk-based segmentation  
- Commonly joins with `Fact_Transaction`, `Fact_Card_Transaction`, and alert triggers