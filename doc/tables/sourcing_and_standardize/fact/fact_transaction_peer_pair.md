## 📜 Table: Fact_Transaction_Peer_Pair

This table aggregates transactional relationships between two customers across a sliding time window. Each record shows the total number of transactions, total transferred amount, and characteristics of interaction between a customer pair. It is designed to support peer-pattern detection, relationship scoring, and fraud ring identification.

- **Type**: Fact  
- **CDC Type**: `1.1`  
- **Writer Type**: `factAppend`  
- **Primary Key**: Composite – `(From_Customer_ID, To_Customer_ID, Window_Days, ds_partition_date)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Stores pairwise aggregated behavior between customer A and B over a defined time window (e.g., 7 days, 30 days).

---

### 🔗 Foreign Keys and Relationships:

| Column             | Referenced Table  | Description                            |
|--------------------|-------------------|----------------------------------------|
| `From_Customer_ID` | `Dim_Customer`    | Initiating party                       |
| `To_Customer_ID`   | `Dim_Customer`    | Receiving party                        |

---

### 📊 Key Columns:

| Raw Column Name    | Raw Type | Standardized Column Name     | Standardized Type | Description                                                     | PK  | Note                      |
|--------------------|----------|-------------------------------|--------------------|-----------------------------------------------------------------|-----|---------------------------|
| `From_Customer_ID` | VARCHAR  | `From_Customer_ID`            | VARCHAR            | Customer who initiated the transactions                        | ✅  | Composite key             |
| `To_Customer_ID`   | VARCHAR  | `To_Customer_ID`              | VARCHAR            | Receiving counterparty                                          | ✅  | Composite key             |
| `Window_Days`      | INT      | `Window_Days`                 | INT                | Number of days for aggregation window (e.g., 7)                | ✅  | Composite key             |
| `Txn_Count`        | INT      | `Txn_Count`                   | INT                | Number of transactions from A → B                              |     |                           |
| `Total_Amount`     | DECIMAL  | `Total_Amount`                | DECIMAL            | Total amount transferred in the window                         |     | AML detection input       |
| `First_Txn_Date`   | DATE     | `First_Txn_Date`              | DATE               | First transaction date in the window                           |     | Time anchoring            |
| `Bidirectional_Flag`| BOOLEAN | `Bidirectional_Flag`          | BOOLEAN            | TRUE if both A→B and B→A transactions exist                    |     | Derived flag              |
| *(N/A)*            | *(N/A)*  | `f_synthetic_relation_flag`   | BOOLEAN            | TRUE if sudden, heavy exchange with no prior history           |     | AML scenario flag         |
| *(N/A)*               | *(N/A)*  | `f_bidirectional_transfer_flag` | BOOLEAN           | TRUE if ≥2 transactions in both directions within 3 days and total amount exceeds threshold |     | AML scenario flag         |

---

### 🧪 Technical Fields (Standardize for Insight):

| Column Name           | Type       | Description |
|------------------------|------------|-------------|
| `cdc_change_type`      | STRING     | Always `'cdc_insert'` (CDC 1.1) |
| `cdc_index`            | LONG       | Monotonically increasing ingestion index |
| `scd_change_timestamp` | TIMESTAMP  | Time record landed in the lake |
| `ds_partition_date`    | DATE       | Date partition for the aggregate window |

---

### 🚩 Related AML Scenarios (Standardize → Insight)

| AML Scenario Name                   | Flag at Standardize          | Used in Insight |
|------------------------------------|-------------------------------|------------------|
| Synthetic Relationships Between Customers | `f_synthetic_relation_flag` | ✅ Yes           |
| Bidirectional Transfers Between Customers | `f_bidirectional_transfer_flag` | ✅ Yes |

---

### 🧠 Flag Logic Definitions

| Flag Name                  | Type    | Logic                                                                 |
|----------------------------|---------|-----------------------------------------------------------------------|
| `f_synthetic_relation_flag`| BOOLEAN | TRUE if no historical relationship in past 90d, AND ≥ 3 txns AND total > 50M VND within 7d |
| `f_bidirectional_transfer_flag` | BOOLEAN | TRUE if Customer A and B each send ≥2 transactions to each other within 3 days, and total amount ≥ configured threshold |

> 💡 May require enriching with historical peer-pair tracking table to detect "no prior history".

---

### ✅ Notes:
- Designed for window-based customer-pair profiling
- Can be reused across multiple scenarios (bidirectional layering, circular flow)
- Derived from `Fact_Transaction` via groupBy (customer_id_1, customer_id_2, window)