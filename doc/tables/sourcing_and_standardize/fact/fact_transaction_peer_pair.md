## 📜 Table: Fact_Transaction_Peer_Pair

This table aggregates transactional relationships between two customers across a sliding time window. Each record shows the total number of transactions, total transferred amount, and characteristics of interaction between a customer pair. It is designed to support peer-pattern detection, relationship scoring, and fraud ring identification.

- **Type**: Fact  
- **CDC Type**: `1.1`  
- **Writer Type**: `factAppend`  
- **Primary Key**: Composite – `(From_Customer_ID, To_Customer_ID, Window_Days, ds_partition_date)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Stores pairwise aggregated behavior between customer A and B over a defined time window (e.g., 7 days, 30 days).

---

### 📊 Key Columns (Standardize)

| Raw/TableName                    | Raw Type | Standardized/TableName            | Standardized Type | Description                                                                 | PK  | Note                                       |
|----------------------------------|----------|-----------------------------------|--------------------|-----------------------------------------------------------------------------|-----|--------------------------------------------|
| `From_Customer_ID`               | VARCHAR  | `From_Customer_ID`                | VARCHAR            | Customer who initiated the transactions                                     | ✅  | FK to `Dim_Customer`                       |
| `To_Customer_ID`                 | VARCHAR  | `To_Customer_ID`                  | VARCHAR            | Receiving customer                                                          | ✅  | FK to `Dim_Customer`                       |
| `Window_Days`                    | INT      | `Window_Days`                     | INT                | Time window in days (e.g., 7, 30)                                           | ✅  | Composite PK element                       |
| `Txn_Count`                      | INT      | `Txn_Count`                       | INT                | Number of transactions from A to B                                          |     | Derived via aggregation                    |
| `Total_Amount`                   | DECIMAL  | `Total_Amount`                    | DECIMAL            | Total amount transferred in window                                          |     | Used in flag logic                         |
| `First_Txn_Date`                 | DATE     | `First_Txn_Date`                  | DATE               | First transaction date in the window                                        |     | Time anchor                                |
| `Bidirectional_Flag`            | BOOLEAN  | `Bidirectional_Flag`              | BOOLEAN            | TRUE if both A→B and B→A transactions exist                                 |     | Behavioral indicator                       |
| *(Derived)*                      | *(N/A)*  | `f_synthetic_relation_flag`       | BOOLEAN            | TRUE if heavy transactions exist without prior history                      |     | AML scenario flag                          |
| *(Derived)*                      | *(N/A)*  | `f_bidirectional_transfer_flag`   | BOOLEAN            | TRUE if ≥2 txns in both directions within 3d and total exceeds threshold    |     | AML scenario flag                          |
|Technical Fields (for CDC + audit)|
| *(Technical)*                    | STRING   | `cdc_change_type`                 | STRING             | Always `'cdc_insert'` for CDC 1.1                                           |     | Append-only                                |
| *(Technical)*                    | LONG     | `cdc_index`                       | LONG               | Monotonically increasing ingestion index                                    |     | Checkpointing                             |
| *(Technical)*                    | TIMESTAMP| `scd_change_timestamp`            | TIMESTAMP          | Timestamp of record arrival                                                 |     |                                            |
| *(Technical)*                    | DATE     | `ds_partition_date`               | DATE               | Partition column (usually last Txn date)                                    | ✅  | Part of composite PK                       |

---

### 🚩 Related AML Scenarios

| AML Scenario Name                        | Flag at Standardize             | Used in Insight |
|-----------------------------------------|----------------------------------|------------------|
| Synthetic Relationship Detection         | `f_synthetic_relation_flag`      | ✅ Yes           |
| Bidirectional Transaction Flows          | `f_bidirectional_transfer_flag`  | ✅ Yes           |

---

### 🧠 Flag Logic Definitions

| Flag Name                         | Type    | Logic                                                                                  |
|----------------------------------|---------|----------------------------------------------------------------------------------------|
| `f_synthetic_relation_flag`      | BOOLEAN | TRUE if no historical peer-pair in past 90d, AND ≥3 txns, AND total > 50M VND         |
| `f_bidirectional_transfer_flag`  | BOOLEAN | TRUE if both A and B sent ≥2 txns to each other in ≤3 days AND total ≥ threshold      |

---

### ✅ Notes

- Built from rolling aggregation on `Fact_Transaction`  
- Helps identify collusion networks, laundering rings, and fabricated peer links  
- Use with `f_synthetic_relation_flag` to detect sudden new high-risk connections  