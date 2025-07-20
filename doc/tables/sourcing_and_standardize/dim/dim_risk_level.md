## 📜 Table: Dim_Risk_Level

This dimension defines the various risk level categories used in customer or transaction scoring. It maps risk bands to threshold scores and descriptive labels, enabling standardized interpretation across AML rules and dashboards.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd2`  
- **Primary Key**: `Risk_Level_ID`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Reference mapping of risk bands used across customer segmentation, transaction scoring, and alerting systems.

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Risk_Level | Raw Type | Standardized/std_Risk_Level | Standardized Type | Description                                       | PK  | Note                     |
|--------------------|----------|------------------------------|-------------------|---------------------------------------------------|-----|--------------------------|
| `Risk_Level_ID`    | VARCHAR  | `Risk_Level_ID`              | VARCHAR           | Unique identifier for the risk band               | ✅  | Primary key              |
| `Level_Name`       | VARCHAR  | `Level_Name`                 | VARCHAR           | Label for the level (e.g., LOW, MEDIUM, HIGH)     |     | UI usage                 |
| `Score_Threshold`  | INT      | `Score_Threshold`            | INT               | Minimum score required to fall into this band     |     | Applied in rule logic    |
| `Description`      | VARCHAR  | `Description`                | VARCHAR           | Business context or notes about this band         |     |                          |
| `created_at`       | TIMESTAMP| `created_at`                 | TIMESTAMP         | Time inserted into the system                     |     | Required for CDC 1.3     |
| `updated_at`       | TIMESTAMP| `updated_at`                 | TIMESTAMP         | Last updated timestamp                            |     | Required for CDC 1.3     |
| **Technical Fields (for CDC + audit + SCD2 tracking)** |          |                      |                   |                                                   |     |                          |
|                    |          | `scd_change_type`           | STRING            | `'cdc_insert'`, `'cdc_update'`, `'cdc_delete'`    |     | CDC 1.3 logic             |
|                    |          | `cdc_index`                 | INT               | Change tracking index                             |     | Optional                  |
|                    |          | `scd_change_timestamp`      | TIMESTAMP         | Timestamp of version ingestion                    |     |                          |
|                    |          | `dtf_start_date`            | DATE              | Start of version validity                         |     |                          |
|                    |          | `dtf_end_date`              | DATE              | End of version validity                           |     | NULL = active version     |
|                    |          | `dtf_current_flag`          | BOOLEAN           | TRUE = current active version                     |     |                          |


---

### ✅ Notes

- Used in joins with `Fact_Risk_Score`, `Fact_Customer_Wealth_Profile`, etc.  
- Enables grouping and filtering of high-risk entities in dashboards  
- Can be maintained by compliance officers or risk engines  
- Facilitates explainable thresholds in risk scoring pipelines