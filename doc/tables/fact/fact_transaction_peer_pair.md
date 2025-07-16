## 📜 Table: Fact_Transaction_Peer_Pair

This table aggregates transactional behavior between customer pairs over a rolling window. It is designed to identify patterns of structured layering, repeated transfers, or circular behavior that may indicate suspicious activity.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factUpsert`  
- **Primary Key**: Composite key – `(From_Customer_ID, To_Customer_ID, Window_Days)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Tracks volume and frequency of transactions between customer pairs over a defined number of days. Supports peer graph analysis and transaction network scoring.

---

### 🔗 Foreign Keys and Relationships:

| Column              | Referenced Table       | Description |
|---------------------|------------------------|-------------|
| `From_Customer_ID`  | `Dim_Customer`         | Sender customer ID  |
| `To_Customer_ID`    | `Dim_Customer`         | Receiver customer ID  |
| `First_Txn_Date`    | `Dim_Time`             | Date of first transaction in window  |

---

### 📊 Key Columns:

| Raw Column Name       | Raw Type | Standardized Column Name   | Standardized Type | Description                                          | PK  | Note                   |
|------------------------|----------|-----------------------------|--------------------|------------------------------------------------------|-----|------------------------|
| `From_Customer_ID`     | VARCHAR  | `From_Customer_ID`          | VARCHAR            | Originating customer                                | ✅  | FK to `Dim_Customer`   |
| `To_Customer_ID`       | VARCHAR  | `To_Customer_ID`            | VARCHAR            | Receiving customer                                  | ✅  | FK to `Dim_Customer`   |
| `Window_Days`          | INT      | `Window_Days`               | INT                | Rolling window size in days                         | ✅  | e.g., 7, 30, 90         |
| `Txn_Count`            | INT      | `Txn_Count`                 | INT                | Number of transactions in window                    |     |                        |
| `Total_Amount`         | DECIMAL  | `Total_Amount`              | DECIMAL            | Sum of transaction amounts in window                |     |                        |
| `First_Txn_Date`       | DATE     | `First_Txn_Date`            | DATE               | First observed transaction date in the window       |     | FK to `Dim_Time`       |
| `Bidirectional_Flag`   | BOOLEAN  | `Bidirectional_Flag`        | BOOLEAN            | True if both customers sent money to each other     |     |                        |

---

### 🧪 Technical Fields (for CDC + audit):

| Raw Column Name        | Raw Type | Standardized Column Name | Standardized Type | Description                               | PK  | Note |
|------------------------|----------|---------------------------|--------------------|-------------------------------------------|-----|------|
| `cdc_change_type`      | STRING   | `cdc_change_type`         | STRING             | `'cdc_insert'` or `'cdc_update'`          |     | CDC 1.3 logic           |
| `cdc_index`            | INT      | `cdc_index`               | INT                | Row index or change sequence              |     | Optional                |
| `scd_change_timestamp` | TIMESTAMP| `scd_change_timestamp`    | TIMESTAMP          | Record load time                          |     |                          |
| `ds_partition_date`    | DATE     | `ds_partition_date`       | DATE               | Partition date (e.g., `First_Txn_Date`)   |     |                          |
| `created_at`           | TIMESTAMP| `created_at`              | TIMESTAMP          | First insert timestamp                    |     |                          |
| `updated_at`           | TIMESTAMP| `updated_at`              | TIMESTAMP          | Last update time                          |     |                          |

---

### ✅ Notes:
- Enables network/graph-based peer analysis
- Supports detection of structuring, smurfing, and transaction loops
- Built from aggregated fact-level transactions
