## 📜 Table: Fact_Customer_Balance

This table tracks the daily closing balance for each customer's account. It is used for monitoring financial position, account valuation, and trend analysis. The data can also feed liquidity risk models or customer segmentation logic.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factUpsert`  
- **Primary Key**: Composite key – `(Customer_ID, Account_ID, Date_ID)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Stores the latest daily balance for each customer-account combination. Updated via upsert to keep only the current record per day.

---

### 📊 Key Columns (Standardize)

| Raw/Fact_Customer_Balance | Raw Type | Standardized/std_Customer_Balance | Standardized Type | Standardized/std_Customer_Balance_Hist | Description                              | PK  | Note                         |
|---------------------------|----------|-----------------------------------|-------------------|-----------------------------------------|------------------------------------------|-----|------------------------------|
| `Customer_ID`             | VARCHAR  | `Customer_ID`                     | VARCHAR           | `Customer_ID`                           | Customer who owns the account            | ✅  | FK to `Dim_Customer`         |
| `Account_ID`              | VARCHAR  | `Account_ID`                      | VARCHAR           | `Account_ID`                            | Account belonging to customer            | ✅  | FK to `Dim_Account_Payment`  |
| `Date_ID`                 | DATE     | `Date_ID`                         | DATE              | `Date_ID`                               | Snapshot date of the balance             | ✅  | FK to `Dim_Time`             |
| `Closing_Balance`         | DECIMAL  | `Closing_Balance`                 | DECIMAL           | `Closing_Balance`                       | Balance at end of the business day       |     |                              |
| `Currency`                | VARCHAR  | `Currency`                        | VARCHAR           | `Currency`                              | Currency of the balance                  |     |                              |
|**Technical Fields (for CDC 1.3)**|         |                                   |                   |                                         |                                          |     |                              |
|                           |          | `cdc_change_type`                | STRING            | `cdc_change_type`                       | `'cdc_insert'` or `'cdc_update'`         |     | CDC 1.3 logic                 |
|                           |          | `cdc_index`                      | INT               | `cdc_index`                             | Sequence index                           |     | Optional                     |
|                           |          | `scd_change_timestamp`           | TIMESTAMP         | `scd_change_timestamp`                  | Ingestion timestamp                      |     |                              |
|                           |          | `created_at`                     | TIMESTAMP         | `created_at`                            | Time record was first inserted           |     | Required for CDC 1.3         |
|                           |          | `updated_at`                     | TIMESTAMP         | `updated_at`                            | Last update time                         |     | Required for CDC 1.3         |
|                           |          |                                  |                   | `ds_partition_date`                     | Partition column                         | ✅  | Usually aligned with `Date_ID`|

---

### ✅ Notes

- One record per `(Customer_ID, Account_ID, Date_ID)`  
- Used for behavioral analysis, liquidity tracking, and time series modeling  
- Required for trend flags in insight layer (e.g., balance drops, sudden increase)  