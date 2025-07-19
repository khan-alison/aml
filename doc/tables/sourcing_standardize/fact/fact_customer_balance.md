## 📜 Table: Fact_Customer_Balance

This table tracks the daily closing balance for each customer's account. It is used for monitoring financial position, account valuation, and trend analysis. The data can also feed liquidity risk models or customer segmentation logic.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factUpsert`  
- **Primary Key**: Composite key – `(Customer_ID, Account_ID, Date_ID)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Stores the latest daily balance for each customer-account combination. Updated via upsert to keep only the current record per day.

---

### 🔗 Foreign Keys and Relationships:

| Column         | Referenced Table       | Description |
|----------------|------------------------|-------------|
| `Customer_ID`  | `Dim_Customer`         | Customer identifier  |
| `Account_ID`   | `Dim_Account_Payment`  | Account reference  |
| `Date_ID`      | `Dim_Time`             | Date for which balance is reported  |

---

### 📊 Key Columns:

| Raw Column Name  | Raw Type | Standardized Column Name | Standardized Type | Description                              | PK  | Note                         |
|------------------|----------|---------------------------|--------------------|------------------------------------------|-----|------------------------------|
| `Customer_ID`    | VARCHAR  | `Customer_ID`             | VARCHAR            | Customer who owns the account            | ✅  | FK to `Dim_Customer`         |
| `Account_ID`     | VARCHAR  | `Account_ID`              | VARCHAR            | Account belonging to customer            | ✅  | FK to `Dim_Account_Payment`  |
| `Date_ID`        | DATE     | `Date_ID`                 | DATE               | Snapshot date of the balance             | ✅  | FK to `Dim_Time`             |
| `Closing_Balance`| DECIMAL  | `Closing_Balance`         | DECIMAL            | Balance at end of the business day       |     |                              |
| `Currency`       | VARCHAR  | `Currency`                | VARCHAR            | Currency of the balance                  |     |                              |

---

### 🧪 Technical Fields (for CDC + audit):

| Raw Column Name        | Raw Type | Standardized Column Name | Standardized Type | Description                             | PK  | Note |
|------------------------|----------|---------------------------|--------------------|-----------------------------------------|-----|------|
| `cdc_change_type`      | STRING   | `cdc_change_type`         | STRING             | Change type from source (`insert`/`update`) |     | Via CDC 1.3 logic            |
| `cdc_index`            | INT      | `cdc_index`               | INT                | Row sequence index                      |     | Optional                     |
| `scd_change_timestamp` | TIMESTAMP| `scd_change_timestamp`    | TIMESTAMP          | Record load/ingestion timestamp         |     |                                |
| `ds_partition_date`    | DATE     | `ds_partition_date`       | DATE               | Partitioning date (often = `Date_ID`)   |     |                                |
| `created_at`           | TIMESTAMP| `created_at`              | TIMESTAMP          | Time record was first inserted          |     |                                |
| `updated_at`           | TIMESTAMP| `updated_at`              | TIMESTAMP          | Last update time (upserted)             |     |                                |

---

### ✅ Notes:
- Uses **CDC Type 1.3** for merge/update logic
- One record per customer-account per day
- Supports historical backfills and time series analytics
