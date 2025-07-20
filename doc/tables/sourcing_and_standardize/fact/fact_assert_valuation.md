## 📜 Table: Fact_Asset_Valuation

This table captures periodic valuation records of assets such as collateral, real estate, or financial instruments. It includes the valuation source, type, amount, and currency. Useful for risk exposure monitoring, capital adequacy, and secured lending assessments.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factUpsert`  
- **Primary Key**: Composite key – `(Asset_ID, Valuation_Date)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Records asset valuations from internal or external sources, allowing point-in-time assessment of value.

---

### 📊 Key Columns (Standardize)

| Raw/Fact_Asset_Valuation | Raw Type | Standardized/std_Asset_Valuation | Standardized Type | Standardized/std_Asset_Valuation_Hist | Description                                      | PK  | Note                               |
|---------------------------|----------|----------------------------------|-------------------|----------------------------------------|--------------------------------------------------|-----|------------------------------------|
| `Asset_ID`               | VARCHAR  | `Asset_ID`                       | VARCHAR           | `Asset_ID`                             | Identifier of the asset                          | ✅  | FK to `Dim_Asset` or `Dim_Collateral` |
| `Valuation_Date`         | DATE     | `Valuation_Date`                 | DATE              | `Valuation_Date`                       | Date valuation was performed                     | ✅  | FK to `Dim_Time`                    |
| `Valuation_Amount`       | DECIMAL  | `Valuation_Amount`               | DECIMAL           | `Valuation_Amount`                     | Estimated value of the asset                     |     |                                     |
| `Source`                 | VARCHAR  | `Source`                         | VARCHAR           | `Source`                               | Source of valuation (internal, external)         |     |                                     |
| `Valuation_Type`         | VARCHAR  | `Valuation_Type`                 | VARCHAR           | `Valuation_Type`                       | Type (market, book, appraisal)                   |     |                                     |
| `Currency`               | VARCHAR  | `Currency`                       | VARCHAR           | `Currency`                             | Currency of valuation                            |     | FK to `Dim_Currency`                |
| `created_at`             | TIMESTAMP| `created_at`                     | TIMESTAMP         | `created_at`                           | Time when record was created                     |     | From source (CDC 1.3)               |
| `updated_at`             | TIMESTAMP| `updated_at`                     | TIMESTAMP         | `updated_at`                           | Last updated timestamp                           |     | From source (CDC 1.3)               |
|**Technical Fields (for CDC + audit + snapshot logic)**|          |                                  |                   |                                        |                                                  |     |                                     |
|                           |          | `cdc_change_type`               | STRING            | `cdc_change_type`                      | `'cdc_insert'` or `'cdc_update'`                 |     | CDC 1.3 logic                        |
|                           |          | `cdc_index`                     | INT               | `cdc_index`                            | Sequence/order indicator                         |     | Optional                            |
|                           |          | `scd_change_timestamp`         | TIMESTAMP         | `scd_change_timestamp`                 | Time record was processed                        |     |                                     |
|                           |          |                                  |                   | `ds_partition_date`                    | Partitioning date (usually `Valuation_Date`)     |     | `_Hist` table only                  |

---

### ✅ Business Use Cases

- Capture multi-source asset valuations for regulatory and risk modeling  
- Support LTV (loan-to-value) calculations and collateral adequacy checks  
- Enable fair-value accounting and point-in-time risk assessments  
- Join with `Fact_Collateral_Assignment` to monitor secured lending