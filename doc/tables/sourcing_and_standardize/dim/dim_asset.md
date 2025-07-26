## 📜 Table: Dim_Asset

This dimension defines registered or identifiable assets that may be owned, pledged, or linked to customers. Assets include real estate, vehicles, securities, or valuables. The table supports exposure analysis, ownership tracing, and collateral valuation.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Asset_ID` (from source)  
- **Partitioned By**: `ds_partition_date` (string, in `_Hist` table only)  
- **Snapshot Strategy**: SCD4a – current record in main table, full history in `_Hist`

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Asset     | Raw Type  | Standardized/Dim_Asset | Standardized Type | Standardized/Dim_Asset_Hist | Description                                      | PK  | Value of Technical Field      |
|-------------------|-----------|-------------------------|--------------------|------------------------------|--------------------------------------------------|-----|-------------------------------|
| `Asset_ID`        | STRING    | `Asset_ID`              | STRING             | `Asset_ID`                   | Unique identifier for the asset                  | ✅  | Primary key from source       |
| `Asset_Type`      | STRING    | `Asset_Type`            | STRING             | `Asset_Type`                 | Category (e.g., Property, Vehicle, etc.)         |     | ENUM or controlled list       |
| `Description`     | STRING    | `Description`           | STRING             | `Description`                | Human-readable description of the asset          |     | Optional                      |
| `Registration_No` | STRING    | `Registration_No`       | STRING             | `Registration_No`            | Official registration or license number          |     | Sensitive/PII field           |
| `Country_Code`    | STRING    | `Country_Code`          | STRING             | `Country_Code`               | Country of asset registration                    |     | FK to `Dim_Country`           |
| `Value_Estimate`  | DECIMAL   | `Value_Estimate`        | DECIMAL(18,2)      | `Value_Estimate`             | Estimated market value                           |     | Optional                      |
| `Currency_Code`   | STRING    | `Currency_Code`         | STRING             | `Currency_Code`              | Currency used for value                          |     | FK to `Dim_Currency`          |
| `Is_Active`       | BOOLEAN   | `Is_Active`             | BOOLEAN            | `Is_Active`                  | Asset still owned or usable                      |     | Used in filtering              |
| `created_at`      | TIMESTAMP | `created_at`            | TIMESTAMP          | `created_at`                 | First seen in source                             |     | From source                    |
| `updated_at`      | TIMESTAMP | `updated_at`            | TIMESTAMP          | `updated_at`                 | Last seen update in source                       |     | From source                    |
| `ds_key`          | STRING    | `ds_key`                | STRING             | `ds_key`                     | Surrogate key                                    | ✅  | `Asset_ID`                    |
| `cdc_index`       | INT       | `cdc_index`             | INT                | `cdc_index`                  | 1 = current, 0 = outdated                        |     | Used in SCD filtering          |
| `cdc_change_type` | STRING    | `cdc_change_type`       | STRING             | `cdc_change_type`            | Type of CDC event                                |     | `'cdc_insert'`, `'cdc_update'`|
| `scd_change_timestamp` | TIMESTAMP | `scd_change_timestamp` | TIMESTAMP        | `scd_change_timestamp`       | Change snapshot timestamp                        |     | `updated_at` or job time       |
| `dtf_start_date`  | DATE      | `dtf_start_date`        | DATE               | `dtf_start_date`             | Validity start date                              |     | From update or partition date  |
| `dtf_end_date`    | DATE      | `dtf_end_date`          | DATE               | `dtf_end_date`               | Validity end date                                |     | NULL if current                |
| `dtf_current_flag`| BOOLEAN   | `dtf_current_flag`      | BOOLEAN            | `dtf_current_flag`           | TRUE if currently valid                          |     | TRUE/FALSE                     |
| *(only in `_Hist`)* |         |                         |                    | `ds_partition_date`          | Partition column in `yyyy-MM-dd` format          |     | Used in `_Hist` only           |

---

### ✅ Business Use Cases

- Trace asset ownership for collateral or exposure analysis  
- Detect inconsistency between declared income and owned assets  
- Support AML investigations into luxury holdings or undeclared wealth  
- Feed asset-based risk scoring and pledge validation logic  