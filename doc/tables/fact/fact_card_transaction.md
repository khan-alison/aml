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

| Column Name     | Description |
|------------------|-------------|
| `Card_Txn_ID`    | Unique ID of the card transaction  |
| `Card_ID`        | Card used for the transaction  |
| `Customer_ID`    | Customer who performed the transaction  |
| `Txn_Date`       | Date the transaction occurred  |
| `Amount`         | Transaction amount  |
| `Merchant`       | Merchant name or location  |
| `Country`        | Country where the transaction occurred  |
| `Channel_ID`     | Channel type used  |
| `Txn_Type`       | Transaction type (e.g., PURCHASE, WITHDRAWAL)  |

---

### 🧪 Technical Fields (for CDC + audit):

| Column Name           | Type       | Description |
|------------------------|------------|-------------|
| `cdc_change_type`      | STRING     | Always `'cdc_insert'`  |
| `cdc_index`            | LONG/INT   | Optional row sequencing index  |
| `scd_change_timestamp` | TIMESTAMP  | Time record was written to the fact table  |
| `ds_partition_date`    | DATE       | Partition date (from Txn_Date)  |
| `created_at`           | TIMESTAMP  | Time of insertion  |
| `updated_at`           | TIMESTAMP  | Usually null in CDC 1.1  |

---

### ✅ Notes:
- Append-only ingestion strategy (CDC 1.1)  
- Enables time-series analysis and fraud modeling  
- Supports real-time transaction visibility for monitoring systems

