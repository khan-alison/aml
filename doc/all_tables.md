# 🧩 AML Schema – CDC Type & Writer Type Summary (Corrected)

This document summarizes the **CDC Types** (Change Data Capture) and **Writer Types** for all **32 tables** in the AML schema, organized by 7 main domain sections.

---

## 1️⃣ Customer & KYC Dimensions

| Table                            | CDC Type | Writer Type | Notes                                                        |
|----------------------------------|----------|-------------|--------------------------------------------------------------|
| `Dim_Customer`                   | 1.3      | scd4a       | Core customer profile with history tracking                  |
| `Fact_KYC_Event`                | 1.1      | factAppend  | Log of KYC events – insert-only, no snapshot needed          |
| `Dim_Customer_Asset_Ownership`  | 1.3      | scd4a       | Ownership links between customer and assets                  |
| `Dim_Customer_Wealth_Profile`   | 1.3      | scd4a       | Estimated customer wealth – slowly changing                  |
| `Dim_Employment`                | 1.3      | scd4a       | Employment history for behavioral profiling                  |
| `Dim_Identity_Document`         | 1.3      | scd4a       | Customer ID/passport information                             |

---

## 2️⃣ Organization, Geography, Reference

| Table            | CDC Type | Writer Type | Notes                                         |
|------------------|----------|-------------|-----------------------------------------------|
| `Dim_Branch`     | 1.1      | scd1        | Bank branch directory                         |
| `Dim_Country`    | 1.1      | scd1        | Country list with risk level                  |
| `Dim_Currency`   | 1.1      | scd1        | ISO currency codes and FX rates               |
| `Dim_Deposit`    | 1.1      | scd1        | Deposit product reference                     |
| `Dim_Account`    | 1.3      | scd4a       | Detailed account information with history     |
| `Dim_Time`       | 0.0      | static      | Static time dimension                         |

---

## 3️⃣ Risk, Score, Alert, Linkage

| Table                               | CDC Type | Writer Type | Notes                                             |
|-------------------------------------|----------|-------------|---------------------------------------------------|
| `Alert_Fact`                        | 1.3      | factUpsert  | Captures triggered alerts                         |
| `Dim_Compliance_Rule_Snapshot`     | 1.3      | scd4a       | Snapshot of rule logic for auditability           |
| `Fact_Customer_Risk_Score`         | 1.3      | scd4a       | Daily customer risk scoring                       |
| `Dim_Customer_Linkage`             | 1.3      | scd4a       | Relationship mapping between customers            |

---

## 4️⃣ Transaction & Transfer

| Table                   | CDC Type | Writer Type | Notes                                           |
|-------------------------|----------|-------------|-------------------------------------------------|
| `Fact_Transaction`      | 1.3      | factAppend  | Core transaction data, append-only              |
| `Dim_Transaction_Type`  | 1.1      | scd1        | Reference for transaction types                 |
| `Dim_Channel`           | 1.1      | scd1        | Channels (e.g., Online, ATM, Branch)            |
| `Dim_Service_Type`      | 1.1      | scd1        | Service classification                          |

---

## 5️⃣ Deposit, Loan, Balance

| Table                       | CDC Type | Writer Type | Notes                                                           |
|-----------------------------|----------|-------------|-----------------------------------------------------------------|
| `Fact_Deposit`              | 1.3      | factAppend  | Captures cash inflows to deposit products                      |
| `Dim_Account_Balance`       | 1.3      | scd4a       | Daily snapshot of account balances per account                 |
| `Dim_Loan_Repayment`        | 1.3      | scd4a       | Repayment details with historical tracking                     |
| `Fact_Customer_Income`      | 1.3      | factAppend  | Verified inflows (salary, dividends) to assess financial behavior |

--- 

## 6️⃣ Asset, Investment, Collateral

| Table                       | CDC Type | Writer Type | Notes                                                  |
|-----------------------------|----------|-------------|--------------------------------------------------------|
| `Fact_Collateral_Assignment`| 1.3      | factUpsert  | Links customers to pledged collateral                  |
| `Dim_Collateral_Type`       | 1.1      | scd1        | Reference for collateral types                         |
| `Dim_Asset`                 | 1.3      | scd4a       | Metadata for physical and registered assets            |
| `Dim_Security`              | 1.3      | scd4a       | Investment securities owned by customers               |

---

## 7️⃣ Audit, Change, Behavior Tracking

| Table                          | CDC Type | Writer Type | Notes                                                           |
|--------------------------------|----------|-------------|-----------------------------------------------------------------|
| `Fact_KYC_Change_Log`          | 1.1      | factAppend  | Tracks all changes made to KYC profiles                         |
| `Dim_KYC_Profile_Snapshot`     | 1.3      | scd4a       | Periodic snapshots of full KYC profile                          |
| `Fact_Login_Activity`          | 1.3      | factAppend  | Logs login sessions for anomaly detection                       |
| `Fact_Forex_Transaction`       | 1.3      | factAppend  | Captures foreign exchange transactions (used in Scenario #15)   |

---

## 🔁 Summary

### CDC Types

- **CDC 1.3**: 22 tables  
- **CDC 1.1**: 9 tables  
- **CDC 0.0**: 1 table (`Dim_Time`)

### Writer Types

- **scd4a**: 15 tables  
- **scd1**: 6 tables  
- **factAppend**: 8 tables  
- **factUpsert**: 3 tables  
- **static**: 1 table

---
