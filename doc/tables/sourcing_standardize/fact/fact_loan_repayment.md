## 📜 Table: Fact_Loan_Repayment

This table stores all loan repayment events made by customers. It contains both principal and interest components, remaining balance, and repayment method. It is designed to support loan lifecycle tracking, credit exposure analysis, and behavioral anomaly detection.

- **Type**: Fact  
- **CDC Type**: `1.1`  
- **Writer Type**: `factAppend`  
- **Primary Key**: Composite – `(Loan_ID, Repayment_Date)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Append-only transactional fact for capturing loan repayment activities, used in cash flow tracking and AML repayment irregularity scenarios.

---

### 🔗 Foreign Keys and Relationships:

| Column         | Referenced Table  | Description                  |
|----------------|-------------------|------------------------------|
| `Customer_ID`  | `Dim_Customer`    | The borrower                 |
| `Loan_ID`      | `Dim_Loan`        | Loan contract (if modeled)   |

---

### 📊 Key Columns:

| Raw Column Name       | Raw Type | Standardized Column Name   | Standardized Type | Description                                         | PK  | Note                      |
|------------------------|----------|-----------------------------|--------------------|-----------------------------------------------------|-----|---------------------------|
| `Loan_ID`              | VARCHAR  | `Loan_ID`                   | VARCHAR            | Unique identifier for the loan                     | ✅  | Composite primary key     |
| `Customer_ID`          | VARCHAR  | `Customer_ID`               | VARCHAR            | Borrower linked to repayment                       |     | FK to `Dim_Customer`      |
| `Repayment_Date`       | DATE     | `Repayment_Date`            | DATE               | Date of the repayment                              | ✅  | Partition source          |
| `Repayment_Amount`     | DECIMAL  | `Repayment_Amount`          | DECIMAL            | Total repayment amount (principal + interest)      |     | Input to AML logic        |
| `Principal_Component`  | DECIMAL  | `Principal_Component`       | DECIMAL            | Portion of repayment towards principal             |     |                           |
| `Interest_Component`   | DECIMAL  | `Interest_Component`        | DECIMAL            | Portion paid as interest                           |     |                           |
| `Repayment_Method`     | VARCHAR  | `Repayment_Method`          | VARCHAR            | Channel or method used (e.g., Auto, Cash, IBFT)    |     |                           |
| `Remaining_Balance`    | DECIMAL  | `Remaining_Balance`         | DECIMAL            | Remaining principal after this repayment           |     | Useful for closure logic  |
| *(N/A)*                | *(N/A)*  | `f_sudden_loan_closure_flag`| BOOLEAN            | TRUE if full repayment made + income mismatch      |     | AML scenario flag         |
| *(N/A)*               | *(N/A)*  | `f_early_full_repayment_flag` | BOOLEAN           | TRUE if loan is fully repaid ≥30 days before maturity without clear income justification |     | AML scenario flag         |
---

### 🧪 Technical Fields (Standardize for Insight):

| Column Name           | Type       | Description |
|------------------------|------------|-------------|
| `cdc_change_type`      | STRING     | Always `'cdc_insert'` (CDC 1.1) |
| `cdc_index`            | LONG       | Ingestion order index           |
| `scd_change_timestamp` | TIMESTAMP  | Load timestamp into data lake  |
| `ds_partition_date`    | DATE       | Usually same as `Repayment_Date` |

---

### 🚩 Related AML Scenarios (Standardize → Insight)

| AML Scenario Name                     | Flag at Standardize             | Used in Insight |
|--------------------------------------|----------------------------------|------------------|
| Sudden Debt Repayment Beyond Income  | `f_sudden_loan_closure_flag`     | ✅ Yes           |
| Early Loan Closure with Unexplained Funds | `f_early_full_repayment_flag` | ✅ Yes |

---

### 🧠 Flag Logic Definitions

| Flag Name                     | Type    | Logic                                                                                 |
|-------------------------------|---------|----------------------------------------------------------------------------------------|
| `f_sudden_loan_closure_flag`  | BOOLEAN | TRUE if repayment amount ≥ full remaining balance AND monthly income < 10M VND        |
| `f_early_full_repayment_flag` | BOOLEAN | TRUE if `Remaining_Balance = 0` and `Repayment_Date` is ≥30 days before expected maturity, and customer shows no significant income increase |

> 💡 Requires joining with `Fact_Customer_Income` to determine average monthly income in the same timeframe.

---

### ✅ Notes:
- Repayment closure patterns outside of income capability are common laundering behavior
- Can be extended to track early closure (maturity comparison from `Dim_Loan` or `Fact_Deposit`)
- Useful for wealth profiling, income deviation, and risk scoring