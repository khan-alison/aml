## 📜 Table: Dim_Risk_Level

This dimension defines the various risk level categories used in customer or transaction scoring. It maps risk bands to threshold scores and descriptive labels, enabling standardized interpretation across AML rules and dashboards.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd2`  
- **Primary Key**: `Risk_Level_ID`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Reference mapping of risk bands used across customer segmentation, transaction scoring, and alerting systems.

---

### 📊 Key Columns:

| Raw Column Name     | Raw Type | Standardized Column Name | Standardized Type | Description                                     | PK  | Note         |
|----------------------|----------|---------------------------|--------------------|-------------------------------------------------|-----|--------------|
| `Risk_Level_ID`      | VARCHAR  | `Risk_Level_ID`           | VARCHAR            | Unique identifier for the risk band             | ✅  | Primary key  |
| `Level_Name`         | VARCHAR  | `Level_Name`              | VARCHAR            | Label for the level (e.g., LOW, MEDIUM, HIGH)   |     | UI usage     |
| `Score_Threshold`    | INT      | `Score_Threshold`         | INT                | Minimum score required to fall into this band   |     | Applied in rule logic |
| `Description`        | VARCHAR  | `Description`             | VARCHAR            | Business context or notes about this band       |     |               |

---

### 🧪 Technical Fields (for SCD2 tracking):

| Field Name            | Type       | Description                                   |
|------------------------|------------|-----------------------------------------------|
| `scd_change_type`      | STRING     | `'cdc_insert'`, `'cdc_update'`, `'cdc_delete'`|
| `cdc_index`            | INT        | Change tracking index                         |
| `scd_change_timestamp` | TIMESTAMP  | Timestamp of version load                     |
| `ds_partition_date`    | DATE       | Partitioning field (e.g., version load date)  |
| `created_at`           | TIMESTAMP  | Time inserted                                 |
| `updated_at`           | TIMESTAMP  | Time last updated                             |
| `dtf_start_date`       | DATE       | Start of version validity                     |
| `dtf_end_date`         | DATE       | End of version validity                       |
| `dtf_current_flag`     | BOOLEAN    | TRUE = current active version                 |

---

### ✅ Notes:
- Used in joins with `Fact_Risk_Score`, `Fact_Customer_Wealth_Profile`, etc.
- Enables grouping and filtering of high-risk entities in dashboards
- Can be maintained by compliance officers or risk engines
