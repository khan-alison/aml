## 📜 Table: Fact_Cash_Deposit_Withdrawal

This table captures all cash-based deposit and withdrawal transactions conducted by customers. It includes physical cash movement events at branches or ATMs, often targeted by money launderers for layering or smurfing activities.

- **Type**: Fact  
- **CDC Type**: `1.1`  
- **Writer Type**: `factAppend`  
- **Primary Key**: Composite – `(Txn_ID, ds_partition_date)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Captures physical cash movements from customer accounts, used to detect structuring, smurfing, and high-volume anonymous transactions.

---

### 🔗 Foreign Keys and Relationships:

| Column         | Referenced Table  | Description                  |
|----------------|-------------------|------------------------------|
| `Account_ID`   | `Dim_Account`     | Account involved in cash txn |
| `Channel`      | `Dim_Channel`     | Channel used (ATM, Branch)   |

---

### 📊 Key Columns:

| Raw Column Name  | Raw Type | Standardized Column Name   | Standardized Type | Description                                  | PK  | Note                     |
|------------------|----------|-----------------------------|--------------------|----------------------------------------------|-----|--------------------------|
| `Txn_ID`         | VARCHAR  | `Txn_ID`                    | VARCHAR            | Unique ID of the transaction                 | ✅  | Composite primary key    |
| `Account_ID`     | VARCHAR  | `Account_ID`                | VARCHAR            | Account associated with the transaction      |     | FK to `Dim_Account`      |
| `Txn_Date`       | DATE     | `Txn_Date`                  | DATE               | Date of transaction                          |     | Partitioning source      |
| `Txn_Type`       | VARCHAR  | `Txn_Type`                  | VARCHAR            | DEPOSIT or WITHDRAWAL                        |     | AML logic input          |
| `Amount`         | DECIMAL  | `Amount`                    | DECIMAL            | Cash amount                                  |     | Used in structuring rule |
| `Channel`        | VARCHAR  | `Channel`                   | VARCHAR            | ATM, BRANCH, etc.                            |     |                           |
| `Location`       | VARCHAR  | `Location`                  | VARCHAR            | Branch or ATM location                       |     | Geographic tracking       |
| `Handled_By`     | VARCHAR  | `Handled_By`                | VARCHAR            | Teller ID or device                          |     | Optional audit trail      |
| *(N/A)*          | *(N/A)*  | `f_structuring_flag`        | BOOLEAN            | TRUE if customer deposited >300M via small txns |  | AML scenario flag        |

---

### 🧪 Technical Fields (Standardize for Insight):

| Column Name           | Type       | Description |
|------------------------|------------|-------------|
| `cdc_change_type`      | STRING     | Always `'cdc_insert'` |
| `cdc_index`            | LONG       | Sequential ingest ID  |
| `scd_change_timestamp` | TIMESTAMP  | Load time             |
| `ds_partition_date`    | DATE       | Usually `Txn_Date`    |

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

> 💡 Requires window aggregation by `Customer_ID`, filter by `Txn_Type = 'DEPOSIT'`, and rolling sum logic.

---

### ✅ Notes:
- Applies primarily to **cash-based DEPOSITs**
- Often used by smurfing operations to avoid threshold detection
- Use with `Location`, `Channel`, and `Handled_By` for geographic or device-based analysis