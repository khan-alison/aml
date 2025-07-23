## 📜 Table: Dim_Country

This dimension provides the reference list of countries used throughout the AML system, including ISO codes, names, and risk classification levels. It supports geolocation, jurisdictional risk modeling, and cross-border rule enforcement.

- **Type**: Dimension  
- **CDC Type**: `1.1`  
- **Writer Type**: `scd1`  
- **Primary Key**: `Country_Code` (from source)  
- **Partitioned By**: `ds_partition_date` (string)  
- **Snapshot Strategy**: Not applicable – overwrite only (SCD1)

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Country | Raw Type  | PK  | Standardized/Dim_Country | Standardized Type | Description                                         | Value of Technical Field       | Note                      |
|-----------------|-----------|-----|----------------------------|--------------------|-----------------------------------------------------|-------------------------------|---------------------------|
| `Country_Code`  | STRING    | ✅  | `Country_Code`            | STRING             | ISO code or internal code identifying the country   |                               | Natural key from source   |
| `Country_Name`  | STRING    |     | `Country_Name`            | STRING             | Official name of the country                        |                               |                           |
| `Region`        | STRING    |     | `Region`                  | STRING             | Continent or global region                          |                               | Optional grouping         |
| `Is_High_Risk`  | BOOLEAN   |     | `Is_High_Risk`            | BOOLEAN            | TRUE if classified as high-risk jurisdiction        |                               | Used in AML rule filters  |
| `created_at`    | TIMESTAMP |     | `created_at`              | TIMESTAMP          | First seen in source                                | From source                   |                           |
| `updated_at`    | TIMESTAMP |     | `updated_at`              | TIMESTAMP          | Last updated from source                            | From source                   |                           |
| **Technical Fields** |      |     |                            |                    |                                                     |                               |                           |
|                 |           |     | `ds_key`                  | STRING             | Surrogate primary key for standardized zone         | `Country_Code`                | Required in DWH           |
|                 |           |     | `cdc_index`               | INT                | Current record flag (always 1 in SCD1)              | `1`                          |                           |
|                 |           |     | `cdc_change_type`         | STRING             | CDC event type                                      | `'cdc_insert'`               | Insert-only               |
|                 |           |     | `scd_change_timestamp`    | TIMESTAMP          | Processing timestamp                                | `updated_at` or job time     |                           |
|                 |           |     | `ds_partition_date`       | STRING             | Partition column (`yyyy-MM-dd`)                     | Job run date                 | Required                  |

---

### ✅ Business Use Cases

- Support AML rules involving high-risk or sanctioned countries  
- Enrich transactions and customer profiles with regional metadata  
- Enable country-level aggregation for reporting and dashboards  
- Power geo-based thresholds, limits, and scoring models  