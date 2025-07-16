## 📜 Table: Fact_Transaction

- **Type**: Fact  
- **CDC Type**: `1.1`  
- **Writer Type**: `factAppend`  
- **Primary Key**: Composite key – `(Transaction_ID, Booking_Date)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Stores atomic financial transaction events, such as fund transfers, deposits, withdrawals, and bill payments. Each transaction is immutable and appended as-is without update or delete logic.

---

### 🔗 Foreign Keys and Relationships:

| Column               | Referenced Table       | Description |
|----------------------|------------------------|-------------|
| `From_Account_ID`    | `Dim_Account_Payment`  | Source account initiating transaction |
| `To_Account_ID`      | `Dim_Account_Payment`  | Destination account (if internal)     |
| `Transaction_Type_ID`| `Dim_TransactionType`  | Nature of transaction (e.g., transfer) |
| `Channel_ID`         | `Dim_Channel`          | Transaction channel (e.g., ATM, Mobile) |
| `Country_Code`       | `Dim_Country`          | Originating country                   |
| `Booking_Date`       | `Dim_Time`             | Date of processing                    |

---

### 📊 Key Columns:

| Column Name           | Description |
|------------------------|-------------|
| `Transaction_ID`       | Unique ID for each transaction  |
| `From_Account_ID`      | Account initiating the transaction  |
| `To_Account_ID`        | Receiving account (if any)  |
| `Amount`               | Transaction amount  |
| `Transaction_Type_ID`  | Type of transaction  |
| `Booking_Date`         | Transaction processing date  |
| `Channel_ID`           | Channel through which it occurred  |
| `Country_Code`         | Originating country code  |
| `Transaction_Reason`   | Free-text reason or description  |
| `Currency`             | Currency used  |

---

### 🧪 Technical Fields (for CDC + audit):

| Column Name           | Type       | Description |
|------------------------|------------|-------------|
| `cdc_change_type`      | STRING     | Always `'cdc_insert'` (append-only logic) |
| `cdc_index`            | LONG/INT   | Optional row sequence index             |
| `scd_change_timestamp` | TIMESTAMP  | Time record was loaded into Fact table  |
| `ds_partition_date`    | DATE       | Partition date (usually from Booking_Date) |
| `created_at`           | TIMESTAMP  | Same as `scd_change_timestamp`          |
| `updated_at`           | TIMESTAMP  | Typically null in CDC 1.1               |

---

### ✅ Notes:
- Aligns directly with **CDC Type 1.1**  
- Ideal for **audit**, **pattern detection**, and **velocity analysis**  
- No merge logic or deduplication — downstream consumers should handle if needed

