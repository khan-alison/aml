## 📜 Table: Dim_KYC_Profile_Snapshot

This dimension stores periodic snapshots of a customer's full KYC profile. It includes identity, risk, occupation, and segmentation fields. This enables point-in-time reconstruction of the KYC state for scoring, investigations, or audit.

- **Type**: Dimension  
- **CDC Type**: `1.3`  
- **Writer Type**: `scd4a`  
- **Primary Key**: `Customer_ID` (from source)  
- **Partitioned By**: `ds_partition_date` (string, in `_Hist` table only)  
- **Snapshot Strategy**: SCD4a – current version in main table, full historical versions in `_Hist`

---

### 📊 Key Columns (Standardize)

| Raw/Dim_KYC_Profile_Snapshot | Raw Type  | PK  | Standardized/Dim_KYC_Profile_Snapshot | Standardized Type | Standardized/Dim_KYC_Profile_Snapshot_Hist | Description                                               | Value of Technical Field       | Note                            |
|------------------------------|-----------|-----|----------------------------------------|--------------------|---------------------------------------------|-----------------------------------------------------------|-------------------------------|---------------------------------|
| `Customer_ID`               | STRING    | ✅  | `Customer_ID`                          | STRING             | `Customer_ID`                                | Unique customer identifier                                 |                               | FK to `Dim_Customer`            |
| `Risk_Score`                | INT       |     | `Risk_Score`                           | INT                | `Risk_Score`                                 | Calculated KYC risk score                                 |                               | Derived from rules              |
| `Risk_Level`                | STRING    |     | `Risk_Level`                           | STRING             | `Risk_Level`                                 | Risk category (Low, Medium, High)                         |                               | Enum                            |
| `Occupation_Code`           | STRING    |     | `Occupation_Code`                      | STRING             | `Occupation_Code`                            | Customer's job or industry code                           |                               | FK to `Dim_Industry`            |
| `Segment_Code`              | STRING    |     | `Segment_Code`                         | STRING             | `Segment_Code`                               | Customer segmentation category                            |                               | FK to segmentation dimension    |
| `Nationality`               | STRING    |     | `Nationality`                          | STRING             | `Nationality`                                | ISO or internal nationality code                          |                               | FK to `Dim_Country`             |
| `Is_PEP`                    | BOOLEAN   |     | `Is_PEP`                               | BOOLEAN            | `Is_PEP`                                     | Politically Exposed Person flag                          |                               | High-risk indicator             |
| `created_at`                | TIMESTAMP |     | `created_at`                           | TIMESTAMP          | `created_at`                                 | When this snapshot was created in the source             | From source                   |                                 |
| `updated_at`                | TIMESTAMP |     | `updated_at`                           | TIMESTAMP          | `updated_at`                                 | When this snapshot was last updated                      | From source                   |                                 |
| **Technical Fields**        |           |     |                                        |                    |                                             |                                                           |                               |                                 |
|                              |           |     | `ds_key`                               | STRING             | `ds_key`                                     | Surrogate key in standardized zone                       | `Customer_ID`                | Used as PK                      |
|                              |           |     | `cdc_change_type`                      | STRING             | `cdc_change_type`                            | CDC operation type                                      | `'cdc_insert'`/`'cdc_update'`| From CDC layer                  |
|                              |           |     | `cdc_index`                            | INT                | `cdc_index`                                  | Current record flag                                     | 1 = current                  | Used in `scd4a` filter logic    |
|                              |           |     | `scd_change_timestamp`                 | TIMESTAMP          | `scd_change_timestamp`                       | Timestamp of change processing                          | `updated_at` or job time     | Required                        |
|                              |           |     | `dtf_start_date`                       | DATE               | `dtf_start_date`                             | Start of validity period                               | From `updated_at` or job time|                                 |
|                              |           |     | `dtf_end_date`                         | DATE               | `dtf_end_date`                               | End of validity period                                 | NULL if current              |                                 |
|                              |           |     | `dtf_current_flag`                     | BOOLEAN            | `dtf_current_flag`                           | Whether this record is the latest                      | TRUE/FALSE                   |                                 |
|                              |           |     |                    | STRING             | `ds_partition_date`                          | Partition column for `_Hist` table                      | Job date (`yyyy-MM-dd`)      | Only in `_Hist`                |

---

### ✅ Business Use Cases

- Support scoring engines with latest KYC data  
- Enable timeline analysis of profile evolution  
- Facilitate investigations by comparing past KYC snapshots  
- Satisfy regulator requests for exact state at given time  