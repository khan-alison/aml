## 📜 Table: Dim_Asset_Risk_Profile

This dimension tracks the risk classification of customer-owned assets, including asset value category, volatility, and market exposure. It is updated daily to capture changes in asset nature or risk tiers and support AML profiling and credit decisioning.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Asset_ID`  
- **Partitioned By**: `ds_partition_date` (in history table)  
- **Snapshot Strategy**: Daily overwrite to history; current snapshot stored in main table

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Asset_Risk_Profile | Raw Type | Standardized/std_Asset_Risk_Profile | Standardized Type | Standardized/std_Asset_Risk_Profile_Hist | Description                                         | PK  | Note                           |
|-----------------------------|----------|-------------------------------------|-------------------|-------------------------------------------|-----------------------------------------------------|-----|--------------------------------|
| `Asset_ID`                 | VARCHAR  | `Asset_ID`                          | VARCHAR           | `Asset_ID`                                | Unique asset identifier                             | ✅  |                                |
| `Customer_ID`              | VARCHAR  | `Customer_ID`                       | VARCHAR           | `Customer_ID`                             | Owner of the asset                                  |     | FK to `Dim_Customer`           |
| `Asset_Type`               | VARCHAR  | `Asset_Type`                        | VARCHAR           | `Asset_Type`                              | Type of asset (e.g., Property, Stock, Crypto)       |     | Categorical                     |
| `Risk_Category`            | VARCHAR  | `Risk_Category`                     | VARCHAR           | `Risk_Category`                           | Classification: Low, Medium, High                   |     | Used in AML screening           |
| `Valuation_Amount`         | DECIMAL  | `Valuation_Amount`                  | DECIMAL           | `Valuation_Amount`                         | Estimated market value                              |     | Dynamic based on pricing feed   |
| `Valuation_Date`           | DATE     | `Valuation_Date`                    | DATE              | `Valuation_Date`                          | When asset value was last assessed                  |     | Snapshot consistency            |
| `Country_Code`             | VARCHAR  | `Country_Code`                      | VARCHAR           | `Country_Code`                            | Jurisdiction of asset location                      |     | FK to `Dim_Country`             |
|Technical Fields (for CDC + audit + snapshot logic)|
|                             |          | `scd_change_type`                  | STRING            | `scd_change_type`                         | `'cdc_insert'` or `'cdc_update'`                    |     | CDC 1.3 logic                    |
|                             |          | `cdc_index`                        | INT               | `cdc_index`                               | Optional change order field                         |     |                                |
|                             |          | `scd_change_timestamp`            | TIMESTAMP         | `scd_change_timestamp`                    | Ingestion timestamp                                 |     |                                |
|                             |          | `dtf_start_date`                  | DATE              | `dtf_start_date`                          | Start of validity window                            |     |                                |
|                             |          | `dtf_end_date`                    | DATE              | `dtf_end_date`                            | End of validity window                              |     | NULL = active                   |
|                             |          | `dtf_current_flag`               | BOOLEAN           | `dtf_current_flag`                        | TRUE = current active snapshot                      |     |                                |
|                             |          |                                   |                   | `ds_partition_date`                       | Partition column (history table only)               |     |                                |

---

### ✅ Business Use Cases

- Monitor high-risk or cross-border asset holdings  
- Detect unusual changes in valuation or asset exposure  
- Feed risk scoring models for loan, investment, or AML decisions  
- Maintain point-in-time asset risk state for forensic reviews