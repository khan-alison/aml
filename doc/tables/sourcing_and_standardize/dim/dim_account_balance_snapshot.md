## 📜 Table: Dim_Account_Balance_Snapshot

This dimension stores daily snapshots of account balances, enabling point-in-time views of financial activity per account. It supports behavioral monitoring, AML trend detection, and historical backtesting of account states.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Account_ID`  
- **Partitioned By**: `ds_partition_date` (in history table)  
- **Snapshot Strategy**: Full daily overwrite to history table; current view maintained in main table

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Account_Balance_Snapshot | Raw Type | Standardized/std_Account_Balance_Snapshot | Standardized Type | Standardized/std_Account_Balance_Snapshot_Hist | Description                                       | PK  | Note                            |
|----------------------------------|----------|-------------------------------------------|-------------------|--------------------------------------------------|---------------------------------------------------|-----|---------------------------------|
| `Account_ID`                     | VARCHAR  | `Account_ID`                              | VARCHAR           | `Account_ID`                                    | Unique account identifier                         | ✅  | FK to `Dim_Account`             |
| `Customer_ID`                    | VARCHAR  | `Customer_ID`                             | VARCHAR           | `Customer_ID`                                   | Owner of the account                              |     | FK to `Dim_Customer`            |
| `Date_ID`                        | DATE     | `Date_ID`                                 | DATE              | `Date_ID`                                       | Snapshot date                                     |     | FK to `Dim_Time`                |
| `Available_Balance`             | DECIMAL  | `Available_Balance`                       | DECIMAL           | `Available_Balance`                             | Amount available for withdrawal                   |     |                                 |
| `Ledger_Balance`                | DECIMAL  | `Ledger_Balance`                          | DECIMAL           | `Ledger_Balance`                                | Posted balance including holds                    |     |                                 |
| `Currency`                      | VARCHAR  | `Currency`                                | VARCHAR           | `Currency`                                      | Currency of the account                           |     |                                 |
| `Account_Status`                | VARCHAR  | `Account_Status`                          | VARCHAR           | `Account_Status`                                | Status (ACTIVE, CLOSED, etc.)                     |     | Optional for segmentation       |
| *(Derived)*                     | *(N/A)*  | `f_closed_indicator`                      | BOOLEAN           | `f_closed_indicator`                            | TRUE if account was closed in the snapshot        |     | Derived lifecycle flag          |
| `created_at`                    | TIMESTAMP| `created_at`                              | TIMESTAMP         | `created_at`                                    | When the record was first seen in the source      |     | From source (CDC 1.3)           |
| `updated_at`                    | TIMESTAMP| `updated_at`                              | TIMESTAMP         | `updated_at`                                    | When the record was last updated in the source    |     | From source (CDC 1.3)           |
| **Technical Fields (for CDC + audit + snapshot logic)** |          |                                           |                   |                                                  |                                                   |     |                                 |
|                                  |          | `scd_change_type`                         | STRING            | `scd_change_type`                               | `'cdc_insert'` or `'cdc_update'`                  |     | CDC 1.3 logic                    |
|                                  |          | `cdc_index`                               | INT               | `cdc_index`                                     | Monotonic ingestion checkpoint                    |     | Optional                        |
|                                  |          | `scd_change_timestamp`                    | TIMESTAMP         | `scd_change_timestamp`                          | When the snapshot was ingested                    |     | Technical field                  |
|                                  |          | `dtf_start_date`                          | DATE              | `dtf_start_date`                                | Start of snapshot validity                        |     | Technical field                  |
|                                  |          | `dtf_end_date`                            | DATE              | `dtf_end_date`                                  | End of snapshot validity (NULL = current)         |     | Technical field                  |
|                                  |          | `dtf_current_flag`                        | BOOLEAN           | `dtf_current_flag`                              | TRUE if this is the currently valid snapshot      |     | Technical field                  |
|                                  |          |                                           |                   | `ds_partition_date`                             | Partition date (in history table only)            |     | `_Hist` table only              |

---

### ✅ Business Use Cases

- Detect changes in account activity trends over time  
- Identify reactivated or dormant accounts based on balance change  
- Support AML scenarios like sudden spikes or dips in balance  
- Power lifecycle flags such as account closure (`f_closed_indicator`)  
- Enable historical auditability for financial state reconstruction