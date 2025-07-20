## 📜 Table: Fact_Card_Transaction

This table captures all credit/debit card transaction activity made by customers. Each row represents one transaction performed using a card, along with its metadata like merchant, country, channel, and type. It is designed for behavioral analysis, fraud detection, and spending pattern aggregation.

- **Type**: Fact  
- **CDC Type**: `1.1`  
- **Writer Type**: `factAppend`  
- **Primary Key**: `Card_Txn_ID`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Stores append-only records of card-based transactions. Each row reflects a customer's card usage instance, including location, amount, and merchant information.

---

### 📊 Key Columns (Standardize)

| Raw/Fact_Card_Transaction | Raw Type | Standardized/std_Card_Transaction | Standardized Type | Standardized/std_Card_Transaction_Hist | Description                                      | PK  | Note                     |
|----------------------------|----------|-----------------------------------|-------------------|----------------------------------------|--------------------------------------------------|-----|--------------------------|
| `Card_Txn_ID`             | VARCHAR  | `Card_Txn_ID`                     | VARCHAR           | `Card_Txn_ID`                          | Unique ID of the card transaction                | ✅  | Primary key              |
| `Card_ID`                 | VARCHAR  | `Card_ID`                         | VARCHAR           | `Card_ID`                              | Card used in the transaction                     |     | FK to `Dim_Card`         |
| `Customer_ID`             | VARCHAR  | `Customer_ID`                     | VARCHAR           | `Customer_ID`                          | Cardholder/customer                              |     | FK to `Dim_Customer`     |
| `Txn_Date`                | DATE     | `Txn_Date`                        | DATE              | `Txn_Date`                             | Date of transaction                              |     | FK to `Dim_Time`         |
| `Amount`                  | DECIMAL  | `Amount`                          | DECIMAL           | `Amount`                               | Transaction amount                               |     | AML scenario input       |
| `Merchant`                | VARCHAR  | `Merchant`                        | VARCHAR           | `Merchant`                             | Merchant name or location                        |     |                          |
| `Country`                 | VARCHAR  | `Country`                         | VARCHAR           | `Country`                              | Country of transaction                           |     | Risk geography screening |
| `Channel_ID`              | VARCHAR  | `Channel_ID`                      | VARCHAR           | `Channel_ID`                           | POS, ATM, Online, etc.                           |     | FK to `Dim_Channel`      |
| `Txn_Type`                | VARCHAR  | `Txn_Type`                        | VARCHAR           | `Txn_Type`                             | PURCHASE, WITHDRAWAL, etc.                       |     |                          |
| *(Derived)*               | *(N/A)*  | `f_round_txn_flag`                | BOOLEAN           | `f_round_txn_flag`                     | TRUE if Amount ends in ≥ 4 zeros                 |     | AML flag                 |
| *(Derived)*               | *(N/A)*  | `f_frequent_fx_flag`              | BOOLEAN           | `f_frequent_fx_flag`                   | TRUE if frequent foreign txns in 7-day window    |     | AML flag (window-based)  |
|**Technical Fields (for CDC 1.1)**   |          |                                   |                   |                                        |                                                  |     |                          |
|                            |          | `cdc_change_type`                | STRING            | `cdc_change_type`                      | Always `'cdc_insert'` (append-only)              |     | CDC 1.1 logic             |
|                            |          | `cdc_index`                      | LONG              | `cdc_index`                            | Monotonically increasing for checkpointing        |     | Required                  |
|                            |          | `scd_change_timestamp`          | TIMESTAMP         | `scd_change_timestamp`                 | Time written to the fact table                   |     | Ingestion time            |
|                            |          |                                  |                   | `ds_partition_date`                    | Derived from `Txn_Date`                          |     | Partition field           |

---

### 🚩 Related AML Scenarios (Standardize → Insight)

| AML Scenario                        | Flag Name              | Derived in Standardize | Used in Insight |
|-------------------------------------|------------------------|-------------------------|------------------|
| Round-number card transactions      | `f_round_txn_flag`     | ✅                      | ✅               |
| Frequent foreign card usage         | `f_frequent_fx_flag`   | ✅                      | ✅               |

---

### 🧠 Flag Logic Definitions

| Flag Name             | Type    | Logic Description                                                                 |
|-----------------------|---------|-----------------------------------------------------------------------------------|
| `f_round_txn_flag`     | BOOLEAN | TRUE if `Amount % 1_000_000 == 0` or ends in ≥ 4 trailing zeros                   |
| `f_frequent_fx_flag`   | BOOLEAN | TRUE if ≥10 card transactions in foreign currency within any 7-day rolling window |

> 💡 `f_frequent_fx_flag` requires Spark window function logic grouped by `Customer_ID`, filtered by currency ≠ local.

---

### ✅ Notes

- Append-only ingestion — no updates or deletes  
- `cdc_index` enables checkpointed ingestion in pipelines  
- Flags support real-time anomaly monitoring in dashboards  
- Serves as input for behavioral scoring and velocity models