# 📘 Insight Table Join Mapping for AML Scenarios (Detailed)

This document outlines how each insight table is derived through specific joins across the data model. For each table, we identify:
- Which table is **main**
- Which tables are **subordinates**
- The **join logic**
- The resulting **derived fields** used for AML detection

---

## 1. ✅ `insight_transaction_behavior`
**Scenarios Covered:**  
1 (Round Numbers), 5 (Rapid In-Out), 7 (Structuring), 11 (Bidirectional Txn), 19 (Balance Mismatch)

### 🔗 Source Tables:
- `Fact_Transaction`: **main**
- `Dim_Account`: sub
- `Dim_Customer`: sub
- `Dim_Time`: sub

### 🔁 Join Logic:
- `Fact_Transaction`  
  → **left join** `Dim_Customer` on `Customer_ID`  
  → **left join** `Dim_Account` on `From_Account_ID` = `Account_ID`  
  → **left join** `Dim_Time` on `Booking_Date` = `Date`

### 🧠 Derived Fields:
- `f_round_amount_flag`
- `f_structuring_flag`
- `f_bidirectional_txn_flag`
- `txn_inflow_outflow_ratio`
- `balance_mismatch_score`

---

## 2. ✅ `insight_account_activity`
**Scenarios Covered:**  
2 (Dormant Spike), 8 (Account Funnel), 9 (Unrelated Senders)

### 🔗 Source Tables:
- `Fact_Transaction`: **main**
- `Dim_Account`: sub
- `Dim_Customer`: sub

### 🔁 Join Logic:
- `Fact_Transaction`  
  → **left join** `Dim_Account` on `From_Account_ID`  
  → **left join** `Dim_Customer` on `Customer_ID`  
  → aggregate by `Account_ID`, over time window

### 🧠 Derived Fields:
- `f_dormant_now_active_flag`
- `f_multiple_accounts_flag`
- `txn_from_unrelated_entities_count`

---

## 3. ✅ `insight_geo_fx_pattern`
**Scenarios Covered:**  
3 (High-Risk Country), 15 (Excessive FX)

### 🔗 Source Tables:
- `Fact_Transaction`: **main**
- `Dim_Country`: sub
- `Fact_Forex_Transaction`: sub

### 🔁 Join Logic:
- `Fact_Transaction`  
  → **left join** `Dim_Country` on `Transaction.Country_Code = Country.Country_Code`  
- FX scenarios use `Fact_Forex_Transaction` separately by aggregation

### 🧠 Derived Fields:
- `f_high_risk_country_flag`
- `f_excessive_fx_conversion_flag`

---

## 4. ✅ `insight_customer_profile_change`
**Scenarios Covered:**  
4 (Synthetic Pairing), 10 (Early Loan Closure), 12 (Spending > Income)

### 🔗 Source Tables:
- `Fact_Transaction`: **main**
- `Fact_Loan_Repayment`: sub
- `Fact_Customer_Income`: sub
- `Dim_Customer`: sub

### 🔁 Join Logic:
- `Fact_Transaction`  
  → **left join** `Fact_Customer_Income` on `Customer_ID`  
  → **left join** `Dim_Customer` on `Customer_ID`  
  → **left join** `Fact_Loan_Repayment` on `Customer_ID` (filter for premature closure)

### 🧠 Derived Fields:
- `f_synthetic_pairing_flag`
- `f_early_loan_closure_flag`
- `f_high_txn_to_income_ratio_flag`

---

## 5. ✅ `insight_income_vs_obligation`
**Scenarios Covered:**  
6 (Unexplained Repayment), 13 (Collateral Mismatch)

### 🔗 Source Tables:
- `Fact_Customer_Income`: **main**
- `Fact_Loan_Repayment`: sub
- `Fact_Collateral_Assignment`: sub
- `Dim_Customer`: sub

### 🔁 Join Logic:
- `Fact_Customer_Income`  
  → **left join** `Fact_Loan_Repayment` on `Customer_ID`  
  → **left join** `Fact_Collateral_Assignment` on `Customer_ID`  
  → **left join** `Dim_Customer` on `Customer_ID`

### 🧠 Derived Fields:
- `f_unexpected_repayment_flag`
- `f_collateral_mismatch_flag`

---

## 6. ✅ `insight_kyc_linkage`
**Scenarios Covered:**  
14 (Duplicate ID / Shared Address)

### 🔗 Source Tables:
- `Dim_Customer`: **main**
- `Dim_KYC_Profile_Snapshot`: sub

### 🔁 Join Logic:
- `Dim_Customer`  
  → **left join** `Dim_KYC_Profile_Snapshot` on `Customer_ID`  
  → group by `ID_Number`, `Address`, count distinct `Customer_ID`

### 🧠 Derived Fields:
- `f_duplicate_id_flag`
- `f_shared_address_flag`

---

## 7. ✅ `insight_snapshot_drift`
**Scenarios Covered:**  
16 (KYC Drift), 17 (Job Hopping), 18 (Wealth Tier Fluctuation)

### 🔗 Source Tables:
- `Dim_KYC_Profile_Snapshot`: **main**
- `Dim_Employment`: sub
- `Dim_Customer_Wealth_Profile`: sub

### 🔁 Join Logic:
- `Dim_KYC_Profile_Snapshot`  
  → **left join** `Dim_Employment` on `Customer_ID`  
  → **left join** `Dim_Customer_Wealth_Profile` on `Customer_ID`  
  → window functions: lag, count distinct values across time

### 🧠 Derived Fields:
- `kyc_change_count_30d`
- `employment_change_count_90d`
- `wealth_tier_change_count_60d`

---

## 8. ✅ `insight_rule_snapshot_diff`
**Scenarios Covered:**  
20 (Rule Relaxation Before Alert)

### 🔗 Source Tables:
- `Dim_Compliance_Rule_Snapshot`: **main**
- `Fact_Alert`: sub

### 🔁 Join Logic:
- `Dim_Compliance_Rule_Snapshot`  
  → **left join** `Fact_Alert` on `Rule_ID`  
  → filter where `Alert_Timestamp - Rule_Effective_Date ≤ 2 days`

### 🧠 Derived Fields:
- `f_rule_relaxation_before_alert`

---