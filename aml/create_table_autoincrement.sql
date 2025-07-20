CREATE TABLE "Dim_Customer" (
  "Customer_ID" SERIAL PRIMARY KEY,
  "Name" varchar,
  "DOB" date,
  "Nationality" varchar,
  "Income_Level" decimal,
  "PEP_Flag" boolean,
  "Marital_Status" varchar,
  "Industry_Code" varchar,
  "ID_Type" varchar,
  "ID_Number" varchar,
  "Address" varchar,
  "Phone" varchar,
  "Email" varchar,
  "Customer_Open_Date" date,
  "Branch_ID" INTEGER
);

CREATE TABLE "Dim_Account" (
  "Account_ID" SERIAL PRIMARY KEY,
  "Customer_ID" INTEGER,
  "Account_Type" varchar,
  "Open_Date" date,
  "Close_Date" date,
  "Account_Status" varchar,
  "Currency" INTEGER,
  "Branch_ID" INTEGER
);

CREATE TABLE "Dim_Transaction_Type" (
  "Transaction_Type_ID" SERIAL PRIMARY KEY,
  "Transaction_Code" varchar,
  "Description" varchar
);

CREATE TABLE "Dim_Country" (
  "Country_Code" SERIAL PRIMARY KEY,
  "Country_Name" varchar,
  "Risk_Level" varchar,
  "Sanctioned_Flag" boolean
);

CREATE TABLE "Dim_Channel" (
  "Channel_ID" SERIAL PRIMARY KEY,
  "Channel_Code" varchar,
  "Channel_Name" varchar,
  "Digital_Flag" boolean
);

CREATE TABLE "Dim_Time" (
  "Date_ID" date PRIMARY KEY,
  "Year" int,
  "Month" int,
  "Quarter" int,
  "Week" int,
  "Day_of_Week" varchar
);

CREATE TABLE "Dim_Risk_Level" (
  "Risk_Level_ID" SERIAL PRIMARY KEY,
  "Level_Name" varchar,
  "Score_Threshold" int,
  "Description" varchar
);

CREATE TABLE "Dim_Alert_Type" (
  "Alert_Type_ID" SERIAL PRIMARY KEY,
  "Scenario_Name" varchar,
  "Detection_Rule" text,
  "Severity_Level" varchar
);

CREATE TABLE "Dim_PEP_List" (
  "National_ID" varchar PRIMARY KEY,
  "Name" varchar,
  "Country" varchar,
  "Position" varchar,
  "Last_Verified_Date" date
);

CREATE TABLE "Dim_KYC_Event" (
  "KYC_Event_ID" SERIAL PRIMARY KEY,
  "Customer_ID" INTEGER,
  "Change_Type" varchar,
  "Old_Value" text,
  "New_Value" text,
  "Change_Date" date
);

CREATE TABLE "Dim_Branch" (
  "Branch_ID" SERIAL PRIMARY KEY,
  "Branch_Code" varchar,
  "Branch_Name" varchar,
  "Region" varchar,
  "Open_Date" date
);

CREATE TABLE "Dim_Employment" (
  "Employer_ID" SERIAL PRIMARY KEY,
  "Customer_ID" INTEGER,
  "Job_Title" varchar,
  "Company_Name" varchar,
  "Industry" varchar,
  "Income_Source" varchar,
  "Verification_Date" date
);

CREATE TABLE "Dim_Transaction_Reason" (
  "Reason_Code" SERIAL PRIMARY KEY,
  "Reason_Desc" varchar,
  "Risk_Level" varchar
);

CREATE TABLE "Dim_Party" (
  "Party_ID" SERIAL PRIMARY KEY,
  "Party_Type" varchar,
  "Party_Name" varchar,
  "Registration_Number" varchar,
  "Country" varchar,
  "Address" varchar,
  "Status" varchar,
  "Is_Customer_Flag" boolean
);

CREATE TABLE "Dim_Party_Role" (
  "Role_ID" SERIAL PRIMARY KEY,
  "Role_Name" varchar,
  "Description" varchar
);

CREATE TABLE "Dim_Collateral_Type" (
  "Collateral_Type_ID" SERIAL PRIMARY KEY,
  "Name" varchar,
  "Category" varchar,
  "Liquidity_Score" int,
  "Accepted_For_Loan_Flag" boolean
);

CREATE TABLE "Dim_Asset" (
  "Asset_ID" SERIAL PRIMARY KEY,
  "Asset_Type" INTEGER,
  "Description" varchar,
  "Registration_No" varchar,
  "Currency" INTEGER,
  "Purchase_Date" date,
  "Customer_ID" INTEGER,
  "Country" INTEGER,
  "Asset_Status" varchar
);

CREATE TABLE "Dim_Customer_Asset_Ownership" (
  "Customer_ID" INTEGER,
  "Asset_ID" INTEGER,
  "Ownership_Type" varchar,
  "Ownership_Percentage" decimal,
  "Declaration_Date" date
);

CREATE TABLE "Dim_Customer_Wealth_Profile" (
  "Customer_ID" INTEGER PRIMARY KEY,
  "Date_ID" date,
  "Total_Balance" decimal,
  "Total_Assets" decimal,
  "Estimated_Income" decimal,
  "Loan_Exposure" decimal,
  "Wealth_Tier" varchar
);

CREATE TABLE "Dim_Account_Balance_Snapshot" (
  "Account_ID" SERIAL PRIMARY KEY,
  "Customer_ID" INTEGER,
  "Balance_Date" date,
  "Current_Balance" decimal,
  "Available_Balance" decimal,
  "Currency" INTEGER,
  "Account_Status" varchar,
  "Overdraft_Limit" decimal,
  "Branch_ID" INTEGER
);

CREATE TABLE "Dim_KYC_Profile_Snapshot" (
  "Customer_ID" INTEGER PRIMARY KEY,
  "Name" varchar,
  "DOB" date,
  "Nationality" varchar,
  "ID_Type" varchar,
  "ID_Number" varchar,
  "Address" varchar,
  "Income_Level" decimal,
  "Marital_Status" varchar,
  "Phone" varchar,
  "Email" varchar,
  "Customer_Open_Date" date,
  "PEP_Flag" boolean
);

CREATE TABLE "Dim_Compliance_Rule_Snapshot" (
  "Rule_ID" SERIAL PRIMARY KEY,
  "Rule_Name" varchar,
  "Rule_SQL" text,
  "Severity_Level" varchar,
  "Thresholds" varchar,
  "Effective_Date" date,
  "Rule_Group" varchar,
  "Is_Enabled" boolean
);

CREATE TABLE "Dim_Currency" (
  "Currency_Code" SERIAL PRIMARY KEY,
  "Currency_Name" varchar,
  "ISO_Code" varchar,
  "FX_Rate" decimal,
  "Effective_Date" date,
  "Is_Active" boolean
);

CREATE TABLE "Hist_Dim_Employment" (
  "Employer_ID" varchar,
  "Customer_ID" INTEGER,
  "Job_Title" varchar,
  "Company_Name" varchar,
  "Industry" varchar,
  "Income_Source" varchar,
  "Verification_Date" date,
  "ds_partition_date" date
);

CREATE TABLE "Fact_Transaction" (
  "Transaction_ID" SERIAL PRIMARY KEY,
  "From_Account_ID" INTEGER,
  "To_Account_ID" INTEGER,
  "Amount" decimal,
  "Transaction_Type_ID" INTEGER,
  "Booking_Date" date,
  "Channel_ID" INTEGER,
  "Country_Code" INTEGER,
  "Transaction_Reason" INTEGER,
  "Currency" INTEGER
);

CREATE TABLE "Fact_Loan_Repayment" (
  "Loan_ID" SERIAL PRIMARY KEY,
  "Customer_ID" INTEGER,
  "Repayment_Date" date,
  "Repayment_Amount" decimal,
  "Principal_Component" decimal,
  "Interest_Component" decimal,
  "Repayment_Method" varchar,
  "Remaining_Balance" decimal
);

CREATE TABLE "Fact_Card_Transaction" (
  "Card_Txn_ID" SERIAL PRIMARY KEY,
  "Card_ID" varchar,
  "Customer_ID" INTEGER,
  "Txn_Date" date,
  "Amount" decimal,
  "Merchant" varchar,
  "Country" varchar,
  "Channel_ID" INTEGER,
  "Txn_Type" varchar
);

CREATE TABLE "Fact_Deposit" (
  "Deposit_ID" SERIAL PRIMARY KEY,
  "Customer_ID" INTEGER,
  "Deposit_Type" varchar,
  "Start_Date" date,
  "Maturity_Date" date,
  "Amount" decimal,
  "Interest_Rate" decimal,
  "Branch_ID" INTEGER
);

CREATE TABLE "Fact_Cash_Deposit_Withdrawal" (
  "Txn_ID" SERIAL PRIMARY KEY,
  "Account_ID" INTEGER,
  "Txn_Date" date,
  "Txn_Type" varchar,
  "Amount" decimal,
  "Channel" varchar,
  "Location" varchar,
  "Handled_By" varchar
);

CREATE TABLE "Fact_Customer_Balance" (
  "Customer_ID" INTEGER,
  "Account_ID" INTEGER,
  "Date_ID" date,
  "Closing_Balance" decimal,
  "Currency" INTEGER
);

CREATE TABLE "Fact_Customer_Income" (
  "Customer_ID" INTEGER,
  "Month" date,
  "Inflow_Amount" decimal,
  "Inflow_Source" varchar,
  "Income_Type" varchar,
  "Estimation_Method" varchar
);

CREATE TABLE "Fact_Alert" (
  "Alert_ID" SERIAL PRIMARY KEY,
  "Customer_ID" INTEGER,
  "Alert_Type_ID" INTEGER,
  "Triggered_On" date,
  "Triggered_By_Rule" INTEGER,
  "Severity" varchar,
  "Status" varchar,
  "Review_Outcome" varchar
);

CREATE TABLE "Fact_Risk_Score" (
  "Customer_ID" INTEGER,
  "Score_Date" date,
  "Score_Value" decimal,
  "Score_Band" varchar,
  "Driving_Rules" text,
  "Override_Flag" boolean
);

CREATE TABLE "Fact_Transaction_Peer_Pair" (
  "From_Customer_ID" INTEGER,
  "To_Customer_ID" INTEGER,
  "Window_Days" int,
  "Txn_Count" int,
  "Total_Amount" decimal,
  "First_Txn_Date" date,
  "Bidirectional_Flag" boolean
);

CREATE TABLE "Fact_Collateral_Assignment" (
  "Loan_ID" INTEGER,
  "Collateral_ID" INTEGER,
  "Customer_ID" INTEGER,
  "Assigned_Date" date,
  "Collateral_Value" decimal,
  "Current_Value" decimal,
  "LTV" decimal,
  "Currency" INTEGER
);

CREATE TABLE "Fact_Asset_Valuation" (
  "Asset_ID" INTEGER,
  "Valuation_Date" date,
  "Valuation_Amount" decimal,
  "Source" varchar,
  "Valuation_Type" varchar,
  "Currency" INTEGER
);

CREATE TABLE "Fact_Party_Linkage" (
  "Customer_ID" INTEGER,
  "Party_ID" INTEGER,
  "Link_Type" varchar,
  "Link_Evidence" text,
  "Relationship_Start" date,
  "Confidence_Score" decimal
);

CREATE TABLE "Fact_Customer_Wealth_Profile" (
  "Customer_ID" INTEGER,
  "Date_ID" date,
  "Total_Balance" decimal,
  "Total_Assets" decimal,
  "Estimated_Income" decimal,
  "Loan_Exposure" decimal,
  "Wealth_Tier" varchar
);

CREATE TABLE "Fact_KYC_Change_Log" (
  "Customer_ID" INTEGER,
  "Change_Field" varchar,
  "Old_Value" text,
  "New_Value" text,
  "Change_Timestamp" timestamp,
  "Change_Reason" varchar,
  "Initiated_By" varchar
);

ALTER TABLE "Dim_Risk_Level" ADD CONSTRAINT uq_level_name UNIQUE ("Level_Name");
ALTER TABLE "Dim_Customer" ADD CONSTRAINT uq_id_number UNIQUE ("ID_Number");
ALTER TABLE "Dim_Party_Role" ADD CONSTRAINT uq_role_name UNIQUE ("Role_Name");
ALTER TABLE "Dim_Asset" ADD CONSTRAINT uq_asset_type UNIQUE ("Asset_Type");

ALTER TABLE "Dim_Account" ADD FOREIGN KEY ("Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Fact_Transaction" ADD FOREIGN KEY ("From_Account_ID") REFERENCES "Dim_Account" ("Account_ID");

ALTER TABLE "Fact_Transaction" ADD FOREIGN KEY ("To_Account_ID") REFERENCES "Dim_Account" ("Account_ID");

ALTER TABLE "Fact_Transaction" ADD FOREIGN KEY ("Transaction_Type_ID") REFERENCES "Dim_Transaction_Type" ("Transaction_Type_ID");

ALTER TABLE "Fact_Transaction" ADD FOREIGN KEY ("Channel_ID") REFERENCES "Dim_Channel" ("Channel_ID");

ALTER TABLE "Fact_Transaction" ADD FOREIGN KEY ("Country_Code") REFERENCES "Dim_Country" ("Country_Code");

ALTER TABLE "Fact_Transaction" ADD FOREIGN KEY ("Currency") REFERENCES "Dim_Currency" ("Currency_Code");

ALTER TABLE "Dim_Account" ADD FOREIGN KEY ("Currency") REFERENCES "Dim_Currency" ("Currency_Code");

ALTER TABLE "Fact_Customer_Balance" ADD FOREIGN KEY ("Currency") REFERENCES "Dim_Currency" ("Currency_Code");

ALTER TABLE "Fact_Collateral_Assignment" ADD FOREIGN KEY ("Currency") REFERENCES "Dim_Currency" ("Currency_Code");

ALTER TABLE "Fact_Asset_Valuation" ADD FOREIGN KEY ("Currency") REFERENCES "Dim_Currency" ("Currency_Code");

ALTER TABLE "Fact_Loan_Repayment" ADD FOREIGN KEY ("Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Fact_Customer_Balance" ADD FOREIGN KEY ("Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Fact_Customer_Balance" ADD FOREIGN KEY ("Account_ID") REFERENCES "Dim_Account" ("Account_ID");

ALTER TABLE "Fact_Customer_Balance" ADD FOREIGN KEY ("Date_ID") REFERENCES "Dim_Time" ("Date_ID");

ALTER TABLE "Fact_Alert" ADD FOREIGN KEY ("Alert_Type_ID") REFERENCES "Dim_Alert_Type" ("Alert_Type_ID");

ALTER TABLE "Fact_Alert" ADD FOREIGN KEY ("Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Fact_Risk_Score" ADD FOREIGN KEY ("Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Fact_Transaction_Peer_Pair" ADD FOREIGN KEY ("From_Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Fact_Transaction_Peer_Pair" ADD FOREIGN KEY ("To_Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Fact_Collateral_Assignment" ADD FOREIGN KEY ("Collateral_ID") REFERENCES "Dim_Asset" ("Asset_ID");

ALTER TABLE "Fact_Collateral_Assignment" ADD FOREIGN KEY ("Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Fact_Asset_Valuation" ADD FOREIGN KEY ("Asset_ID") REFERENCES "Dim_Asset" ("Asset_ID");

ALTER TABLE "Fact_Party_Linkage" ADD FOREIGN KEY ("Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Fact_Party_Linkage" ADD FOREIGN KEY ("Party_ID") REFERENCES "Dim_Party" ("Party_ID");

ALTER TABLE "Fact_Customer_Wealth_Profile" ADD FOREIGN KEY ("Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Fact_Customer_Wealth_Profile" ADD FOREIGN KEY ("Date_ID") REFERENCES "Dim_Time" ("Date_ID");

ALTER TABLE "Fact_KYC_Change_Log" ADD FOREIGN KEY ("Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Dim_Customer" ADD FOREIGN KEY ("Branch_ID") REFERENCES "Dim_Branch" ("Branch_ID");

ALTER TABLE "Dim_Asset" ADD FOREIGN KEY ("Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Dim_Customer_Asset_Ownership" ADD FOREIGN KEY ("Asset_ID") REFERENCES "Dim_Asset" ("Asset_ID");

ALTER TABLE "Dim_Customer_Asset_Ownership" ADD FOREIGN KEY ("Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Dim_Employment" ADD FOREIGN KEY ("Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Dim_KYC_Event" ADD FOREIGN KEY ("Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Fact_Customer_Income" ADD FOREIGN KEY ("Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Fact_Cash_Deposit_Withdrawal" ADD FOREIGN KEY ("Account_ID") REFERENCES "Dim_Account" ("Account_ID");

ALTER TABLE "Fact_Deposit" ADD FOREIGN KEY ("Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Fact_Card_Transaction" ADD FOREIGN KEY ("Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Fact_Card_Transaction" ADD FOREIGN KEY ("Channel_ID") REFERENCES "Dim_Channel" ("Channel_ID");

ALTER TABLE "Fact_Transaction" ADD FOREIGN KEY ("Transaction_Reason") REFERENCES "Dim_Transaction_Reason" ("Reason_Code");

ALTER TABLE "Fact_Risk_Score" ADD FOREIGN KEY ("Score_Band") REFERENCES "Dim_Risk_Level" ("Level_Name");

ALTER TABLE "Dim_PEP_List" ADD FOREIGN KEY ("National_ID") REFERENCES "Dim_Customer" ("ID_Number");

ALTER TABLE "Fact_Party_Linkage" ADD FOREIGN KEY ("Link_Type") REFERENCES "Dim_Party_Role" ("Role_Name");

ALTER TABLE "Dim_Asset" ADD FOREIGN KEY ("Asset_Type") REFERENCES "Dim_Collateral_Type" ("Collateral_Type_ID");

ALTER TABLE "Dim_Account_Balance_Snapshot" ADD FOREIGN KEY ("Account_ID") REFERENCES "Dim_Account" ("Account_ID");

ALTER TABLE "Dim_Account_Balance_Snapshot" ADD FOREIGN KEY ("Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Dim_KYC_Profile_Snapshot" ADD FOREIGN KEY ("Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Hist_Dim_Employment" ADD FOREIGN KEY ("Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Fact_Alert" ADD FOREIGN KEY ("Triggered_By_Rule") REFERENCES "Dim_Compliance_Rule_Snapshot" ("Rule_ID");

ALTER TABLE "Dim_Customer_Wealth_Profile" ADD FOREIGN KEY ("Customer_ID") REFERENCES "Dim_Customer" ("Customer_ID");

ALTER TABLE "Dim_Customer_Wealth_Profile" ADD FOREIGN KEY ("Date_ID") REFERENCES "Dim_Time" ("Date_ID");