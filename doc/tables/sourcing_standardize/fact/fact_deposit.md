## 📜 Table: Fact_Deposit

This table records fixed-term or demand deposit information held by customers. Each entry includes the deposit terms, principal amount, associated interest rate, and maturity timeline. It supports deposit analytics, interest liability projections, and cash flow modeling.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factUpsert`  
- **Primary Key**: `Deposit_ID`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Tracks the latest state of customer deposits including type, duration, interest, and maturity. Supports upsert behavior based on deposit ID.

---

### 🔗 Foreign Keys and Relationships:

| Column         | Referenced Table       | Description |
|----------------|------------------------|-------------|
| `Deposit_ID`   | `Dim_Deposit`          | Master metadata of the deposit  |
| `Customer_ID`  | `Dim_Customer`         | Owner of the deposit  |
| `Branch_ID`    | `Dim_Branch`           | Branch where deposit was created  |
| `Start_Date`   | `Dim_Time`             | Start date of the deposit  |
| `Maturity_Date`| `Dim_Time`             | End/maturity date of deposit  |

---

### 📊 Key Columns:

| Raw Column Name  | Raw Type | Standardized Column Name | Standardized Type | Description                          | PK  | Note                    |
|------------------|----------|---------------------------|--------------------|--------------------------------------|-----|-------------------------|
| `Deposit_ID`     | VARCHAR  | `Deposit_ID`              | VARCHAR            | Unique ID of the deposit             | ✅  |                         |
| `Customer_ID`    | VARCHAR  | `Customer_ID`             | VARCHAR            | Linked customer identifier           |     | FK to `Dim_Customer`    |
| `Deposit_Type`   | VARCHAR  | `Deposit_Type`            | VARCHAR            | Type of deposit (e.g., Term, Savings)|     |                         |
| `Start_Date`     | DATE     | `Start_Date`              | DATE               | Deposit opening date                 |     | FK to `Dim_Time`        |
| `Maturity_Date`  | DATE     | `Maturity_Date`           | DATE               | Contractual maturity date            |     | FK to `Dim_Time`        |
| `Amount`         | DECIMAL  | `Amount`                  | DECIMAL            | Principal amount deposited           |     |                         |
| `Interest_Rate`  | DECIMAL  | `Interest_Rate`           | DECIMAL            | Annual interest rate agreed          |     |                         |
| `Branch_ID`      | VARCHAR  | `Branch_ID`               | VARCHAR            | Branch where the deposit was opened  |     | FK to `Dim_Branch`      |

---

### 🧪 Technical Fields (for CDC + audit):

| Raw Column Name        | Type       | Description                                 | Standardized Column Name | Type       | Description                                 |
|------------------------|------------|---------------------------------------------|----------------------------|------------|---------------------------------------------|
| `cdc_change_type`      | STRING     | Change type from source (`insert`/`update`) | `cdc_change_type`          | STRING     | `'cdc_insert'` or `'cdc_update'` event      |
| `cdc_index`            | LONG/INT   | Raw sequence/order index                    | `cdc_index`                | LONG/INT   | Sequence/order indicator                    |
| `scd_change_timestamp` | TIMESTAMP  | Timestamp from raw ingestion                | `scd_change_timestamp`     | TIMESTAMP  | Time of record processing                   |
| `ds_partition_date`    | DATE       | Load or transaction date                    | `ds_partition_date`        | DATE       | Partition column (load or business date)    |
| `created_at`           | TIMESTAMP  | Creation timestamp                          | `created_at`               | TIMESTAMP  | First insert timestamp                      |
| `updated_at`           | TIMESTAMP  | Last modified timestamp                     | `updated_at`               | TIMESTAMP  | Last update time (if applicable)            |

------------------------|------------|-------------|
| `cdc_change_type`      | STRING     | `'cdc_insert'` or `'cdc_update'` depending on event  |
| `cdc_index`            | LONG/INT   | Sequence/order indicator  |
| `scd_change_timestamp` | TIMESTAMP  | Time of record processing  |
| `ds_partition_date`    | DATE       | Date partition (based on `Start_Date` or load date)  |
| `created_at`           | TIMESTAMP  | When record was first created  |
| `updated_at`           | TIMESTAMP  | Last updated time (via upsert)  |

---

### ✅ Notes:
- Uses **CDC Type 1.3** with upsert logic
- Ideal for showing current position of customer deposits
- Enables term maturity tracking and interest forecasting
