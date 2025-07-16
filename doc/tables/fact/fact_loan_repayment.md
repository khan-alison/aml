## 📜 Table: Fact_Loan_Repayment

This table is used to track detailed daily loan repayment activity for each loan held by a customer. It captures the total repayment amount made on a given day, how that amount is split into interest and principal, the repayment method used (e.g., auto-debit, manual transfer), and the remaining balance after the repayment. This enables financial institutions to monitor loan performance, assess payment behavior, and support delinquency analysis.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factUpsert`  
- **Primary Key**: Composite key – `(Loan_ID, Repayment_Date)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Captures daily loan repayment activities by customers, including amount, breakdown of principal and interest, and remaining balance. Each record reflects the latest status of a loan repayment on a given day.

---

### 🔗 Foreign Keys and Relationships:

| Column               | Referenced Table       | Description |
|----------------------|------------------------|-------------|
| `Loan_ID`            | `Dim_Loan`             | Loan reference key  |
| `Customer_ID`        | `Dim_Customer`         | Borrower making the repayment  |
| `Repayment_Method`   | `Dim_RepaymentMethod`  | Repayment method used  |
| `Repayment_Date`     | `Dim_Time`             | Date of repayment  |

---

### 📊 Key Columns:

| Column Name            | Description |
|-------------------------|-------------|
| `Loan_ID`              | Unique identifier for the loan  |
| `Customer_ID`          | Customer who made the repayment  |
| `Repayment_Date`       | Date of repayment transaction  |
| `Repayment_Amount`     | Total repayment amount on the day  |
| `Principal_Component`  | Portion of repayment applied to principal  |
| `Interest_Component`   | Portion of repayment applied to interest  |
| `Repayment_Method`     | Method used for repayment (e.g., Auto Debit, Cash)  |
| `Remaining_Balance`    | Outstanding balance after repayment  |

---

### 🧪 Technical Fields (for CDC + audit):

| Column Name           | Type       | Description |
|------------------------|------------|-------------|
| `cdc_change_type`      | STRING     | `'cdc_insert'` or `'cdc_update'` depending on change  |
| `cdc_index`            | LONG/INT   | Optional row index for tracking changes  |
| `scd_change_timestamp` | TIMESTAMP  | Ingestion or processing timestamp  |
| `ds_partition_date`    | DATE       | Partition date, typically equal to `Repayment_Date`  |
| `created_at`           | TIMESTAMP  | Record insertion time  |
| `updated_at`           | TIMESTAMP  | Time of latest update to the record  |

---

### ✅ Notes:
- Uses **CDC Type 1.3** for upsert logic
- Ensures only the most recent daily record is retained per loan
- Ideal for monitoring repayment behavior and calculating performance metrics
