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

### 📊 Key Columns (Standardize)

| Raw/Fact_Deposit | Raw Type | Standardized/Fact_Deposit | Standardized Type | Description                               | PK  | Note                  |
|------------------|----------|----------------------------|--------------------|-------------------------------------------|-----|------------------------|
| `Deposit_ID`     | VARCHAR  | `Deposit_ID`               | VARCHAR            | Unique ID of the deposit                  | ✅  | Primary key            |
| `Customer_ID`    | VARCHAR  | `Customer_ID`              | VARCHAR            | Linked customer identifier                |     | FK to `Dim_Customer`   |
| `Deposit_Type`   | VARCHAR  | `Deposit_Type`             | VARCHAR            | Type of deposit (e.g., Term, Savings)     |     |                        |
| `Start_Date`     | DATE     | `Start_Date`               | DATE               | Deposit opening date                      |     | FK to `Dim_Time`       |
| `Maturity_Date`  | DATE     | `Maturity_Date`            | DATE               | Contractual maturity date                 |     | FK to `Dim_Time`       |
| `Amount`         | DECIMAL  | `Amount`                   | DECIMAL            | Principal amount deposited                |     |                        |
| `Interest_Rate`  | DECIMAL  | `Interest_Rate`            | DECIMAL            | Annual interest rate agreed               |     |                        |
| `Branch_ID`      | VARCHAR  | `Branch_ID`                | VARCHAR            | Branch where the deposit was opened       |     | FK to `Dim_Branch`     |

---

### 🧪 Technical Fields (CDC + Audit)

| Standardized Field     | Type       | Description                                 |
|------------------------|------------|---------------------------------------------|
| `cdc_change_type`      | STRING     | `'cdc_insert'` or `'cdc_update'` from source|
| `cdc_index`            | INT        | Optional row sequence for versioning        |
| `scd_change_timestamp` | TIMESTAMP  | Ingestion timestamp                         |
| `ds_partition_date`    | DATE       | Partition column (usually Start_Date or load date) |
| `created_at`           | TIMESTAMP  | Record creation time                        |
| `updated_at`           | TIMESTAMP  | Record last updated time                    |

---

### ✅ Notes:

- CDC 1.3 ensures the latest state per `Deposit_ID` with overwrite semantics  
- Useful for forecasting future interest liabilities and maturity schedules  
- Pairs with `Fact_Customer_Balance` for total liquidity and cash flow planning