## 📜 Table: Fact_Collateral_Assignment

This table stores the association between loan accounts and pledged collaterals. It captures when a customer pledges an asset, its value, and resulting Loan-to-Value (LTV) ratio. The data supports collateral monitoring, loan risk evaluation, and AML risk detection.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factUpsert`  
- **Primary Key**: Composite – `(Loan_ID, Collateral_ID)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Tracks collaterals pledged for loans, including valuation and customer profile at time of assignment.

---

### 🔗 Foreign Keys and Relationships:

| Column          | Referenced Table      | Description                              |
| --------------- | --------------------- | ---------------------------------------- |
| `Loan_ID`       | `Fact_Loan_Repayment` | Loan to which the collateral is assigned |
| `Collateral_ID` | `Dim_Asset`           | The pledged asset                        |
| `Customer_ID`   | `Dim_Customer`        | Owner of the collateral                  |
| `Currency`      | `Dim_Currency`        | Currency of valuation                    |

---

### 📊 Key Columns (Standardize)

| Raw Column Name    | Raw Type | Standardized Column Name     | Standardized Type | Description                                         | PK  | Note                    |
| ------------------ | -------- | ---------------------------- | ----------------- | --------------------------------------------------- | --- | ----------------------- |
| `Loan_ID`          | VARCHAR  | `Loan_ID`                    | VARCHAR           | Associated loan account                             | ✅  |                         |
| `Collateral_ID`    | VARCHAR  | `Collateral_ID`              | VARCHAR           | Asset pledged as collateral                         | ✅  |                         |
| `Customer_ID`      | VARCHAR  | `Customer_ID`                | VARCHAR           | Owner of collateral                                 |     | FK to `Dim_Customer`    |
| `Assigned_Date`    | DATE     | `Assigned_Date`              | DATE              | When the collateral was assigned                    |     | Used in lifecycle logic |
| `Collateral_Value` | DECIMAL  | `Collateral_Value`           | DECIMAL           | Valuation at time of assignment                     |     |                         |
| `Current_Value`    | DECIMAL  | `Current_Value`              | DECIMAL           | Latest known market value                           |     | Optional for monitoring |
| `LTV`              | DECIMAL  | `LTV`                        | DECIMAL           | Loan-to-Value ratio                                 |     | Derived or ingested     |
| `Currency`         | VARCHAR  | `Currency`                   | VARCHAR           | Currency used in valuation                          |     |                         |
| *(N/A)*            | *(N/A)*  | `f_collateral_mismatch_flag` | BOOLEAN           | TRUE if asset value > 5B VND but income < threshold |     | AML scenario flag       |
|Technical Fields (for CDC + audit)|
| *(N/A)*               | *(N/A)*   | `cdc_change_type`            | STRING             | `'cdc_insert'` or `'cdc_update'`          |     | CDC 1.3 logic  |
| *(N/A)*               | *(N/A)*   | `cdc_index`                  | LONG               | Monotonic ingestion checkpoint             |     |                |
| *(N/A)*               | *(N/A)*   | `scd_change_timestamp`       | TIMESTAMP          | Time record entered data lake              |     |                |
| *(N/A)*               | *(N/A)*   | `created_at`                 | TIMESTAMP          | First time seen                            |     |                |
| *(N/A)*               | *(N/A)*   | `updated_at`                 | TIMESTAMP          | Time last updated                          |     |                |
| *(N/A)*               | *(N/A)*   | `ds_partition_date`          | DATE               | Partition date (based on `Assigned_Date`)  |     |                |

---

### 🚩 Related AML Scenarios (Standardize → Insight)

| AML Scenario Name                         | Flag at Standardize          | Used in Insight |
| ----------------------------------------- | ---------------------------- | --------------- |
| Collateral Mismatch with Customer Profile | `f_collateral_mismatch_flag` | ✅ Yes          |

---

### 🧠 Flag Logic Definitions

| Flag Name                    | Type    | Logic                                                                        |
| ---------------------------- | ------- | ---------------------------------------------------------------------------- |
| `f_collateral_mismatch_flag` | BOOLEAN | TRUE if `Collateral_Value` > 5,000,000,000 AND `Customer_Income` < 10M/month |

---

### ✅ Notes

- Assumes income profile is sourced from `Fact_Customer_Income` (joined via `Customer_ID`, `Month`)
- Can identify shell individuals or money mules pledging high-value assets
- Used to validate declared wealth vs pledged security