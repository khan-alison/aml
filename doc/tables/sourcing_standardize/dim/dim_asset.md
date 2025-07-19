## 📜 Table: Dim_Asset

This dimension captures individual customer-linked assets that may be used as collateral, declared wealth, or subject to valuation and monitoring. It includes ownership details, registration metadata, and lifecycle status.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd2`  
- **Primary Key**: `Asset_ID`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Defines customer-reported or institution-tracked assets, used in wealth profiling, collateral analysis, and financial monitoring.

---

### 🔗 Foreign Keys and Relationships:

| Column         | Referenced Table       | Description |
|----------------|------------------------|-------------|
| `Customer_ID`  | `Dim_Customer`         | Asset owner                           |
| `Country`      | `Dim_Country`          | Country where the asset is registered |

---

### 📊 Key Columns:

| Raw Column Name     | Raw Type | Standardized Column Name | Standardized Type | Description                                        | PK  | Note                    |
|----------------------|----------|---------------------------|--------------------|----------------------------------------------------|-----|-------------------------|
| `Asset_ID`           | VARCHAR  | `Asset_ID`                | VARCHAR            | Unique identifier for each asset                  | ✅  | Primary key             |
| `Asset_Type`         | VARCHAR  | `Asset_Type`              | VARCHAR            | Type (e.g., Property, Vehicle, Jewelry, Stock)    |     | Used in segmentation    |
| `Description`        | VARCHAR  | `Description`             | VARCHAR            | Brief description of the asset                    |     |                         |
| `Registration_No`    | VARCHAR  | `Registration_No`         | VARCHAR            | Official registration or certificate number       |     | May be sensitive         |
| `Currency`           | VARCHAR  | `Currency`                | VARCHAR            | Currency of valuation or purchase                 |     | Used in valuation logic |
| `Purchase_Date`      | DATE     | `Purchase_Date`           | DATE               | When asset was acquired or declared               |     |                         |
| `Customer_ID`        | VARCHAR  | `Customer_ID`             | VARCHAR            | Customer who owns the asset                       |     | FK to `Dim_Customer`    |
| `Country`            | VARCHAR  | `Country`                 | VARCHAR            | Location where asset is registered/located        |     | FK to `Dim_Country`     |
| `Asset_Status`       | VARCHAR  | `Asset_Status`            | VARCHAR            | ACTIVE, DISPOSED, ENCUMBERED, etc.                |     | Lifecycle status        |

---

### 🧪 Technical Fields (for SCD2 tracking):

| Field Name            | Type       | Description                                   |
|------------------------|------------|-----------------------------------------------|
| `scd_change_type`      | STRING     | `'cdc_insert'`, `'cdc_update'`, `'cdc_delete'`|
| `cdc_index`            | INT        | Change order index                            |
| `scd_change_timestamp` | TIMESTAMP  | Record load timestamp                         |
| `ds_partition_date`    | DATE       | Partitioning column                           |
| `created_at`           | TIMESTAMP  | When record was first inserted                |
| `updated_at`           | TIMESTAMP  | When record was last modified                 |
| `dtf_start_date`       | DATE       | Start of active period                        |
| `dtf_end_date`         | DATE       | End of active period                          |
| `dtf_current_flag`     | BOOLEAN    | TRUE if this is the active record             |

---

### ✅ Notes:
- Used in `Fact_Asset_Valuation`, `Fact_Collateral_Assignment`, and KYC enrichment
- Helps evaluate customer wealth, net worth, and risk exposure
- Supports regulatory disclosures and asset verification workflows
