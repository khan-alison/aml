# 🧩 AML Project – Standard Mapping Specification (CDC + Technical Fields)

This document defines the standard required structure and behavior for all table mappings in the AML data platform. It governs both **dimension** and **fact** tables, across all CDC strategies.

---

## ✅ Table Metadata Block

Each mapping begins with a YAML-style metadata header:

- **Type**: `Dimension` or `Fact`
- **CDC Type**: e.g. `1.1`, `1.3`
- **Writer Type**: `scd4a`, `factAppend`, `scd1`, `factUpsert`, etc.
- **Primary Key**: Field used in Standardized Zone (often `ds_key`)
- **Partitioned By**: Always `ds_partition_date` (string)
- **Snapshot Strategy**: Only applies to SCD4a or SCD2

---

## 📊 Key Columns (Standardize)

Every table must present a unified table containing:

| Raw/{Table}         | Raw Type | Standardized/{Table}       | Standardized Type | Standardized/{Table}_Hist | Description                                  | PK  | Note                    |
|---------------------|----------|-----------------------------|--------------------|-----------------------------|----------------------------------------------|-----|-------------------------|

- Fields from source should be matched 1:1 wherever applicable.
- All dimension keys and joinable fields must clearly specify FK relationships.
- Mark the `ds_key` row as ✅ PK.
- **Technical fields must appear inline at the bottom**.

---

## 🔐 Required Technical Fields (Standardized Zone Only)

These are always **appended** during the transformation from raw → standardized. They are never present in the raw source.

| Field Name              | Type      | Required | Default or Logic                                                                 | Description                                                    |
|-------------------------|-----------|----------|-----------------------------------------------------------------------------------|----------------------------------------------------------------|
| `ds_key`                | STRING    | ✅       | - Use source PK (e.g. `Customer_ID`) if stable<br>- Else: `concat` or hash logic | Surrogate key used as primary key in Standardized zone         |
| `cdc_change_type`       | STRING    | ✅       | `'cdc_insert'`, `'cdc_update'`, `'cdc_delete'`                                   | Indicates type of change event (used for filtering)            |
| `cdc_index`             | INT       | ✅       | `1` = current record, `0` = outdated                                              | Used to quickly filter current valid records                   |
| `scd_change_timestamp`  | TIMESTAMP | ✅       | Prefer source `updated_at` or `created_at`<br>Else: job run time                 | Indicates when the snapshot or change occurred                 |
| `ds_partition_date`     | STRING    | ✅       | Job execution date in `'yyyy-MM-dd'` format                                       | Required for partitioning all tables                           |

---

## 🧠 Additional Notes

- `cdc_change_type` is critical for distinguishing deleted records in `factAppend` tables.
- `cdc_index = 1` can be used in analytics to filter "latest valid" records efficiently.
- `ds_partition_date` must always be `STRING`, even if derived from `created_at` or `Event_Date`.

---

## ✅ Sample Logic for `ds_key`

| Table Type     | ds_key Generation                                     | Example                                     |
|----------------|-------------------------------------------------------|---------------------------------------------|
| Stable PK      | `Customer_ID`                                         | `ds_key = Customer_ID`                      |
| Composite Key  | `concat(Customer_ID, Account_ID)`                     | `ds_key = concat(Customer_ID, '-', Account_ID)` |
| Multi-column   | `md5(concat(...))`                                    | `ds_key = md5(Customer_ID || Branch_Code)`  |

---

## 💡 Mapping Table Summary Layout Example

You must use the following format in all future mappings:

1. Metadata block  
2. Full column mapping table including **technical fields**  
3. Inline field-level explanations for logic, PK/FK, or value derivation  
4. Optional business use case section for context

---

Let me know if you'd like a Markdown template file prefilled with this structure, or want to continue mapping another table.