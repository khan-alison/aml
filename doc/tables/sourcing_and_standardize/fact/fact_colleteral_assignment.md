## 📜 Table: Fact_Collateral_Assignment

This fact table links customers or accounts to pledged collateral assets. It tracks the presence and nature of secured assets backing loans or exposures. The table supports AML detection for asset shielding, circular pledging, and irregular collateral practices.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factUpsert`  
- **Primary Key**: `ds_key`  
- **Partitioned By**: `ds_partition_date`  
- **Snapshot Strategy**: *(Not applicable – factUpsert tables do not use `_Hist`)*

---

### 📊 Key Columns (Standardize)

| Raw/Fact_Collateral_Assignment | Raw Type  | PK (Source) | Standardized/Fact_Collateral_Assignment | Standardized Type | Description                                       | PK  | Value of Technical Field       | Note                           |
|--------------------------------|-----------|-------------|------------------------------------------|-------------------|---------------------------------------------------|-----|-------------------------------|--------------------------------|
| `Assignment_ID`               | STRING    | ✅          | `Assignment_ID`                         | STRING            | Unique ID for the collateral assignment           |     |                               | Natural key                    |
| `Customer_ID`                 | STRING    |             | `Customer_ID`                           | STRING            | Customer pledging the collateral                  |     |                               | FK to `Dim_Customer`           |
| `Collateral_ID`              | STRING    |             | `Collateral_ID`                         | STRING            | ID of the pledged asset                           |     |                               | FK to `Dim_Asset` or `Dim_Collateral_Type` |
| `Assignment_Date`            | DATE      |             | `Assignment_Date`                       | DATE              | Date when collateral was pledged                  |     |                               | Used in time-based logic       |
| `Release_Date`               | DATE      |             | `Release_Date`                          | DATE              | Date when collateral was released (nullable)      |     |                               | Used in duration calculations  |
| `Collateral_Type_Code`       | STRING    |             | `Collateral_Type_Code`                  | STRING            | Type of asset (e.g. Property, Shares, Vehicle)    |     |                               | FK to `Dim_Collateral_Type`    |
| `Valuation_Amount`           | DECIMAL   |             | `Valuation_Amount`                      | DECIMAL           | Assessed value of the pledged asset               |     |                               | Used in exposure analysis      |
| `Currency_Code`              | STRING    |             | `Currency_Code`                         | STRING            | Currency of the valuation                         |     |                               | FK to `Dim_Currency`           |
| `created_at`                 | TIMESTAMP |             | `created_at`                            | TIMESTAMP         | Record creation time in source                    |     | From source                   |                                |
| `updated_at`                 | TIMESTAMP |             | `updated_at`                            | TIMESTAMP         | Last update time in source                        |     | From source                   |                                |
|**Technical Field**|
|                              |           |             | `ds_key`                                | STRING            | Surrogate primary key                             | ✅  | `md5(Assignment_ID)`         |                                |
|                              |           |             | `cdc_change_type`                       | STRING            | Type of change event                              |     | `'cdc_insert'`, `'cdc_update'` | Required by CDC 1.3           |
|                              |           |             | `cdc_index`                             | INT               | 1 = current, 0 = outdated                         |     | `1`                          | Used for filtering             |
|                              |           |             | `scd_change_timestamp`                  | TIMESTAMP         | Change capture time                               |     | `updated_at` or job time     | Required for audit             |
|                              |           |             | `ds_partition_date`                     | STRING            | Partition column                                  |     | Job run date (`yyyy-MM-dd`)  | Required in all fact tables    |

---

### ✅ Business Use Cases

- Monitor secured lending arrangements across multiple entities  
- Detect suspicious patterns like repeated pledge and release cycles  
- Assess collateral adequacy and concentration risk  
- Support AML detection of asset fronting and obfuscation