## 📜 Table: Fact_Loan_Repayment

This table stores all loan repayment events made by customers. It contains both principal and interest components, remaining balance, and repayment method. It is designed to support loan lifecycle tracking, credit exposure analysis, and behavioral anomaly detection.

- **Type**: Fact  
- **CDC Type**: `1.1`  
- **Writer Type**: `factAppend`  
- **Primary Key**: Composite – `(Loan_ID, Repayment_Date)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Append-only transactional fact capturing loan repayment activities, used in cash flow tracking and AML repayment irregularity scenarios.

---

### 📊 Key Columns (Standardize)

| Raw/Fact_Loan_Repayment | Raw Type | Standardized/Fact_Loan_Repayment | Standardized Type | Description                                            | PK  | Note                          |
|--------------------------|----------|-----------------------------------|--------------------|--------------------------------------------------------|-----|-------------------------------|
| `Loan_ID`                | VARCHAR  | `Loan_ID`                         | VARCHAR            | Unique identifier for the loan                         | ✅  | Composite PK, FK to `Dim_Loan` |
| `Customer_ID`            | VARCHAR  | `Customer_ID`                     | VARCHAR            | Borrower linked to repayment                           |     | FK to `Dim_Customer`          |
| `Repayment_Date`         | DATE     | `Repayment_Date`                  | DATE               | Date of the repayment                                  | ✅  | Composite PK                  |
| `Repayment_Amount`       | DECIMAL  | `Repayment_Amount`                | DECIMAL            | Total repayment amount (principal + interest)          |     | Used in repayment ratio calc  |
| `Principal_Component`    | DECIMAL  | `Principal_Component`             | DECIMAL            | Portion toward loan principal                          |     |                               |
| `Interest_Component`     | DECIMAL  | `Interest_Component`              | DECIMAL            | Portion paid as interest                               |     |                               |
| `Repayment_Method`       | VARCHAR  | `Repayment_Method`                | VARCHAR            | Channel (e.g., Auto, Cash, IBFT)                       |     | Used for source traceability  |
| `Remaining_Balance`      | DECIMAL  | `Remaining_Balance`               | DECIMAL            | Outstanding principal after this repayment             |     | Used for early closure rules  |
| *(derived)*              | *(N/A)*  | `f_sudden_loan_closure_flag`      | BOOLEAN            | TRUE if full repayment made with low income            |     | AML flag                      |
| *(derived)*              | *(N/A)*  | `f_early_full_repayment_flag`     | BOOLEAN            | TRUE if loan fully repaid early with no justification  |     | AML flag                      |
|Technical Fields (Standardize)|
|                          |          | `cdc_change_type`                 | STRING             | Always `'cdc_insert'`                                  |     | CDC 1.1 logic                  |
|                          |          | `cdc_index`                       | LONG               | Ingestion checkpoint ID                                |     | Required for deduplication    |
|                          |          | `scd_change_timestamp`            | TIMESTAMP          | Time record was written to the lake                    |     |                               |
|                          |          | `ds_partition_date`               | DATE               | Usually equal to `Repayment_Date`                      |     | Partition column              |

---

### ✅ Notes

- CDC 1.1 ensures **append-only** logic — no updates or deletes  
- Used in scenarios like **early repayment with unknown funds**  
- Join with `Fact_Customer_Income` to compare against declared income  