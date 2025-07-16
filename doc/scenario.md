# 📘 AML Detection Scenarios (Business Logic)

Below is a comprehensive list of **Anti-Money Laundering (AML) detection scenarios**. Each includes a **short description**, **business logic rule**, and **sample examples** that illustrate how it may appear in real transaction behavior.

---

## 🔍 1. Round-Number Transactions
**Description:** Customer repeatedly sends or receives amounts like 50,000,000 VND or 100,000,000 VND. These amounts often signal structuring or layering of illicit funds.  
**Rule:**  
- If ≥ 3 transactions in 7 days have amount ending in all zeros → flag for possible layering

**Examples:**
- Day 1: Transfer of 50,000,000 VND to account A  
- Day 3: Transfer of 100,000,000 VND to account B  
- Day 6: Transfer of 200,000,000 VND to account C

---

## 🔍 2. High Velocity in Dormant Account
**Description:** Inactive account suddenly initiates many transactions in a short period, possibly used as a mule or pass-through.  
**Rule:**  
- If account had ≤ 1 txn/month (last 6 months), but ≥ 10 txns in 24h → suspicious activity

**Examples:**
- A savings account that was used once a month suddenly makes 12 transfers within 6 hours  
- 8 different recipients receive between 5–15M VND each in one day

---

## 🔍 3. Cross-Border High-Risk Jurisdictions
**Description:** Transactions to/from sanctioned or high-risk countries (e.g., Iran, North Korea, Panama)  
**Rule:**  
- If ≥ 2 txns to high-risk countries in 30 days → trigger alert

**Examples:**
- Remittance of 80M VND to Panama and 50M VND to Cayman Islands  
- Receiving 70M VND from a shell company in Syria

---

## 🔍 4. Synthetic Relationships Between Customers
**Description:** Two customers with no prior interaction suddenly exchange large funds  
**Rule:**  
- No txn history in 90d, then ≥ 3 txns + total > 50M VND in 7d → flag

**Examples:**
- Customer A and B each transfer 20M VND to the other 3 times in a week  
- No business, family, or location link found between them

---

## 🔍 5. Rapid In-Out Transactions (Layering)
**Description:** Funds enter and quickly exit account, sometimes within minutes  
**Rule:**  
- If 80%+ of incoming amount is transferred out within 1 hour → high suspicion

**Examples:**
- 150M VND deposited at 10:00 AM, then 145M VND transferred to 3 other accounts by 10:40 AM

---

## 🔍 6. Sudden Debt Repayment Beyond Known Income
**Description:** Customer with low declared income pays off full loan amount unexpectedly  
**Rule:**  
- Avg income ≤ 10M VND/mo, normally pays interest only, suddenly repays full debt (>100M VND) → trigger

**Examples:**
- Salary ~10M VND/month, typically pays 5M interest  
- Suddenly repays 350M loan principal in one transaction

---

## 🔍 7. Structuring / Smurfing
**Description:** Large amount split into many small deposits to avoid regulatory thresholds  
**Rule:**  
- If total deposits in 7 days > 300M VND, with no single deposit > 100M → possible structuring

**Examples:**
- 10 deposits of 30M VND across 3 different branches  
- Daily ATM cash deposits of 50M VND over a week

---

## 🔍 8. Use of Multiple Accounts for Transfers
**Description:** Customer uses multiple internal accounts to shuffle or split funds  
**Rule:**  
- If customer linked to ≥ 3 accounts with interlinked txns → monitor for funneling

**Examples:**
- Account A → B → C within same day, all owned by same ID  
- Same IP or device used for all accounts

---

## 🔍 9. Transactions with Unrelated Individuals
**Description:** Customer receives multiple payments from unrelated or unknown persons  
**Rule:**  
- If ≥ 5 txns from non-family senders in 7 days → flag for review

**Examples:**
- Receives 5 transfers from 5 different individuals not in known relationship/KYC  
- No invoice, contract, or business reason

---

## 🔍 10. Early Loan Closure with Unexplained Funds
**Description:** Loan is paid off much earlier than expected, without declared income or asset sale  
**Rule:**  
- If full repayment + closure occurs 30+ days before maturity and no salary spike → alert

**Examples:**
- 2-year loan repaid fully in month 9 with no salary increase, no asset liquidation on record

---

## 🔍 11. Bidirectional Transfers Between Customers
**Description:** Two customers send money back and forth, possibly layering or laundering  
**Rule:**  
- If ≥ 2 txns in both directions within 3 days + total > threshold → flag

**Examples:**
- A sends 60M VND to B on Monday  
- B sends 58M VND back to A on Wednesday

---

## 🔍 12. High Transaction-to-Income Ratio
**Description:** Spending or transfers exceed income by wide margin  
**Rule:**  
- If monthly outflow > 5× declared income → unexplained wealth → flag

**Examples:**
- Income: 12M VND/month, total transfers: 90M VND in same month  
- No matching inflows from salary or asset sale

---

## 🔍 13. Use of Collateral Mismatched with Customer Profile
**Description:** Low-income individual pledges high-value asset for a loan  
**Rule:**  
- If customer income ≤ 10M/month but pledges house worth >5B VND → escalate

**Examples:**
- Taxi driver pledges luxury condo worth 6B VND  
- No prior asset declaration or title history

---

## 🔍 14. Multiple Customers Linked to Same ID or Address
**Description:** Possible fraud ring or synthetic identities  
**Rule:**  
- ≥ 3 customers with same ID/Address → synthetic ID or fraud ring risk

**Examples:**
- 5 customer accounts linked to same National ID or apartment number  
- All opened within 1 week timeframe

---

## 🔍 15. Frequent Foreign Currency Exchange
**Description:** Excessive FX activity without stated purpose (travel, business)  
**Rule:**  
- If ≥ 10 FX conversions in 7 days, total > 100M VND → possible laundering

**Examples:**
- 12 USD/VND exchanges totaling 120M VND in 5 days  
- No overseas travel history or declared FX usage