## 📜 Table: Fact_Cash_Deposit_Withdrawal

This table captures all cash-based deposit and withdrawal transactions conducted by customers. It includes physical cash movement events at branches or ATMs, often targeted by money launderers for layering or smurfing activities.

- **Type**: Fact  
- **CDC Type**: `1.1`  
- **Writer Type**: `factAppend`  
- **Primary Key**: Composite – `(Txn_ID, ds_partition_date)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Captures physical cash movements from customer accounts, used to detect structuring, smurfing, and high-volume anonymous transactions.

---

### 📊 Key Columns (Standardize)

| Raw/Fact_Cash_Deposit_Withdrawal | Raw Type | Standardized/std_Cash_Deposit_Withdrawal | Standardized Type | Standardized/std_Cash_Deposit_Withdrawal_Hist | Description                                          | PK  | Note                         |
|----------------------------------|----------|-------------------------------------------|-------------------|--------------------------------------------------|------------------------------------------------------|-----|------------------------------|
| `Txn_ID`                         | VARCHAR  | `Txn_ID`                                  | VARCHAR           | `Txn_ID`                                        | Unique identifier for the transaction                | ✅  | Composite key with partition |
| `Account_ID`                     | VARCHAR  | `Account_ID`                              | VARCHAR           | `Account_ID`                                    | Account associated with the cash transaction         |     | FK to `Dim_Account`          |
| `Txn_Date`                       | DATE     | `Txn_Date`                                | DATE              | `Txn_Date`                                      | Date of transaction                                  |     | FK to `Dim_Time`             |
| `Txn_Type`                       | VARCHAR  | `Txn_Type`                                | VARCHAR           | `Txn_Type`                                      | DEPOSIT or WITHDRAWAL                                |     | AML logic input              |
| `Amount`                         | DECIMAL  | `Amount`                                  | DECIMAL           | `Amount`                                        | Amount of cash transacted                            |     |                              |
| `Channel`                        | VARCHAR  | `Channel`                                 | VARCHAR           | `Channel`                                       | ATM, BRANCH, etc.                                    |     | FK to `Dim_Channel`          |
| `Location`                       | VARCHAR  | `Location`                                | VARCHAR           | `Location`                                      | Branch or ATM location                               |     | Used in geo-analysis         |
| `Handled_By`                     | VARCHAR  | `Handled_By`                              | VARCHAR           | `Handled_By`                                    | Teller ID or device identifier                       |     | Optional audit trail         |
| *(Derived)*                      | *(N/A)*  | `f_structuring_flag`                      | BOOLEAN           | `f_structuring_flag`                            | TRUE if customer deposited >300M via small txns      |     | AML structuring scenario     |
|**Technical Fields (for CDC 1.1)**|          |                                           |                   |                                                  |                                                      |     |                              |
|                                  |          | `cdc_change_type`                         | STRING            | `cdc_change_type`                               | Always `'cdc_insert'` (append-only)                  |     | CDC 1.1 logic                 |
|                                  |          | `cdc_index`                               | LONG              | `cdc_index`                                     | Monotonic ingestion checkpoint                       |     | Required                     |
|                                  |          | `scd_change_timestamp`                    | TIMESTAMP         | `scd_change_timestamp`                          | Timestamp when record was loaded                     |     | Audit field                   |
|                                  |          |                                           |                   | `ds_partition_date`                             | Partition column (derived from `Txn_Date`)           | ✅  | Required for fact partition  |

---

### 🚩 Related AML Scenarios (Standardize → Insight)

| AML Scenario Name              | Flag at Standardize     | Used in Insight |
|-------------------------------|--------------------------|------------------|
| Structuring / Smurfing        | `f_structuring_flag`     | ✅ Yes           |

---

### 🧠 Flag Logic Definitions

| Flag Name             | Type    | Logic                                                                 |
|-----------------------|---------|-----------------------------------------------------------------------|
| `f_structuring_flag`  | BOOLEAN | TRUE if total DEPOSITs in 7 days > 300M VND and no single txn > 100M |

> 💡 Requires Spark window-based aggregation:
> Partition by `Customer_ID`, filter where `Txn_Type = 'DEPOSIT'`, and compute rolling 7-day sums.

---

### ✅ Notes

- Designed for detection of **layering and smurfing** via cash
- Leverages `Channel`, `Location`, `Handled_By` to trace behavioral or device anomalies
- Used in threshold violation monitoring and alert generation