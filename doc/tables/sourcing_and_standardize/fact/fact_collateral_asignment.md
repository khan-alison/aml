## 📜 Table: Fact_Collateral_Assignment

This table records the assignment of collaterals to loans. It contains original and current collateral values, linkage to the loan and customer, and calculated Loan-to-Value (LTV). Useful in credit risk modeling and secured lending compliance.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factUpsert`  
- **Primary Key**: Composite key – `(Loan_ID, Collateral_ID, Assigned_Date)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Captures the value and relationship of collaterals assigned to loans at a specific time.

---

### 🔗 Foreign Keys and Relationships:

| Column           | Referenced Table       | Description |
|------------------|------------------------|-------------|
| `Loan_ID`        | `Dim_Loan`             | Loan to which collateral is assigned  |
| `Collateral_ID`  | `Dim_Collateral`       | Collateral asset reference            |
| `Customer_ID`    | `Dim_Customer`         | Customer owning the collateral        |
| `Assigned_Date`  | `Dim_Time`             | Date of assignment                    |

---

### 📊 Key Columns:

| Raw Column Name     | Raw Type | Standardized Column Name | Standardized Type | Description                                | PK  | Note                     |
|---------------------|----------|---------------------------|--------------------|--------------------------------------------|-----|--------------------------|
| `Loan_ID`           | VARCHAR  | `Loan_ID`                 | VARCHAR            | Loan ID associated with collateral         | ✅  | FK to `Dim_Loan`         |
| `Collateral_ID`     | VARCHAR  | `Collateral_ID`           | VARCHAR            | Assigned collateral asset ID               | ✅  | FK to `Dim_Collateral`   |
| `Customer_ID`       | VARCHAR  | `Customer_ID`             | VARCHAR            | Customer tied to loan and collateral       |     | FK to `Dim_Customer`     |
| `Assigned_Date`     | DATE     | `Assigned_Date`           | DATE               | Assignment date of collateral              | ✅  | FK to `Dim_Time`         |
| `Collateral_Value`  | DECIMAL  | `Collateral_Value`        | DECIMAL            | Value at time of assignment                |     |                          |
| `Current_Value`     | DECIMAL  | `Current_Value`           | DECIMAL            | Most recent collateral value               |     |                          |
| `LTV`               | DECIMAL  | `LTV`                     | DECIMAL            | Loan-to-Value ratio                        |     | Derived metric           |
| `Currency`          | VARCHAR  | `Currency`                | VARCHAR            | Currency of the collateral valuation       |     |                          |

---

### 🧪 Technical Fields (for CDC + audit):

| Raw Column Name        | Raw Type | Standardized Column Name | Standardized Type | Description                                  | PK  | Note |
|------------------------|----------|---------------------------|--------------------|----------------------------------------------|-----|------|
| `cdc_change_type`      | STRING   | `cdc_change_type`         | STRING             | `'cdc_insert'` or `'cdc_update'`             |     | CDC 1.3 logic           |
| `cdc_index`            | INT      | `cdc_index`               | INT                | Sequence/order indicator                     |     | Optional                |
| `scd_change_timestamp` | TIMESTAMP| `scd_change_timestamp`    | TIMESTAMP          | Time record was processed                    |     |                          |
| `ds_partition_date`    | DATE     | `ds_partition_date`       | DATE               | Partitioning date (aligned with assignment)  |     |                          |
| `created_at`           | TIMESTAMP| `created_at`              | TIMESTAMP          | Insertion timestamp                          |     |                          |
| `updated_at`           | TIMESTAMP| `updated_at`              | TIMESTAMP          | Last update timestamp                        |     |                          |

---

### ✅ Notes:
- Captures both original and dynamic value of pledged collateral
- Supports credit risk LTV calculations and collateral risk monitoring
- Enables secured lending traceability per customer and loan
