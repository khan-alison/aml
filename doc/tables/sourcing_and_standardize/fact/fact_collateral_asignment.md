## 📜 Table: Fact_Collateral_Assignment

This table records the assignment of collaterals to loans. It contains original and current collateral values, linkage to the loan and customer, and calculated Loan-to-Value (LTV). Useful in credit risk modeling and secured lending compliance.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factUpsert`  
- **Primary Key**: Composite key – `(Loan_ID, Collateral_ID, Assigned_Date)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Captures the value and relationship of collaterals assigned to loans at a specific time.

---

### 📊 Key Columns (Standardize)

| Raw/Fact_Collateral_Assignment | Raw Type | Standardized/std_Collateral_Assignment | Standardized Type | Standardized/std_Collateral_Assignment_Hist | Description                                | PK  | Note                     |
|--------------------------------|----------|----------------------------------------|-------------------|---------------------------------------------|--------------------------------------------|-----|--------------------------|
| `Loan_ID`                      | VARCHAR  | `Loan_ID`                              | VARCHAR           | `Loan_ID`                                   | Loan ID associated with collateral         | ✅  | FK to `Dim_Loan`         |
| `Collateral_ID`                | VARCHAR  | `Collateral_ID`                        | VARCHAR           | `Collateral_ID`                             | Assigned collateral asset ID               | ✅  | FK to `Dim_Collateral`   |
| `Customer_ID`                  | VARCHAR  | `Customer_ID`                          | VARCHAR           | `Customer_ID`                               | Customer tied to loan and collateral       |     | FK to `Dim_Customer`     |
| `Assigned_Date`                | DATE     | `Assigned_Date`                        | DATE              | `Assigned_Date`                             | Assignment date of collateral              | ✅  | FK to `Dim_Time`         |
| `Collateral_Value`             | DECIMAL  | `Collateral_Value`                     | DECIMAL           | `Collateral_Value`                          | Value at time of assignment                |     |                          |
| `Current_Value`                | DECIMAL  | `Current_Value`                        | DECIMAL           | `Current_Value`                             | Most recent collateral value               |     |                          |
| `LTV`                          | DECIMAL  | `LTV`                                  | DECIMAL           | `LTV`                                       | Loan-to-Value ratio                        |     | Derived metric           |
| `Currency`                     | VARCHAR  | `Currency`                             | VARCHAR           | `Currency`                                  | Currency of the collateral valuation       |     |                          |
|**Technical Fields (for CDC 1.3)**|         |                                        |                   |                                             |                                            |     |                          |
|                                |          | `cdc_change_type`                      | STRING            | `cdc_change_type`                           | `'cdc_insert'` or `'cdc_update'`           |     | CDC 1.3 logic             |
|                                |          | `cdc_index`                            | INT               | `cdc_index`                                 | Sequence/order indicator                   |     | Optional                  |
|                                |          | `scd_change_timestamp`                 | TIMESTAMP         | `scd_change_timestamp`                      | Time record was processed                  |     | Audit field               |
|                                |          | `created_at`                           | TIMESTAMP         | `created_at`                                | Insertion timestamp                        |     | Required for CDC 1.3      |
|                                |          | `updated_at`                           | TIMESTAMP         | `updated_at`                                | Last update timestamp                      |     | Required for CDC 1.3      |
|                                |          |                                        |                   | `ds_partition_date`                         | Partitioning date (aligned with assignment)| ✅  | Required for performance  |

---

### ✅ Notes

- Captures both original and dynamic value of pledged collateral  
- Supports credit risk LTV calculations and collateral risk monitoring  
- Enables secured lending traceability per customer and loan  
- `ds_partition_date` typically aligns with `Assigned_Date` for optimal query filtering  