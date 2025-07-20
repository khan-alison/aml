## 📜 Table: Dim_Time

This is the standard time dimension used to support date-based partitioning, filtering, and aggregation across all fact tables. It provides multiple temporal breakdowns (year, quarter, month, etc.) to enable flexible time-based slicing.

- **Type**: Dimension  
- **CDC Type**: `1.1`  
- **Writer Type**: `scd1`  
- **Primary Key**: `Date_ID`  
- **Partitioned By**: *(None – static table)*  
- **Description**: Date dimension with calendar hierarchies and formats used across all reporting layers.

---

### 📊 Key Columns (Standardize)

| Raw/Dim_Time | Raw Type | Standardized/std_Time | Standardized Type | Standardized/std_Time_Hist | Description                                | PK  | Note                       |
|--------------|----------|------------------------|-------------------|-----------------------------|--------------------------------------------|-----|----------------------------|
| `Date_ID`    | DATE     | `Date_ID`              | DATE              | `Date_ID`                   | Unique date identifier (yyyy-MM-dd)        | ✅  | Primary key                |
| `Year`       | INT      | `Year`                 | INT               | `Year`                      | Calendar year                              |     |                            |
| `Month`      | INT      | `Month`                | INT               | `Month`                     | Calendar month (1–12)                      |     |                            |
| `Quarter`    | INT      | `Quarter`              | INT               | `Quarter`                   | Quarter (1–4)                              |     |                            |
| `Week`       | INT      | `Week`                 | INT               | `Week`                      | Week number of the year                    |     |                            |
| `Day_of_Week`| VARCHAR  | `Day_of_Week`          | VARCHAR           | `Day_of_Week`               | Name or code of weekday (e.g., Mon)        |     |                            |
| **Technical Fields (for CDC + audit)** |          |                        |                   |                             |                                            |     |                            |
|              |          | `cdc_change_type`      | STRING            | `cdc_change_type`           | Always `'cdc_insert'`                      |     | CDC 1.1 static table logic |
|              |          | `scd_change_timestamp` | TIMESTAMP         | `scd_change_timestamp`      | Load timestamp                             |     |                            |
|              |          | `ds_partition_date`    | DATE              | `ds_partition_date`         | Static or aligned with fact partitions     |     | Optional for filtering     |

---

### ✅ Notes

- No history tracking — values are static per date  
- Essential for filtering, dashboard drilldowns, and time series models  
- Can be enriched with holidays, fiscal flags, and working day indicators  
- **CDC 1.1: Do not include `created_at`, `updated_at`**