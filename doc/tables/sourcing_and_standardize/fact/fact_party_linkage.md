## 📜 Table: Fact_Party_Linkage

This table captures linkages between a customer and other individuals, entities, or accounts. It is commonly used for relationship risk scoring, network analysis, and identifying beneficial ownership structures in AML investigations.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factUpsert`  
- **Primary Key**: Composite key – `(Customer_ID, Party_ID, Link_Type)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Represents declared or inferred relationships between parties, including type, confidence, and supporting evidence.

---

### 📊 Key Columns (Standardize)

| Raw/Fact_Party_Linkage | Raw Type | Standardized/Fact_Party_Linkage | Standardized Type | Description                                      | PK  | Note                                |
|-------------------------|----------|----------------------------------|--------------------|--------------------------------------------------|-----|-------------------------------------|
| `Customer_ID`           | VARCHAR  | `Customer_ID`                    | VARCHAR            | Main customer ID                                | ✅  | FK to `Dim_Customer`                |
| `Party_ID`              | VARCHAR  | `Party_ID`                       | VARCHAR            | Linked counterparty or individual               | ✅  | FK to `Dim_Party` or `Dim_Customer` |
| `Link_Type`             | VARCHAR  | `Link_Type`                      | VARCHAR            | Nature of the link (e.g., Spouse, Employer)      | ✅  |                                     |
| `Link_Evidence`         | TEXT     | `Link_Evidence`                  | TEXT               | Supporting documentation or notes               |     | Optional                            |
| `Relationship_Start`    | DATE     | `Relationship_Start`             | DATE               | When the relationship was established           |     | FK to `Dim_Time`                    |
| `Confidence_Score`      | DECIMAL  | `Confidence_Score`               | DECIMAL            | System-generated score (0–1 or percentage)      |     | Reflects inference or certainty     |
|Technical Fields (Standardize)|
|                         |          | `cdc_change_type`                | STRING             | `'cdc_insert'` or `'cdc_update'`                |     | CDC 1.3 logic                        |
|                         |          | `cdc_index`                      | INT                | Change index for deduplication                  |     | Optional                            |
|                         |          | `scd_change_timestamp`           | TIMESTAMP          | Timestamp of ingestion                          |     |                                     |
|                         |          | `ds_partition_date`              | DATE               | Partitioning column                             |     | Usually same as `Relationship_Start`|
|                         |          | `created_at`                     | TIMESTAMP          | Insert timestamp                                |     |                                     |
|                         |          | `updated_at`                     | TIMESTAMP          | Last modified timestamp                         |     |                                     |

---

### ✅ Notes
- Enables relationship/network scoring and graph risk modeling  
- Supports identification of hidden beneficial owners or third-party risk  
- Confidence score helps separate declared from inferred links