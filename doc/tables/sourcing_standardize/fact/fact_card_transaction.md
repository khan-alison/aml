## 📜 Table: Fact_Card_Transaction

This table captures all credit/debit card transaction activity made by customers. Each row represents one transaction performed using a card, along with its metadata like merchant, country, channel, and type. It is designed for behavioral analysis, fraud detection, and spending pattern aggregation.

- **Type**: Fact  
- **CDC Type**: `1.1`  
- **Writer Type**: `factAppend`  
- **Primary Key**: `Card_Txn_ID`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Stores append-only records of card-based transactions. Each row reflects a customer's card usage instance, including location, amount, and merchant information.

---

### 🔗 Foreign Keys and Relationships:

| Column         | Referenced Table       | Description |
|----------------|------------------------|-------------|
| `Card_ID`      | `Dim_Card`             | Card used in the transaction  |
| `Customer_ID`  | `Dim_Customer`         | Cardholder/customer  |
| `Channel_ID`   | `Dim_Channel`          | Channel used for transaction (POS, ATM, Online)  |
| `Txn_Date`     | `Dim_Time`             | Date of transaction  |

---

### 📊 Key Columns:

| Raw Column Name | Raw Type | Standardized Column Name | Standardized Type | Description                            | PK  | Note                  |
|------------------|----------|---------------------------|--------------------|----------------------------------------|-----|------------------------|
| `Card_Txn_ID`    | VARCHAR  | `Card_Txn_ID`             | VARCHAR            | Unique ID of the card transaction      | ✅  | Primary key            |
| `Card_ID`        | VARCHAR  | `Card_ID`                 | VARCHAR            | Card used in the transaction           |     | FK to `Dim_Card`       |
| `Customer_ID`    | VARCHAR  | `Customer_ID`             | VARCHAR            | Customer who performed the transaction |     | FK to `Dim_Customer`   |
| `Txn_Date`       | DATE     | `Txn_Date`                | DATE               | Date of transaction                    |     | Partition source       |
| `Amount`         | DECIMAL  | `Amount`                  | DECIMAL            | Transaction amount                     |     | Used in AML logic      |
| `Merchant`       | VARCHAR  | `Merchant`                | VARCHAR            | Merchant name or location              |     |                        |
| `Country`        | VARCHAR  | `Country`                 | VARCHAR            | Country where transaction occurred     |     | Risk country check     |
| `Channel_ID`     | VARCHAR  | `Channel_ID`              | VARCHAR            | Channel type used (ATM, POS, Internet) |     | FK to `Dim_Channel`    |
| `Txn_Type`       | VARCHAR  | `Txn_Type`                | VARCHAR            | PURCHASE, WITHDRAWAL, etc.             |     | Used in segmentation   |
|           |   | `f_round_txn_flag`        | BOOLEAN            | TRUE if Amount is a round number       |     | AML flag               |
|           |   | `f_frequent_fx_flag`      | BOOLEAN            | TRUE if many foreign txns in short time |     | AML flag               |

---

### 🧪 Technical Fields (Standardize for Insight):

| Column Name           | Type       | Description |
|------------------------|------------|-------------|
| `cdc_change_type`      | STRING     | Always `'cdc_insert'` (CDC 1.1) |
| `cdc_index`            | LONG       | Monotonically increasing ID for checkpointing |
| `scd_change_timestamp` | TIMESTAMP  | Time record was written to fact table |
| `ds_partition_date`    | DATE       | Derived from `Txn_Date` |

---

### 🚩 Related AML Scenarios (Standardize → Insight)

| AML Scenario Name                   | Flag at Standardize      | Used in Insight |
|------------------------------------|---------------------------|------------------|
| Round-Number Transactions          | `f_round_txn_flag`        | ✅ Yes           |
| Frequent Foreign Currency Exchange | `f_frequent_fx_flag`      | ✅ Yes           |

---

### 🧠 Flag Logic Definitions

| Flag Name             | Type    | Logic Description                                                                 |
|-----------------------|---------|-----------------------------------------------------------------------------------|
| `f_round_txn_flag`     | BOOLEAN | TRUE if `Amount % 1_000_000 == 0` or ends in ≥ 4 zeros                           |
| `f_frequent_fx_flag`   | BOOLEAN | TRUE if ≥10 foreign transactions within 7 days for same `Customer_ID`            |

> 💡 `f_frequent_fx_flag` may require window-based calculation across Std_Card_Transaction or merged with Std_Transaction.

---

### ✅ Notes:
- Append-only logic; CDC 1.1 ensures immutability
- No `created_at` / `updated_at` — only `cdc_index` for incremental loads
- Flags precomputed to avoid repeated logic in insight stage