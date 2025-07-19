## 📜 Table: Fact_Customer_Income

This table estimates or records the monthly income of customers, based on transaction analysis, declared inflows, or predictive models. It supports credit scoring, customer profiling, and behavioral segmentation.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factUpsert`  
- **Primary Key**: Composite key – `(Customer_ID, Month)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Stores monthly income-level records per customer, with information on the source and estimation logic.

---

### 🔗 Foreign Keys and Relationships:

| Column         | Referenced Table       | Description |
|----------------|------------------------|-------------|
| `Customer_ID`  | `Dim_Customer`         | Customer reference  |
| `Month`        | `Dim_Time`             | Monthly snapshot date  |

---

### 📊 Key Columns:

| Raw Column Name     | Raw Type | Standardized Column Name | Standardized Type | Description                                     | PK  | Note                     |
|---------------------|----------|---------------------------|--------------------|-------------------------------------------------|-----|--------------------------|
| `Customer_ID`       | VARCHAR  | `Customer_ID`             | VARCHAR            | Customer identifier                             | ✅  | FK to `Dim_Customer`     |
| `Month`             | DATE     | `Month`                   | DATE               | Snapshot month of the inflow                    | ✅  | FK to `Dim_Time`         |
| `Inflow_Amount`     | DECIMAL  | `Inflow_Amount`           | DECIMAL            | Monthly income amount estimated/observed        |     |                          |
| `Inflow_Source`     | VARCHAR  | `Inflow_Source`           | VARCHAR            | Source of inflow (e.g., salary, rental, transfer)|     |                          |
| `Income_Type`       | VARCHAR  | `Income_Type`             | VARCHAR            | Type of income (e.g., regular, irregular)       |     |                          |
| `Estimation_Method` | VARCHAR  | `Estimation_Method`       | VARCHAR            | How the income was estimated                    |     |                          |
| *(N/A)*             | *(N/A)*  | `f_high_txn_to_income_ratio_flag` | BOOLEAN           | TRUE if total transaction outflows exceed 5× monthly declared income |     | AML scenario flag         |

---

### 🧪 Technical Fields (for CDC + audit):

| Raw Column Name        | Raw Type | Standardized Column Name | Standardized Type | Description                                 | PK  | Note |
|------------------------|----------|---------------------------|--------------------|---------------------------------------------|-----|------|
| `cdc_change_type`      | STRING   | `cdc_change_type`         | STRING             | `'cdc_insert'` or `'cdc_update'`            |     | CDC 1.3 logic            |
| `cdc_index`            | INT      | `cdc_index`               | INT                | Sequence/order index                        |     | Optional                 |
| `scd_change_timestamp` | TIMESTAMP| `scd_change_timestamp`    | TIMESTAMP          | Ingestion timestamp                         |     |                           |
| `ds_partition_date`    | DATE     | `ds_partition_date`       | DATE               | Partition date (aligned with `Month`)       |     |                           |
| `created_at`           | TIMESTAMP| `created_at`              | TIMESTAMP          | Time first seen in data                     |     |                           |
| `updated_at`           | TIMESTAMP| `updated_at`              | TIMESTAMP          | Time last updated                           |     |                           |

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

### ✅ Notes:
- Uses **CDC 1.3** logic for upsert (merge by `Customer_ID` + `Month`)
- Enables monthly income trend and customer affordability modeling
- Can be sourced from both declared values and transactional inference
- Flag supports AML profiling where declared income is disproportionately lower than spending