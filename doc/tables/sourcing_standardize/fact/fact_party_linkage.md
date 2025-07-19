## 📜 Table: Fact_Party_Linkage

This table captures linkages between a customer and other individuals, entities, or accounts. It is commonly used for relationship risk scoring, network analysis, and identifying beneficial ownership structures in AML investigations.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factUpsert`  
- **Primary Key**: Composite key – `(Customer_ID, Party_ID, Link_Type)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Represents declared or inferred relationships between parties, including type, confidence, and supporting evidence.

---

### 🔗 Foreign Keys and Relationships:

| Column         | Referenced Table       | Description |
|----------------|------------------------|-------------|
| `Customer_ID`  | `Dim_Customer`         | Primary customer in the relationship  |
| `Party_ID`     | `Dim_Party` or `Dim_Customer` | Linked entity or person             |
| `Relationship_Start` | `Dim_Time`         | Start of the relationship             |

---

### 📊 Key Columns:

| Raw Column Name       | Raw Type | Standardized Column Name | Standardized Type | Description                                      | PK  | Note                           |
|------------------------|----------|---------------------------|--------------------|--------------------------------------------------|-----|--------------------------------|
| `Customer_ID`          | VARCHAR  | `Customer_ID`             | VARCHAR            | Main customer ID                                | ✅  | FK to `Dim_Customer`           |
| `Party_ID`             | VARCHAR  | `Party_ID`                | VARCHAR            | Linked counterparty or individual               | ✅  | FK to `Dim_Party` or `Dim_Customer` |
| `Link_Type`            | VARCHAR  | `Link_Type`               | VARCHAR            | Nature of the link (e.g., Spouse, Employer)      | ✅  |                                |
| `Link_Evidence`        | TEXT     | `Link_Evidence`           | TEXT               | Supporting documentation or notes               |     | Could be source document        |
| `Relationship_Start`   | DATE     | `Relationship_Start`      | DATE               | When the relationship was established           |     | FK to `Dim_Time`                |
| `Confidence_Score`     | DECIMAL  | `Confidence_Score`        | DECIMAL            | System-generated score (0–1 or % range)         |     | Indicates inference confidence  |

---

### 🧪 Technical Fields (for CDC + audit):

| Raw Column Name        | Raw Type | Standardized Column Name | Standardized Type | Description                               | PK  | Note |
|------------------------|----------|---------------------------|--------------------|-------------------------------------------|-----|------|
| `cdc_change_type`      | STRING   | `cdc_change_type`         | STRING             | `'cdc_insert'` or `'cdc_update'`          |     | CDC 1.3 logic           |
| `cdc_index`            | INT      | `cdc_index`               | INT                | Row index for audit trail                 |     | Optional                |
| `scd_change_timestamp` | TIMESTAMP| `scd_change_timestamp`    | TIMESTAMP          | Timestamp of ingestion                    |     |                          |
| `ds_partition_date`    | DATE     | `ds_partition_date`       | DATE               | Partition column                          |     | Often from `Relationship_Start` |
| `created_at`           | TIMESTAMP| `created_at`              | TIMESTAMP          | First insert timestamp                    |     |                          |
| `updated_at`           | TIMESTAMP| `updated_at`              | TIMESTAMP          | Last update timestamp                     |     |                          |

---

### ✅ Notes:
- Enables social/transactional network modeling for AML
- Supports KYC enrichment and third-party risk management
- `Confidence_Score` can reflect AI/ML-based inference certainty
