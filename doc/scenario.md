# 📘 AML Detection Scenarios (Business Logic)

Each detection rule includes:
- **Description** of the suspicious behavior  
- **Detection Logic** in simple rule terms  
- **Fields Involved** (table.column references)  
- **Example Behavior** that would trigger the alert

---

## 🔍 1. Round-Number Transactions

**Description:** Repetitive transfers of round numbers suggest structuring/layering.  
**Detection Logic:**  
- If ≥ 3 transactions in 7 days have `Amount` ending in all zeros → flag

**Fields Involved:**  
- `Fact_Transaction.Amount`  
- `Fact_Transaction.Booking_Date`

**Example:**  
- Day 1: 50,000,000 VND  
- Day 3: 100,000,000 VND  
- Day 6: 200,000,000 VND

---

## 🔍 2. High Velocity in Dormant Account

**Description:** Dormant account suddenly makes high-volume transfers.  
**Detection Logic:**  
- ≤1 txn/month in past 6 months, but ≥10 txns in 24h → flag

**Fields Involved:**  
- `Fact_Transaction.From_Account_ID`  
- `Fact_Transaction.Booking_Date`

**Example:**  
- 12 transfers in 6 hours from an account used monthly

---

## 🔍 3. Cross-Border High-Risk Jurisdictions

**Description:** Transactions to/from high-risk or sanctioned countries.  
**Detection Logic:**  
- ≥2 transactions to countries with `Risk_Level = 'HIGH'` in 30 days

**Fields Involved:**  
- `Fact_Transaction.Country_Code`  
- `Dim_Country.Sanctioned_Flag`  
- `Dim_Country.Risk_Level`

**Example:**  
- Transfers to Panama & Cayman Islands in 2 weeks

---

## 🔍 4. Synthetic Relationships Between Customers

**Description:** Sudden large transfers between previously unlinked customers.  
**Detection Logic:**  
- No txn history in 90 days → ≥3 txns totaling >50M VND in 7 days

**Fields Involved:**  
- `Fact_Transaction.From_Account_ID`  
- `Fact_Transaction.To_Account_ID`  
- `Fact_Transaction.Booking_Date`

**Example:**  
- Customer A and B exchange 20M VND multiple times in 1 week

---

## 🔍 5. Rapid In-Out Transactions

**Description:** Funds deposited and withdrawn quickly (layering).  
**Detection Logic:**  
- If ≥80% of incoming funds exit within 1 hour → flag

**Fields Involved:**  
- `Fact_Transaction.Amount`  
- `Booking_Date`, transaction timestamps

**Example:**  
- 150M VND in at 10:00 → 145M VND out by 10:40

---

## 🔍 6. Sudden Debt Repayment Beyond Income

**Description:** Customer repays large loan amount without matching income.  
**Detection Logic:**  
- Avg income ≤10M/month and full loan paid suddenly (>100M VND)

**Fields Involved:**  
- `Fact_Loan_Repayment.Amount`  
- `Fact_Customer_Income.Inflow_Amount`

**Example:**  
- Customer with 10M income/month repays 350M in one transaction

---

## 🔍 7. Structuring / Smurfing

**Description:** Large deposits split into smaller transactions.  
**Detection Logic:**  
- If total deposits >300M in 7d, each ≤100M → flag

**Fields Involved:**  
- `Fact_Transaction.Amount`  
- `Booking_Date`

**Example:**  
- 10 deposits of 30M across multiple branches in a week

---

## 🔍 8. Use of Multiple Accounts for Transfers

**Description:** Customer uses multiple linked accounts to move funds.  
**Detection Logic:**  
- ≥3 linked accounts involved in inter-account txns → flag

**Fields Involved:**  
- `Fact_Transaction.From_Account_ID`  
- `Fact_Transaction.To_Account_ID`  
- `Dim_Customer.Customer_ID`

**Example:**  
- A → B → C transfers all by same customer in one day

---

## 🔍 9. Transactions with Unrelated Individuals

**Description:** Funds received from unknown, non-related parties.  
**Detection Logic:**  
- ≥5 inbound txns from unknown senders in 7d → flag

**Fields Involved:**  
- `Fact_Transaction.To_Account_ID`  
- `From_Account_ID`, `Dim_Customer.Relationship_Type`

**Example:**  
- 5 transfers from unrelated customers in 5 days

---

## 🔍 10. Early Loan Closure with Unexplained Funds

**Description:** Loan closed earlier than scheduled without visible funding source.  
**Detection Logic:**  
- If loan is paid ≥30d before maturity and no income spike → flag

**Fields Involved:**  
- `Fact_Loan_Repayment.Closure_Date`  
- `Fact_Customer_Income.Inflow_Amount`  
- `Loan.Term_End_Date`

**Example:**  
- 2-year loan repaid in month 9 with no salary increase

---

## 🔍 11. Bidirectional Transfers Between Customers

**Description:** Customers send and return similar amounts in a short span.  
**Detection Logic:**  
- ≥2 transfers in both directions within 3 days, total > threshold

**Fields Involved:**  
- `Fact_Transaction.From_Account_ID`, `To_Account_ID`, `Booking_Date`

**Example:**  
- A sends 60M → B, then B sends 58M → A two days later

---

## 🔍 12. High Transaction-to-Income Ratio

**Description:** Customer spends significantly more than declared income.  
**Detection Logic:**  
- Outflows in a month > 5× monthly declared income → flag

**Fields Involved:**  
- `Fact_Transaction.Amount`  
- `Fact_Customer_Income.Inflow_Amount`

**Example:**  
- Income = 12M, outflow = 90M VND in one month

---

## 🔍 13. Collateral Mismatch with Customer Profile

**Description:** Low-income customers pledge high-value collateral.  
**Detection Logic:**  
- If income ≤10M and collateral pledged >5B → flag

**Fields Involved:**  
- `Fact_Collateral_Assignment.Collateral_Value`  
- `Fact_Customer_Income.Inflow_Amount`

**Example:**  
- Taxi driver pledges luxury condo valued at 6B VND

---

## 🔍 14. Multiple Customers Linked to Same ID or Address

**Description:** Shared ID or address among multiple customers.  
**Detection Logic:**  
- ≥3 customers share same ID or address → synthetic identity risk

**Fields Involved:**  
- `Dim_Customer.ID_Number`, `Dim_Customer.Address`

**Example:**  
- 5 customers share same passport number or apartment

---

## 🔍 15. Frequent Foreign Currency Exchange

**Description:** Excessive FX usage without known business or travel needs.  
**Detection Logic:**  
- ≥10 FX conversions in 7 days totaling >100M VND → flag

**Fields Involved:**  
- `Fact_Forex_Transaction.Amount`, `FX_Type`, `Booking_Date`

**Example:**  
- 12 USD exchanges worth 120M VND in 5 days

---

## 🔍 16. KYC Profile Drift Over Time

**Description:** KYC info changes multiple times in a short span.  
**Detection Logic:**  
- ≥3 field changes (address, income, ID) in 30 days → flag

**Fields Involved:**  
- `Dim_KYC_Profile_Snapshot.*`, `scd_change_timestamp`

**Example:**  
- New address, income level, and ID issued within 2 weeks

---

## 🔍 17. Frequent Employer Changes

**Description:** Rapid changes in employment data.  
**Detection Logic:**  
- ≥3 distinct employers in `Dim_Employment` in 90 days → flag

**Fields Involved:**  
- `Dim_Employment.Customer_ID`, `Employer_ID`, `Verification_Date`

**Example:**  
- Changed jobs 3 times in 2 months

---

## 🔍 18. Wealth Tier Fluctuation Without Explanation

**Description:** Moves up/down tiers rapidly with no justification.  
**Detection Logic:**  
- `Wealth_Tier` changes ≥2 times in 60 days → flag

**Fields Involved:**  
- `Dim_Customer_Wealth_Profile.Wealth_Tier`, `scd_change_timestamp`

**Example:**  
- HNW → Affluent → Mass within 45 days

---

## 🔍 19. Inconsistent Balance vs. Transactions

**Description:** Balance delta does not match expected net transactions.  
**Detection Logic:**  
- ∆ Balance ≠ Net inflow/outflow ±10% → anomaly

**Fields Involved:**  
- `Dim_Account_Balance_Snapshot.*`  
- `Fact_Transaction.*`

**Example:**  
- Balance rose by 1B but no inbound txns recorded

---

## 🔍 20. Rule Change Immediately Before Alert

**Description:** Rule logic was modified shortly before firing an alert.  
**Detection Logic:**  
- If `Dim_Compliance_Rule_Snapshot` changed within 48h before alert → escalate

**Fields Involved:**  
- `Dim_Compliance_Rule_Snapshot.scd_change_timestamp`  
- `Alert_Fact.Alert_Timestamp`

**Example:**  
- Threshold raised from 500M to 800M the day before a 750M txn alert