# 📘 AML Detection Scenarios (Business Logic)

Each detection rule includes:
- **Description** of the suspicious behavior  
- **Detection Logic** in simple rule terms  
- **Fields Involved** (table.column references)  
- **Example Behavior** that would trigger the alert  
- **Related Tables and Joins** used in detection logic  

---

## 🔍 1. Round-Number Transactions
**Description:** Repetitive transfers of round numbers suggest structuring/layering.  
**Detection Logic:**
- ≥ 3 transactions in 7 days have `Amount` ending in all zeros → flag  
**Fields Involved:**
- `Fact_Transaction.Amount`, `Fact_Transaction.Booking_Date`  
**Example:**
- 50M → 100M → 200M VND in a week  
**Related Tables and Joins:**
- `Fact_Transaction` only  

---

## 🔍 2. High Velocity in Dormant Account
**Description:** Dormant account suddenly makes high-volume transfers.  
**Detection Logic:**
- ≤1 txn/month in past 6 months, but ≥10 txns in 24h → flag  
**Fields Involved:**
- `Fact_Transaction.From_Account_ID`, `Fact_Transaction.Booking_Date`  
**Example:**
- 12 transfers in 6 hours from previously inactive account  
**Related Tables and Joins:**
- `Fact_Transaction`, optionally `Dim_Account` for activity tagging  

---

## 🔍 3. Cross-Border High-Risk Jurisdictions
**Description:** Transactions to/from high-risk or sanctioned countries.  
**Detection Logic:**
- ≥2 transactions to countries with `Risk_Level = 'HIGH'` in 30 days  
**Fields Involved:**
- `Fact_Transaction.Country_Code`, `Dim_Country.Sanctioned_Flag`, `Dim_Country.Risk_Level`  
**Example:**
- Transfers to Panama & Cayman Islands in 2 weeks  
**Related Tables and Joins:**
- `Fact_Transaction` JOIN `Dim_Country` ON `Country_Code`  

---

## 🔍 4. Synthetic Relationships Between Customers
**Description:** Sudden large transfers between previously unlinked customers.  
**Detection Logic:**
- ≥3 txns totaling >50M VND in 7 days without prior history  
**Fields Involved:**
- `Fact_Transaction.From_Account_ID`, `To_Account_ID`, `Booking_Date`  
**Example:**
- A ↔ B = 60M exchanged in a week  
**Related Tables and Joins:**
- `Fact_Transaction`, optionally linked with `Dim_Customer` for KYC  

---

## 🔍 5. Rapid In-Out Transactions
**Description:** Funds deposited and withdrawn quickly (layering).  
**Detection Logic:**
- ≥80% of incoming funds exit within 1 hour  
**Fields Involved:**
- `Fact_Transaction.Amount`, `Booking_Date`, timestamps  
**Example:**
- 150M in → 145M out within 40 mins  
**Related Tables and Joins:**
- `Fact_Transaction`, optionally with `Dim_Time`  

---

## 🔍 6. Sudden Debt Repayment Beyond Income
**Description:** Customer repays large loan amount without matching income.  
**Detection Logic:**
- Avg income ≤10M/month and repays loan >100M suddenly  
**Fields Involved:**
- `Fact_Loan_Repayment.Amount`, `Fact_Customer_Income.Inflow_Amount`  
**Example:**
- 350M repayment with 10M/month income  
**Related Tables and Joins:**
- `Fact_Loan_Repayment` JOIN `Fact_Customer_Income` ON `Customer_ID`  

---

## 🔍 7. Structuring / Smurfing
**Description:** Large deposits split into smaller transactions.  
**Detection Logic:**
- Total deposits >300M in 7 days, each ≤100M  
**Fields Involved:**
- `Fact_Transaction.Amount`, `Booking_Date`  
**Example:**
- 10×30M VND deposits  
**Related Tables and Joins:**
- `Fact_Transaction` only  

---

## 🔍 8. Use of Multiple Accounts for Transfers
**Description:** Customer uses multiple accounts to move funds.  
**Detection Logic:**
- ≥3 linked accounts used in inter-account txns  
**Fields Involved:**
- `Fact_Transaction.From_Account_ID`, `To_Account_ID`, `Dim_Customer.Customer_ID`  
**Example:**
- A → B → C transfers by same person  
**Related Tables and Joins:**
- `Fact_Transaction` JOIN `Dim_Customer_Account` or ownership view  

---

## 🔍 9. Transactions with Unrelated Individuals
**Description:** Funds received from unrelated or unknown parties.  
**Detection Logic:**
- ≥5 inbound txns from unrelated senders in 7d  
**Fields Involved:**
- `Fact_Transaction.To_Account_ID`, `From_Account_ID`, `Dim_Customer.Relationship_Type`  
**Example:**
- 5+ unrelated transfers in 5 days  
**Related Tables and Joins:**
- `Fact_Transaction` JOIN `Dim_Customer` ON both From & To sides  

---

## 🔍 10. Early Loan Closure with Unexplained Funds
**Description:** Loan closed early with no visible income source.  
**Detection Logic:**
- Closure ≥30d early and no income spike  
**Fields Involved:**
- `Fact_Loan_Repayment.Closure_Date`, `Fact_Customer_Income.Inflow_Amount`, `Loan.Term_End_Date`  
**Example:**
- 2-yr loan closed at 9 months  
**Related Tables and Joins:**
- `Fact_Loan_Repayment` JOIN `Fact_Customer_Income` JOIN `Dim_Loan`  

---

## 🔍 11. Bidirectional Transfers Between Customers
**Description:** Customers send and return funds within short time.  
**Detection Logic:**
- ≥2 transfers both ways in 3 days  
**Fields Involved:**
- `Fact_Transaction.From_Account_ID`, `To_Account_ID`, `Booking_Date`  
**Example:**
- A → B → A in 2 days  
**Related Tables and Joins:**
- `Fact_Transaction`  

---

## 🔍 12. High Transaction-to-Income Ratio
**Description:** Outflows far exceed declared income.  
**Detection Logic:**
- Outflow > 5× income in one month  
**Fields Involved:**
- `Fact_Transaction.Amount`, `Fact_Customer_Income.Inflow_Amount`  
**Example:**
- 90M outflow with 12M income  
**Related Tables and Joins:**
- `Fact_Transaction` JOIN `Fact_Customer_Income`  

---

## 🔍 13. Collateral Mismatch with Customer Profile
**Description:** Low-income customer pledges valuable assets.  
**Detection Logic:**
- Income ≤10M and collateral >5B  
**Fields Involved:**
- `Fact_Collateral_Assignment.Collateral_Value`, `Fact_Customer_Income.Inflow_Amount`  
**Example:**
- 6B condo with 10M income  
**Related Tables and Joins:**
- `Fact_Collateral_Assignment` JOIN `Fact_Customer_Income`  

---

## 🔍 14. Multiple Customers Linked to Same ID or Address
**Description:** Shared identity/address across customers.  
**Detection Logic:**
- ≥3 customers share ID or address  
**Fields Involved:**
- `Dim_Customer.ID_Number`, `Address`  
**Example:**
- 5 customers with same passport or apartment  
**Related Tables and Joins:**
- `Dim_Customer` self-join on `ID_Number` or `Address`  

---

## 🔍 15. Frequent Foreign Currency Exchange
**Description:** Excessive FX transactions in short period.  
**Detection Logic:**
- ≥10 FX conversions in 7 days totaling >100M  
**Fields Involved:**
- `Fact_Forex_Transaction.Amount`, `FX_Type`, `Booking_Date`  
**Example:**
- 12 USD exchanges worth 120M in 5 days  
**Related Tables and Joins:**
- `Fact_Forex_Transaction`, optionally `Dim_Customer`  

---

## 🔍 16. KYC Profile Drift Over Time
**Description:** Too many changes to KYC fields recently.  
**Detection Logic:**
- ≥3 KYC field changes in 30 days  
**Fields Involved:**
- `Dim_KYC_Profile_Snapshot.*`, `scd_change_timestamp`  
**Example:**
- New address, ID, income in 2 weeks  
**Related Tables and Joins:**
- `Dim_KYC_Profile_Snapshot`, `Dim_Customer`  

---

## 🔍 17. Frequent Employer Changes
**Description:** Many employer changes in short time.  
**Detection Logic:**
- ≥3 employers in 90 days  
**Fields Involved:**
- `Dim_Employment.Customer_ID`, `Employer_ID`, `Verification_Date`  
**Example:**
- 3 jobs in 2 months  
**Related Tables and Joins:**
- `Dim_Employment`, `Dim_Customer`  

---

## 🔍 18. Wealth Tier Fluctuation Without Explanation
**Description:** Wealth tier rises/falls rapidly.  
**Detection Logic:**
- ≥2 tier changes in 60 days  
**Fields Involved:**
- `Dim_Customer_Wealth_Profile.Wealth_Tier`, `scd_change_timestamp`  
**Example:**
- HNW → Mass in 45 days  
**Related Tables and Joins:**
- `Dim_Customer_Wealth_Profile`, `Dim_Customer`  

---

## 🔍 19. Inconsistent Balance vs. Transactions
**Description:** Balance does not match net flows.  
**Detection Logic:**
- ∆Balance ≠ Net inflow/outflow ±10%  
**Fields Involved:**
- `Dim_Account_Balance_Snapshot.*`, `Fact_Transaction.*`  
**Example:**
- Balance rose by 1B with no inflows  
**Related Tables and Joins:**
- `Dim_Account_Balance_Snapshot` JOIN `Fact_Transaction` ON `Account_ID`  

---

## 🔍 20. Rule Change Immediately Before Alert
**Description:** Rule edited just before alert was triggered.  
**Detection Logic:**
- Rule changed within 48h before alert  
**Fields Involved:**
- `Dim_Compliance_Rule_Snapshot.scd_change_timestamp`, `Alert_Fact.Alert_Timestamp`  
**Example:**
- Threshold changed the day before alert  
**Related Tables and Joins:**
- `Dim_Compliance_Rule_Snapshot` JOIN `Alert_Fact` ON rule_id or time proximity  

