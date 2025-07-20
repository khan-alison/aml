## 📜 Table: Dim_Alert_Type

This dimension table defines the alert categories and detection scenarios used in AML systems. Each record corresponds to a rule-driven or model-driven scenario that triggers alerts. Severity is used for prioritization in alert queues and dashboards.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd2`  
- **Primary Key**: `Alert_Type_ID`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Reference table listing alert types, detection logic, and severity classification used for AML alert generation and workflow routing.

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Alert_Type  | Raw Type | Standardized/Dim_Alert_Type | Standardized Type | Description                                             | PK  | Note                         |
|---------------------|----------|------------------------------|--------------------|---------------------------------------------------------|-----|------------------------------|
| `Alert_Type_ID`     | VARCHAR  | `Alert_Type_ID`              | VARCHAR            | Unique identifier of alert type                         | ✅  | Primary key                  |
| `Scenario_Name`     | VARCHAR  | `Scenario_Name`              | VARCHAR            | Short business-readable label for scenario              |     | Display name for UI          |
| `Detection_Rule`    | TEXT     | `Detection_Rule`             | TEXT               | Description of rule logic triggering the alert          |     | Rule engine format (SQL, DSL)|
| `Severity_Level`    | VARCHAR  | `Severity_Level`             | VARCHAR            | Priority of alert (e.g., LOW, MEDIUM, HIGH)             |     | Used in alert routing        |
| `created_at`        | TIMESTAMP| `created_at`                 | TIMESTAMP          | When the record was first created in the source         |     | From source (CDC 1.3)        |
| `updated_at`        | TIMESTAMP| `updated_at`                 | TIMESTAMP          | When the record was last updated in the source          |     | From source (CDC 1.3)        |
| **Technical Fields (for CDC + audit)** |          |                          |                    |                                                         |     |                              |
|                     |          | `scd_change_type`            | STRING             | `'cdc_insert'`, `'cdc_update'`, `'cdc_delete'`          |     | SCD2 tracking                |
|                     |          | `cdc_index`                  | INT                | Row change index                                        |     | Optional                     |
|                     |          | `scd_change_timestamp`       | TIMESTAMP          | Time of record version change                           |     | Technical field              |
|                     |          | `dtf_start_date`             | DATE               | Start of SCD2 version                                   |     | Technical field              |
|                     |          | `dtf_end_date`               | DATE               | End of SCD2 version                                     |     | Technical field              |
|                     |          | `dtf_current_flag`           | BOOLEAN            | TRUE = currently active version                         |     | Technical field              |


---

### ✅ Notes

- Used in `Fact_Alert` to determine the triggering scenario and severity  
- Supports case prioritization in AML workflows  
- `Detection_Rule` can be synced from rule engines or model explanations