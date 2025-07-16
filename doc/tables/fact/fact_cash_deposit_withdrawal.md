## 📜 Table: Fact_Cash_Deposit_Withdrawal

This table captures transactions where customers deposit or withdraw physical cash from their accounts via various channels (e.g., branch, ATM). It includes metadata such as location, channel, and staff handling the transaction. Used for cash flow analysis, ATM activity trends, and operational risk monitoring.

- **Type**: Fact  
- **CDC Type**: `1.1`  
- **Writer Type**: `factAppend`  
- **Primary Key**: `Txn_ID`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Records all customer-initiated cash deposits and withdrawals. Each transaction is atomic and append-only.

---

### 🔗 Foreign Keys and Relationships:

| Column         | Referenced Table       | Description |
|----------------|------------------------|-------------|
| `Account_ID`   | `Dim_Account_Payment`  | Account linked to the cash transaction  |
| `Txn_Date`     | `Dim_Time`             | Date the transaction occurred  |
| `Channel`      | `Dim_Channel`          | Medium used for cash handling  |
| `Handled_By`   | `Dim_Employee`         | Employee/staff responsible (if branch-based) |

---

### 📊 Key Columns:

| Raw Column Name  | Raw Type | Standardized Column Name     | Standardized Type | Description                            | PK  | Note                    |
|------------------|----------|-------------------------------|--------------------|----------------------------------------|-----|-------------------------|
| `Txn_ID`         | VARCHAR  | `Txn_ID`                      | VARCHAR            | Unique ID of the cash transaction      | ✅  |                         |
| `Account_ID`     | VARCHAR  | `Account_ID`                  | VARCHAR            | Account impacted by the transaction    |     | FK to `Dim_Account_Payment` |
| `Txn_Date`       | DATE     | `Txn_Date`                    | DATE               | Date of the transaction                |     | FK to `Dim_Time`        |
| `Txn_Type`       | VARCHAR  | `Txn_Type`                    | VARCHAR            | Type: Deposit or Withdrawal            |     |                         |
| `Amount`         | DECIMAL  | `Amount`                      | DECIMAL            | Amount of cash deposited/withdrawn     |     |                         |
| `Channel`        | VARCHAR  | `Channel`                     | VARCHAR            | Source channel (ATM, Teller, etc.)     |     | FK to `Dim_Channel`     |
| `Location`       | VARCHAR  | `Location`                    | VARCHAR            | Physical location of transaction       |     |                         |
| `Handled_By`     | VARCHAR  | `Handled_By`                  | VARCHAR            | Employee/staff who processed it        |     | FK to `Dim_Employee`    |

---

### 🧪 Technical Fields (for CDC + audit):

| Raw Column Name        | Raw Type | Standardized Column Name | Standardized Type | Description                             | PK  | Note |
|------------------------|----------|---------------------------|--------------------|-----------------------------------------|-----|------|
| `cdc_change_type`      | STRING   | `cdc_change_type`         | STRING             | Change type from source (`insert`)      |     | Always `'cdc_insert'`   |
| `cdc_index`            | INT      | `cdc_index`               | INT                | Row sequence index                      |     | Optional                |
| `scd_change_timestamp` | TIMESTAMP| `scd_change_timestamp`    | TIMESTAMP          | Record load/ingestion timestamp         |     |                         |
| `ds_partition_date`    | DATE     | `ds_partition_date`       | DATE               | Partitioning date                       |     | Often equals `Txn_Date` |
| `created_at`           | TIMESTAMP| `created_at`              | TIMESTAMP          | Time record was first inserted          |     |                         |
| `updated_at`           | TIMESTAMP| `updated_at`              | TIMESTAMP          | Usually null in CDC 1.1                 |     |                         |

---

### ✅ Notes:
- Append-only ingestion pattern (CDC 1.1)
- Critical for tracking real cash movement in/out of customer accounts
- Useful for fraud analytics, vault capacity planning, and channel usage reporting

