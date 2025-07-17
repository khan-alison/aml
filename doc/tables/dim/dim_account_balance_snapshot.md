## 📜 Table: Dim_Account_Balance_Snapshot

This dimension captures daily snapshots of account balances for behavioral analysis, velocity monitoring, and ML features. It implements `SCD4a` with daily full snapshots, while changes are detected using `CDC 1.3` from the core banking system.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Account_ID`  
- **Partitioned By**: `ds_partition_date` (in history table)  
- **Snapshot Strategy**: Daily full image captured in hist table; main table holds latest record only

---

### 🧩 Main Table Schema (Latest Snapshot Only)

| Column Name           | Type     | Description                                  |
|-----------------------|----------|----------------------------------------------|
| `Account_ID`          | VARCHAR  | Unique account identifier                    |
| `Customer_ID`         | VARCHAR  | Linked customer ID                           |
| `Balance_Date`        | DATE     | Snapshot date (balance as of this date)      |
| `Current_Balance`     | DECIMAL  | Current total balance                        |
| `Available_Balance`   | DECIMAL  | Funds available for withdrawal               |
| `Currency`            | VARCHAR  | Currency of the account                      |
| `Account_Status`      | VARCHAR  | Account status (e.g., ACTIVE, DORMANT)       |
| `Overdraft_Limit`     | DECIMAL  | Overdraft limit if applicable                |
| `Branch_ID`           | VARCHAR  | Branch managing the account                  |

#### 🧪 Technical Fields (Main Table):
| Column Name            | Type       | Description                                  |
|------------------------|------------|----------------------------------------------|
| `scd_change_type`      | STRING     | 'cdc_insert' or 'cdc_update'                 |
| `cdc_index`            | INT        | Optional order for record updates            |
| `scd_change_timestamp` | TIMESTAMP  | When the snapshot was taken                  |
| `dtf_start_date`       | DATE       | Snapshot validity start                      |
| `dtf_end_date`         | DATE       | Snapshot validity end (null if current)      |
| `dtf_current_flag`     | BOOLEAN    | TRUE if current snapshot                     |

---

### 🗃 History Table Schema (Snapshot per Day)

All fields from main table, **plus:**

| Column Name          | Type     | Description                                  |
|----------------------|----------|----------------------------------------------|
| `ds_partition_date`  | DATE     | Partition field = snapshot ingestion date    |

---

### ✅ Business Use Cases
- Measure transaction velocity (Δ balance over time)
- Detect sudden drops, inactivity, or overdraft risk
- Model balance behavior as ML features for credit/risk scoring
- Reconstruct historical account state at any point in time
