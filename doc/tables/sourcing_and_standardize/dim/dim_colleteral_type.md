## 📜 Table: Dim_Collateral_Type

This dimension provides a reference list of collateral categories such as real estate, vehicles, cash, and securities. It supports risk assessment, regulatory capital computation, and enrichment of pledged asset data.

- **Type**: Dimension  
- **CDC Type**: `1.1`  
- **Writer Type**: `scd1`  
- **Primary Key**: `Collateral_Type_Code` (from source)  
- **Partitioned By**: `ds_partition_date` (string)  
- **Snapshot Strategy**: Not applicable – overwrite only (SCD1)

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Collateral_Type | Raw Type  | PK  | Standardized/Dim_Collateral_Type | Standardized Type | Description                                          | Value of Technical Field       | Note                        |
|--------------------------|-----------|-----|-----------------------------------|--------------------|------------------------------------------------------|-------------------------------|-----------------------------|
| `Collateral_Type_Code`   | STRING    | ✅  | `Collateral_Type_Code`            | STRING             | Unique code for collateral classification           |                               | Natural key from source     |
| `Collateral_Type_Name`   | STRING    |     | `Collateral_Type_Name`            | STRING             | Descriptive label of the collateral type            |                               |                             |
| `Risk_Weight`            | DECIMAL   |     | `Risk_Weight`                     | DECIMAL(5,2)       | Regulatory weight for capital/risk calculations     |                               | Optional                    |
| `Is_Active`              | BOOLEAN   |     | `Is_Active`                       | BOOLEAN            | Whether the type is currently valid                 |                               | Used for filtering          |
| `created_at`             | TIMESTAMP |     | `created_at`                      | TIMESTAMP          | Timestamp of initial load from source               | From source                   |                             |
| `updated_at`             | TIMESTAMP |     | `updated_at`                      | TIMESTAMP          | Timestamp of latest update                          | From source                   |                             |
| **Technical Fields**     |           |     |                                   |                    |                                                      |                               |                             |
|                          |           |     | `ds_key`                          | STRING             | Surrogate key in standardized zone                  | `Collateral_Type_Code`        | Required in DWH             |
|                          |           |     | `cdc_index`                       | INT                | Current record flag (always 1 in SCD1)              | `1`                           |                             |
|                          |           |     | `cdc_change_type`                 | STRING             | CDC event type (insert only)                        | `'cdc_insert'`                |                             |
|                          |           |     | `scd_change_timestamp`            | TIMESTAMP          | Snapshot or change time                             | `updated_at` or job time      |                             |
|                          |           |     | `ds_partition_date`               | STRING             | Partition column (`yyyy-MM-dd`)                     | Job run date                  | Required                    |

---

### ✅ Business Use Cases

- Enable standardization of pledged asset types across systems  
- Support credit and AML models involving risk-weighted collateral  
- Enrich transactional and portfolio data with type-level metadata  
- Feed filtering logic for dashboards and regulatory reports  