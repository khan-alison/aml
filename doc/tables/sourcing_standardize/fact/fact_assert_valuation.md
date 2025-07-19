## 📜 Table: Fact_Asset_Valuation

This table captures periodic valuation records of assets such as collateral, real estate, or financial instruments. It includes the valuation source, type, amount, and currency. Useful for risk exposure monitoring, capital adequacy, and secured lending assessments.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factUpsert`  
- **Primary Key**: Composite key – `(Asset_ID, Valuation_Date)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Records asset valuations from internal or external sources, allowing point-in-time assessment of value.

---

### 🔗 Foreign Keys and Relationships:

| Column           | Referenced Table       | Description |
|------------------|------------------------|-------------|
| `Asset_ID`       | `Dim_Asset` or `Dim_Collateral` | Asset being valued  |
| `Valuation_Date` | `Dim_Time`             | Date of valuation    |

---

### 📊 Key Columns:

| Raw Column Name     | Raw Type | Standardized Column Name | Standardized Type | Description                                     | PK  | Note                        |
|---------------------|----------|---------------------------|--------------------|-------------------------------------------------|-----|-----------------------------|
| `Asset_ID`          | VARCHAR  | `Asset_ID`                | VARCHAR            | Identifier of the asset                         | ✅  | FK to `Dim_Asset` or `Dim_Collateral` |
| `Valuation_Date`    | DATE     | `Valuation_Date`          | DATE               | Date valuation was performed                    | ✅  | FK to `Dim_Time`             |
| `Valuation_Amount`  | DECIMAL  | `Valuation_Amount`        | DECIMAL            | Estimated value of asset                        |     |                             |
| `Source`            | VARCHAR  | `Source`                  | VARCHAR            | Source of valuation (internal, external)        |     |                             |
| `Valuation_Type`    | VARCHAR  | `Valuation_Type`          | VARCHAR            | Type of valuation (market, book, appraisal)     |     |                             |
| `Currency`          | VARCHAR  | `Currency`                | VARCHAR            | Currency used in valuation                      |     |                             |

---

### 🧪 Technical Fields (for CDC + audit):

| Raw Column Name        | Raw Type | Standardized Column Name | Standardized Type | Description                                  | PK  | Note |
|------------------------|----------|---------------------------|--------------------|----------------------------------------------|-----|------|
| `cdc_change_type`      | STRING   | `cdc_change_type`         | STRING             | `'cdc_insert'` or `'cdc_update'`             |     | CDC 1.3 logic           |
| `cdc_index`            | INT      | `cdc_index`               | INT                | Sequence/order indicator                     |     | Optional                |
| `scd_change_timestamp` | TIMESTAMP| `scd_change_timestamp`    | TIMESTAMP          | Time record was processed                    |     |                          |
| `ds_partition_date`    | DATE     | `ds_partition_date`       | DATE               | Partitioning date (usually Valuation_Date)    |     |                          |
| `created_at`           | TIMESTAMP| `created_at`              | TIMESTAMP          | Insertion timestamp                          |     |                          |
| `updated_at`           | TIMESTAMP| `updated_at`              | TIMESTAMP          | Last update timestamp                        |     |                          |

---

### ✅ Notes:
- Captures multi-source valuations for risk modeling
- Supports exposure monitoring, LTV adjustment, and fair-value reporting
- Works well with `Fact_Collateral_Assignment` and loan provisioning modules
