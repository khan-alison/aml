## 📜 Table: Dim_Collateral_Type

This dimension defines categories of collateral assets pledged against loans. It includes type names, classifications, and liquidity scores, which are essential for loan underwriting, collateral valuation, and LTV/risk ratio computations.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd2`  
- **Primary Key**: `Collateral_Type_ID`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Classifies collateral types by category, liquidity, and acceptance eligibility for lending decisions.

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Collateral_Type   | Raw Type | Standardized/Dim_Collateral_Type | Standardized Type | Description                                               | PK  | Note                  |
|---------------------------|----------|----------------------------------|--------------------|-----------------------------------------------------------|-----|-----------------------|
| `Collateral_Type_ID`      | VARCHAR  | `Collateral_Type_ID`             | VARCHAR            | Unique identifier for each collateral type                | ✅  | Primary key           |
| `Name`                    | VARCHAR  | `Name`                           | VARCHAR            | Name of the collateral type (e.g., Real Estate, Bond)     |     | UI/display use         |
| `Category`                | VARCHAR  | `Category`                       | VARCHAR            | Grouping (e.g., MOVABLE, IMMOVABLE, FINANCIAL)            |     | Used in reports        |
| `Liquidity_Score`         | INT      | `Liquidity_Score`                | INT                | Score representing ease of liquidation (e.g., 1–10)       |     | Used in LTV logic      |
| `Accepted_For_Loan_Flag` | BOOLEAN  | `Accepted_For_Loan_Flag`        | BOOLEAN            | TRUE if eligible for securing loans                       |     | Business validation    |
|                           |          | `scd_change_type`               | STRING             | `'cdc_insert'`, `'cdc_update'`, `'cdc_delete'`            |     | SCD2 logic             |
|                           |          | `cdc_index`                     | INT                | Version tracking index                                    |     | Optional               |
|                           |          | `scd_change_timestamp`          | TIMESTAMP          | Timestamp of latest record update                         |     |                        |
|                           |          | `ds_partition_date`             | DATE               | Partition column                                          |     |                        |
|                           |          | `created_at`                    | TIMESTAMP          | Record creation timestamp                                 |     |                        |
|                           |          | `updated_at`                    | TIMESTAMP          | Last modified timestamp                                   |     |                        |
|                           |          | `dtf_start_date`                | DATE               | Start of version validity                                 |     |                        |
|                           |          | `dtf_end_date`                  | DATE               | End of version validity                                   |     |                        |
|                           |          | `dtf_current_flag`              | BOOLEAN            | TRUE if this is the active record                         |     |                        |

---

### ✅ Notes

- Joins with `Fact_Collateral_Assignment` and loan-level LTV computation  
- Helps differentiate secured vs. unsecured lending scenarios  
- Can be extended with regulatory collateral classifications (e.g., Basel III)