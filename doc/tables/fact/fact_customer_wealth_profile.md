## 📜 Table: Fact_Customer_Wealth_Profile

This table provides a daily or periodic snapshot of a customer’s financial standing. It aggregates total balance, assets, income, and liabilities to assign a dynamic wealth tier classification. Used in customer segmentation, marketing, and risk-based onboarding.

- **Type**: Fact  
- **CDC Type**: `1.3`  
- **Writer Type**: `factUpsert`  
- **Primary Key**: Composite key – `(Customer_ID, Date_ID)`  
- **Partitioned By**: `ds_partition_date`  
- **Description**: Reflects financial summary indicators and wealth tier classification per customer on a given date.

---

### 🔗 Foreign Keys and Relationships:

| Column         | Referenced Table       | Description |
|----------------|------------------------|-------------|
| `Customer_ID`  | `Dim_Customer`         | Customer reference  |
| `Date_ID`      | `Dim_Time`             | Date of snapshot    |

---

### 📊 Key Columns:

| Raw Column Name     | Raw Type | Standardized Column Name | Standardized Type | Description                                        | PK  | Note                    |
|---------------------|----------|---------------------------|--------------------|----------------------------------------------------|-----|-------------------------|
| `Customer_ID`       | VARCHAR  | `Customer_ID`             | VARCHAR            | Customer identifier                                | ✅  | FK to `Dim_Customer`    |
| `Date_ID`           | DATE     | `Date_ID`                 | DATE               | Snapshot date                                      | ✅  | FK to `Dim_Time`        |
| `Total_Balance`     | DECIMAL  | `Total_Balance`           | DECIMAL            | Total balance across all accounts                 |     |                         |
| `Total_Assets`      | DECIMAL  | `Total_Assets`            | DECIMAL            | Estimated value of owned assets                   |     |                         |
| `Estimated_Income`  | DECIMAL  | `Estimated_Income`        | DECIMAL            | Monthly or annual estimated income                |     |                         |
| `Loan_Exposure`     | DECIMAL  | `Loan_Exposure`           | DECIMAL            | Outstanding liabilities or loans                  |     |                         |
| `Wealth_Tier`       | VARCHAR  | `Wealth_Tier`             | VARCHAR            | Tier (e.g., Mass, Affluent, HNW) based on profile |     | Derived field           |

---

### 🧪 Technical Fields (for CDC + audit):

| Raw Column Name        | Raw Type | Standardized Column Name | Standardized Type | Description                               | PK  | Note |
|------------------------|----------|---------------------------|--------------------|-------------------------------------------|-----|------|
| `cdc_change_type`      | STRING   | `cdc_change_type`         | STRING             | `'cdc_insert'` or `'cdc_update'`          |     | CDC 1.3 logic           |
| `cdc_index`            | INT      | `cdc_index`               | INT                | Row sequence index                        |     | Optional                |
| `scd_change_timestamp` | TIMESTAMP| `scd_change_timestamp`    | TIMESTAMP          | Timestamp of data load                    |     |                          |
| `ds_partition_date`    | DATE     | `ds_partition_date`       | DATE               | Partition column (aligned with Date_ID)   |     |                          |
| `created_at`           | TIMESTAMP| `created_at`              | TIMESTAMP          | Time record was first inserted            |     |                          |
| `updated_at`           | TIMESTAMP| `updated_at`              | TIMESTAMP          | Last update timestamp                     |     |                          |

---

### ✅ Notes:
- Enables customer segmentation and personalized service models
- Used for annual reviews, KYC enhancements, and creditworthiness scoring
- Often joined with product holdings and transactional behavior
