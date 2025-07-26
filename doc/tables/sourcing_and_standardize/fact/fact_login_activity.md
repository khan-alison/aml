## 📜 Table: Fact_Login_Activity

This fact table captures login activity across all channels and devices. It supports anomaly detection, device profiling, and behavioral modeling for AML and fraud detection.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factAppend`  
- **Primary Key**: `ds_key`  
- **Partitioned By**: `ds_partition_date` (string)  
- **Snapshot Strategy**: *(Not applicable – fact tables do not have `_Hist`)*

---

### 📊 Key Columns (Standardize)

| Raw/Fact_Login_Activity | Raw Type  | PK (Source) | Standardized/Fact_Login_Activity | Standardized Type | Description                                                  | PK  | Value of Technical Field        | Note                            |
|--------------------------|-----------|-------------|-----------------------------------|--------------------|--------------------------------------------------------------|-----|----------------------------------|---------------------------------|
| `Login_ID`              | STRING    | ✅          | `Login_ID`                        | STRING             | Unique login event ID                                        |     |                                  | Natural key                     |
| `Customer_ID`           | STRING    |             | `Customer_ID`                     | STRING             | Identifier of the customer logging in                        |     |                                  | FK to `Dim_Customer`           |
| `Channel_Code`          | STRING    |             | `Channel_Code`                    | STRING             | Login channel (e.g., web, mobile, branch)                    |     |                                  | FK to `Dim_Channel`            |
| `Device_ID`             | STRING    |             | `Device_ID`                       | STRING             | Unique device fingerprint or ID used in session             |     |                                  | Used in device tracking         |
| `IP_Address`            | STRING    |             | `IP_Address`                      | STRING             | Source IP address of the login                               |     |                                  | Geo risk analytics              |
| `Geo_Location`          | STRING    |             | `Geo_Location`                    | STRING             | Approximate geolocation (e.g., city-country)                |     |                                  | Optional enrichment             |
| `Login_Timestamp`       | TIMESTAMP |             | `Login_Timestamp`                 | TIMESTAMP          | Time the login attempt occurred                              |     |                                  | Behavioral modeling             |
| `Login_Result`          | STRING    |             | `Login_Result`                    | STRING             | Outcome: success, failure, locked, etc.                      |     |                                  | ENUM                            |
| `created_at`            | TIMESTAMP |             | `created_at`                      | TIMESTAMP          | When the login record was created in source                  |     | From source                      |                                 |
| `updated_at`            | TIMESTAMP |             | `updated_at`                      | TIMESTAMP          | When the record was last updated in source                   |     | From source                      |                                 |
| **Technical Fields**    |           |             |                                   |                    |                                                              |     |                                  |                                 |
|                          |           |             | `ds_key`                          | STRING             | Surrogate primary key in standardized table                  | ✅  | `md5(Login_ID)`                 | Required for all fact tables     |
|                          |           |             | `cdc_change_type`                 | STRING             | CDC operation type                                           |     | `'cdc_insert'` / `'cdc_update'` | From CDC logic                  |
|                          |           |             | `cdc_index`                       | INT                | 1 = current, 0 = outdated                                    |     | `1`                             | For filtering current data       |
|                          |           |             | `scd_change_timestamp`            | TIMESTAMP          | Timestamp when change was processed                          |     | `updated_at` or job time        |                                 |
|                          |           |             | `ds_partition_date`               | STRING             | Partition column (`yyyy-MM-dd`)                              |     | Job run date                    | Required for partitioning        |

---

### ✅ Business Use Cases

- Detect abnormal logins (e.g., time, frequency, geo-distance, or channel)  
- Enrich fraud scoring models with device and IP behavior  
- Trigger rules for high-risk sessions or credentials compromise  
- Support investigations with session-level traceability  