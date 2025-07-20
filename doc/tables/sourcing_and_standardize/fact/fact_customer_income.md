## 📜 Table: Fact_Customer_Income

This table estimates or records the monthly income of customers, based on transaction analysis, declared inflows, or predictive models. It supports credit scoring, customer profiling, and behavioral segmentation.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factUpsert`  
- **Primary Key**: Composite key – `(Customer_ID, Month)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Stores monthly income-level records per customer, with information on the source and estimation logic.

---

### 📊 Key Columns (Standardize)

| Raw/Fact_Customer_Income | Raw Type | Standardized/std_Customer_Income | Standardized Type | Standardized/std_Customer_Income_Hist | Description                                       | PK  | Note                     |
|--------------------------|----------|----------------------------------|-------------------|----------------------------------------|---------------------------------------------------|-----|--------------------------|
| `Customer_ID`            | VARCHAR  | `Customer_ID`                    | VARCHAR           | `Customer_ID`                          | Customer identifier                               | ✅  | FK to `Dim_Customer`     |
| `Month`                  | DATE     | `Month`                          | DATE              | `Month`                                | Snapshot month of the inflow                      | ✅  | FK to `Dim_Time`         |
| `Inflow_Amount`          | DECIMAL  | `Inflow_Amount`                  | DECIMAL           | `Inflow_Amount`                        | Estimated/observed monthly income                 |     |                          |
| `Inflow_Source`          | VARCHAR  | `Inflow_Source`                  | VARCHAR           | `Inflow_Source`                        | Source of inflow (salary, rental, etc.)           |     |                          |
| `Income_Type`            | VARCHAR  | `Income_Type`                    | VARCHAR           | `Income_Type`                          | Income classification (e.g., regular)             |     |                          |
| `Estimation_Method`      | VARCHAR  | `Estimation_Method`              | VARCHAR           | `Estimation_Method`                    | Logic or model used for estimation                |     |                          |
| *(derived)*              | *(N/A)*  | `f_high_txn_to_income_ratio_flag`| BOOLEAN           | `f_high_txn_to_income_ratio_flag`      | TRUE if total monthly outflows > 5× income        |     | AML scenario flag         |
|**Technical Fields (for CDC + audit)**|         |                                  |                   |                                        |                                                   |     |                          |
|                          |          | `cdc_change_type`                | STRING            | `cdc_change_type`                      | `'cdc_insert'` or `'cdc_update'`                 |     | CDC 1.3 logic            |
|                          |          | `cdc_index`                      | INT               | `cdc_index`                            | Optional CDC ordering                            |     |                          |
|                          |          | `scd_change_timestamp`           | TIMESTAMP         | `scd_change_timestamp`                 | Ingestion timestamp                              |     |                          |
|                          |          | `created_at`                     | TIMESTAMP         | `created_at`                           | Time first seen in system                        |     | Required for CDC 1.3     |
|                          |          | `updated_at`                     | TIMESTAMP         | `updated_at`                           | Last update timestamp                            |     | Required for CDC 1.3     |
|                          |          |                                  |                   | `ds_partition_date`                    | Partition column (aligned with `Month`)          | ✅  |                          |

---

### 🚩 Related AML Scenarios (Standardize → Insight)

| AML Scenario Name                  | Flag at Standardize               | Used in Insight |
|-----------------------------------|-----------------------------------|------------------|
| High Transaction-to-Income Ratio  | `f_high_txn_to_income_ratio_flag` | ✅ Yes           |

---

### 🧠 Flag Logic Definitions

| Flag Name                         | Type    | Logic                                                                 |
|-----------------------------------|---------|-----------------------------------------------------------------------|
| `f_high_txn_to_income_ratio_flag` | BOOLEAN | TRUE if sum(outflow transactions for the month) > 5 × `Inflow_Amount` |

---

### ✅ Notes

- Enables monthly affordability and income vs. behavior consistency checks  
- Sourced from declared values and/or transaction-derived inference  
- Can power dashboards showing salary trend, volatility, or underreporting