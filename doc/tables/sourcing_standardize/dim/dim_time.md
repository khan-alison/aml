## 📜 Table: Dim_Time

This is the standard time dimension used to support date-based partitioning, filtering, and aggregation across all fact tables. It provides multiple temporal breakdowns (year, quarter, month, etc.) to enable flexible time-based slicing.

- **Type**: Dimension  
- **CDC Type**: `1.1`  
- **Writer Type**: `scd1`  
- **Primary Key**: `Date_ID`  
- **Partitioned By**: none (static calendar table)  
- **Description**: Date dimension with calendar hierarchies and formats used across all reporting layers.

---

### 📊 Key Columns:

| Raw Column Name     | Raw Type | Standardized Column Name | Standardized Type | Description                              | PK  | Note            |
|----------------------|----------|---------------------------|--------------------|------------------------------------------|-----|-----------------|
| `Date_ID`            | DATE     | `Date_ID`                 | DATE               | Unique date identifier (yyyy-MM-dd)      | ✅  | Primary key     |
| `Year`              | INT      | `Year`                    | INT                | Calendar year                            |     |                 |
| `Month`             | INT      | `Month`                   | INT                | Calendar month (1–12)                    |     |                 |
| `Quarter`           | INT      | `Quarter`                 | INT                | Quarter (1–4)                            |     |                 |
| `Week`              | INT      | `Week`                    | INT                | Week number of the year                  |     |                 |
| `Day_of_Week`       | VARCHAR  | `Day_of_Week`             | VARCHAR            | Name or code of weekday (e.g., Mon)      |     |                 |

---

### 🧪 Technical Fields:

| Field Name            | Type       | Description                            |
|------------------------|------------|----------------------------------------|
| `cdc_change_type`      | STRING     | Always `'cdc_insert'` (static table)   |
| `scd_change_timestamp` | TIMESTAMP  | Load timestamp                         |
| `ds_partition_date`    | DATE       | Optional if joined with fact partitions|
| `created_at`           | TIMESTAMP  | Insert time                            |
| `updated_at`           | TIMESTAMP  | NULL or same as created_at             |

---

### ✅ Notes:
- No history tracking — values are static per date
- Essential for filtering, dashboard drilldowns, and time series models
- Can be enriched with holidays, fiscal flags, and working day indicators
