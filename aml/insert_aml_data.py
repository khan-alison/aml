import uuid
import random
from faker import Faker
from datetime import datetime, timedelta, date

fake = Faker()

# Storage for FK values
state = {}
state['next_id'] = {}

def get_next_id(table):
    if table not in state['next_id']:
        state['next_id'][table] = 1
    id_ = state['next_id'][table]
    state['next_id'][table] += 1
    return id_

def random_currency():
    return random.choice(state["currency_codes"])

def random_date(start_year=2020, end_year=2024):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return fake.date_between(start_date=start, end_date=end)

def random_datetime(start_year=2020, end_year=2024):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return fake.date_time_between(start_date=start, end_date=end)

def format_sql_value(val):
    if val is None:
        return 'NULL'
    if isinstance(val, str):
        return f"'{val.replace("'", "''")}'"
    if isinstance(val, bool):
        return 'TRUE' if val else 'FALSE'
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, datetime):
        return f"'{val.strftime('%Y-%m-%d %H:%M:%S')}'"
    if isinstance(val, date):
        return f"'{val.strftime('%Y-%m-%d')}'"
    raise ValueError(f"Unsupported value type: {type(val)}")

def generate_insert_sql(file, table, columns, values):
    cols_str = ", ".join(f'"{col}"' for col in columns)
    vals_str = ", ".join(format_sql_value(v) for v in values)
    sql = f'INSERT INTO "{table}" ({cols_str}) VALUES ({vals_str});'
    file.write(sql + '\n')
    print(f"✔ Generated insert for {table}")

def generate_insert_multiple_sql(file, table, columns, values_list):
    for values in values_list:
        generate_insert_sql(file, table, columns, values)
    print(f"✔ Generated {len(values_list)} inserts for {table}")

# Open output file
with open("generate_data.sql", "w") as f:
    # 1. Dim_Country (multiple countries)
    countries = []
    state["country_codes"] = []
    for i in range(10):
        country_code = get_next_id("Dim_Country")
        state["country_codes"].append(country_code)
        countries.append([
            country_code,
            fake.country(),
            random.choice(["Low", "Medium", "High"]),
            random.choice([True, False])
        ])
    state["Country_Code"] = state["country_codes"][0]  # Primary country
    generate_insert_multiple_sql(f, "Dim_Country", ["Country_Code", "Country_Name", "Risk_Level", "Sanctioned_Flag"], countries)

    # 2. Dim_Risk_Level (multiple risk levels)
    risk_levels = []
    state["risk_level_names"] = ["Low", "Medium", "High", "Critical"]
    for i, level in enumerate(state["risk_level_names"]):
        risk_level_id = get_next_id("Dim_Risk_Level")
        risk_levels.append([
            risk_level_id,
            level,
            (i + 1) * 25,
            f"{level} risk category"
        ])
    state["Score_Band"] = "Medium"
    generate_insert_multiple_sql(f, "Dim_Risk_Level", ["Risk_Level_ID", "Level_Name", "Score_Threshold", "Description"], risk_levels)

    # 3. Dim_Transaction_Type (multiple types)
    transaction_types = []
    state["transaction_type_ids"] = []
    type_codes = ["TT01", "TT02", "TT03", "TT04", "TT05"]
    descriptions = ["Wire Transfer", "ACH Transfer", "Card Payment", "Cash Deposit", "Loan Payment"]
    for code, desc in zip(type_codes, descriptions):
        txn_type_id = get_next_id("Dim_Transaction_Type")
        state["transaction_type_ids"].append(txn_type_id)
        transaction_types.append([txn_type_id, code, desc])
    state["Transaction_Type_ID"] = state["transaction_type_ids"][0]
    generate_insert_multiple_sql(f, "Dim_Transaction_Type", ["Transaction_Type_ID", "Transaction_Code", "Description"], transaction_types)

    # 4. Dim_Channel (multiple channels)
    channels = []
    state["channel_ids"] = []
    channel_data = [
        ("CH01", "Mobile App", True),
        ("CH02", "Internet Banking", True),
        ("CH03", "Branch", False),
        ("CH04", "ATM", False),
        ("CH05", "Phone Banking", False)
    ]
    for code, name, digital in channel_data:
        channel_id = get_next_id("Dim_Channel")
        state["channel_ids"].append(channel_id)
        channels.append([channel_id, code, name, digital])
    state["Channel_ID"] = state["channel_ids"][0]
    generate_insert_multiple_sql(f, "Dim_Channel", ["Channel_ID", "Channel_Code", "Channel_Name", "Digital_Flag"], channels)

    # 5. Dim_Currency (multiple currencies)
    currencies = []
    state["currency_codes"] = []
    currency_data = [
        ("US Dollar", "USD", 1.0),
        ("Euro", "EUR", 0.85),
        ("Vietnamese Dong", "VND", 24000.0),
        ("Japanese Yen", "JPY", 110.0),
        ("British Pound", "GBP", 0.75)
    ]
    for name, iso, rate in currency_data:
        code = get_next_id("Dim_Currency")
        state["currency_codes"].append(code)
        currencies.append([code, name, iso, rate, datetime.today(), True])
    state["Currency_Code"] = state["currency_codes"][0]
    generate_insert_multiple_sql(f, "Dim_Currency", ["Currency_Code", "Currency_Name", "ISO_Code", "FX_Rate", "Effective_Date", "Is_Active"], currencies)

    # 6. Dim_Branch (multiple branches)
    branches = []
    state["branch_ids"] = []
    branch_data = [
        ("BR01", "Hanoi HQ", "North"),
        ("BR02", "Ho Chi Minh Branch", "South"),
        ("BR03", "Da Nang Branch", "Central"),
        ("BR04", "Hai Phong Branch", "North"),
        ("BR05", "Can Tho Branch", "South")
    ]
    for code, name, region in branch_data:
        branch_id = get_next_id("Dim_Branch")
        state["branch_ids"].append(branch_id)
        branches.append([branch_id, code, name, region, random_date(2010, 2020)])
    state["Branch_ID"] = state["branch_ids"][0]
    generate_insert_multiple_sql(f, "Dim_Branch", ["Branch_ID", "Branch_Code", "Branch_Name", "Region", "Open_Date"], branches)

    # 7. Dim_Party_Role (multiple roles)
    party_roles = []
    state["role_names"] = []
    role_data = [
        ("Beneficiary", "Receives funds"),
        ("Director", "Company director"),
        ("Shareholder", "Company shareholder"),
        ("Agent", "Acting agent"),
        ("Trustee", "Trust manager")
    ]
    for name, desc in role_data:
        role_id = get_next_id("Dim_Party_Role")
        state["role_names"].append(name)
        party_roles.append([role_id, name, desc])
    state["Role_Name"] = "Beneficiary"
    generate_insert_multiple_sql(f, "Dim_Party_Role", ["Role_ID", "Role_Name", "Description"], party_roles)

    # 8. Dim_Time (date dimension)
    time_records = []
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2025, 12, 31)
    current_date = start_date
    state["date_ids"] = []
    
    while current_date <= end_date:
        state["date_ids"].append(current_date.date())
        time_records.append([
            current_date.date(),
            current_date.year,
            current_date.month,
            (current_date.month - 1) // 3 + 1,  # Quarter
            current_date.isocalendar()[1],  # Week
            current_date.strftime('%A')  # Day of week
        ])
        current_date += timedelta(days=1)
    
    state["Date_ID"] = state["date_ids"][0]
    generate_insert_multiple_sql(f, "Dim_Time", ["Date_ID", "Year", "Month", "Quarter", "Week", "Day_of_Week"], time_records)

    # 9. Dim_Alert_Type
    alert_types = []
    state["alert_type_ids"] = []
    alert_data = [
        ("Large Cash Transaction", "amount > 10000", "High"),
        ("Frequent Small Deposits", "count > 10 AND amount < 1000", "Medium"),
        ("Cross Border Transfer", "country_risk = 'High'", "High"),
        ("PEP Transaction", "customer.pep_flag = true", "Critical"),
        ("Unusual Pattern", "deviation > 3_sigma", "Medium")
    ]
    for scenario, rule, severity in alert_data:
        alert_id = get_next_id("Dim_Alert_Type")
        state["alert_type_ids"].append(alert_id)
        alert_types.append([alert_id, scenario, rule, severity])
    state["Alert_Type_ID"] = state["alert_type_ids"][0]
    generate_insert_multiple_sql(f, "Dim_Alert_Type", ["Alert_Type_ID", "Scenario_Name", "Detection_Rule", "Severity_Level"], alert_types)

    # 10. Dim_Transaction_Reason
    transaction_reasons = []
    state["reason_codes"] = []
    reason_data = [
        ("Salary Payment", "Low"),
        ("Investment", "Medium"),
        ("Loan", "High"),
        ("Gift", "Medium"),
        ("Trade", "Low")
    ]
    for desc, risk in reason_data:
        code = get_next_id("Dim_Transaction_Reason")
        state["reason_codes"].append(code)
        transaction_reasons.append([code, desc, risk])
    state["Reason_Code"] = state["reason_codes"][0]
    generate_insert_multiple_sql(f, "Dim_Transaction_Reason", ["Reason_Code", "Reason_Desc", "Risk_Level"], transaction_reasons)

    # 11. Dim_Collateral_Type
    asset_types = []
    state["asset_types"] = []
    asset_type_names = ["RealEstate", "Vehicle", "Equipment", "Securities", "Jewelry"]
    for asset_type in asset_type_names:
        collateral_id = get_next_id("Dim_Collateral_Type")
        state["asset_types"].append(collateral_id)
        category = "Physical Asset" if asset_type != "Securities" else "Financial Asset"
        asset_types.append([
            collateral_id,
            asset_type,
            category,
            random.randint(50, 100),
            True
        ])
    state["Asset_Type"] = state["asset_types"][0]
    generate_insert_multiple_sql(f, "Dim_Collateral_Type", ["Collateral_Type_ID", "Name", "Category", "Liquidity_Score", "Accepted_For_Loan_Flag"], asset_types)

    # 12. Dim_Compliance_Rule_Snapshot
    compliance_rules = []
    state["rule_ids"] = []
    rule_data = [
        ("CASH_10K", "Large Cash Transaction", "SELECT * FROM transactions WHERE amount > 10000", "High", "amount:10000", "AML"),
        ("FREQ_DEP", "Frequent Deposits", "SELECT * FROM transactions WHERE txn_count > 10", "Medium", "count:10", "AML"),
        ("PEP_CHK", "PEP Screening", "SELECT * FROM customers WHERE pep_flag = true", "Critical", "", "KYC"),
        ("SANC_CHK", "Sanctions Check", "SELECT * FROM parties WHERE sanctioned = true", "Critical", "", "Sanctions")
    ]
    for code, name, sql, severity, thresholds, group in rule_data:
        full_rule_id = get_next_id("Dim_Compliance_Rule_Snapshot")
        state["rule_ids"].append(full_rule_id)
        compliance_rules.append([full_rule_id, code, sql, severity, thresholds, random_date(2020, 2023), group, True])
    state["Rule_ID"] = state["rule_ids"][0]
    generate_insert_multiple_sql(f, "Dim_Compliance_Rule_Snapshot", ["Rule_ID", "Rule_Name", "Rule_SQL", "Severity_Level", "Thresholds", "Effective_Date", "Rule_Group", "Is_Enabled"], compliance_rules)

    # 13. Dim_Customer (multiple customers)
    customers = []
    state["customer_ids"] = []
    state["id_numbers"] = []
    for i in range(1000):
        customer_id = get_next_id("Dim_Customer")
        id_number = fake.random_int(min=100000000, max=999999999)
        state["customer_ids"].append(customer_id)
        state["id_numbers"].append(id_number)
        customers.append([
            customer_id,
            fake.name(),
            fake.date_of_birth(),
            fake.country(),
            round(random.uniform(20000, 200000), 2),
            random.choice([True, False]),
            random.choice(["Single", "Married", "Divorced"]),
            str(fake.random_int(min=1000, max=9999)),
            random.choice(["Passport", "ID Card", "Driver License"]),
            id_number,
            fake.address(),
            fake.phone_number(),
            fake.email(),
            random_date(2015, 2023),
            random.choice(state["branch_ids"])
        ])
    state["Customer_ID"] = state["customer_ids"][0]
    state["ID_Number"] = state["id_numbers"][0]
    generate_insert_multiple_sql(f, "Dim_Customer", ["Customer_ID", "Name", "DOB", "Nationality", "Income_Level", "PEP_Flag", "Marital_Status", "Industry_Code", "ID_Type", "ID_Number", "Address", "Phone", "Email", "Customer_Open_Date", "Branch_ID"], customers)

    # 14. Dim_PEP_List (Politically Exposed Persons)
    pep_records = []
    for i in range(100):
        national_id = random.choice(state["id_numbers"])
        pep_records.append([
            national_id,
            fake.name(),
            fake.country(),
            random.choice(["Minister", "Governor", "Judge", "Ambassador", "CEO"]),
            random_date(2020, 2024)
        ])
    generate_insert_multiple_sql(f, "Dim_PEP_List", ["National_ID", "Name", "Country", "Position", "Last_Verified_Date"], pep_records)

    # 15. Dim_Party (External parties)
    parties = []
    state["party_ids"] = []
    for i in range(500):
        party_id = get_next_id("Dim_Party")
        state["party_ids"].append(party_id)
        parties.append([
            party_id,
            random.choice(["Individual", "Company", "Government", "NGO"]),
            fake.company(),
            str(fake.random_number(digits=10)),
            fake.country(),
            fake.address(),
            random.choice(["Active", "Inactive", "Suspended"]),
            random.choice([True, False])
        ])
    state["Party_ID"] = state["party_ids"][0]
    generate_insert_multiple_sql(f, "Dim_Party", ["Party_ID", "Party_Type", "Party_Name", "Registration_Number", "Country", "Address", "Status", "Is_Customer_Flag"], parties)

    # 16. Dim_Asset (Customer assets)
    assets = []
    state["asset_ids"] = []
    for i in range(2000):
        asset_id = get_next_id("Dim_Asset")
        state["asset_ids"].append(asset_id)
        asset_type = random.choice(state["asset_types"])
        assets.append([
            asset_id,
            asset_type,
            f"{asset_type_names[state['asset_types'].index(asset_type)]} - {fake.word()}",
            str(fake.random_number(digits=8)),
            random.choice(state["currency_codes"]),
            random_date(2015, 2023),
            random.choice(state["customer_ids"]),
            random.choice(state["country_codes"]),
            random.choice(["Active", "Sold", "Disposed"])
        ])
    state["Asset_ID"] = state["asset_ids"][0]
    generate_insert_multiple_sql(f, "Dim_Asset", ["Asset_ID", "Asset_Type", "Description", "Registration_No", "Currency", "Purchase_Date", "Customer_ID", "Country", "Asset_Status"], assets)

    # 17. Dim_Account (Customer accounts)
    accounts = []
    state["account_ids"] = []
    for i in range(1500):
        account_id = get_next_id("Dim_Account")
        state["account_ids"].append(account_id)
        open_date = random_date(2015, 2023)
        close_date = random_date(2024, 2025) if random.random() < 0.1 else None
        accounts.append([
            account_id,
            random.choice(state["customer_ids"]),
            random.choice(["Savings", "Checking", "Investment", "Loan"]),
            open_date,
            close_date,
            "Closed" if close_date else "Active",
            random.choice(state["currency_codes"]),
            random.choice(state["branch_ids"])
        ])
    state["Account_ID"] = state["account_ids"][0]
    generate_insert_multiple_sql(f, "Dim_Account", ["Account_ID", "Customer_ID", "Account_Type", "Open_Date", "Close_Date", "Account_Status", "Currency", "Branch_ID"], accounts)

    # 18. Dim_Employment
    employments = []
    for i in range(800):
        employer_id = get_next_id("Dim_Employment")
        employments.append([
            employer_id,
            random.choice(state["customer_ids"]),
            fake.job(),
            fake.company(),
            random.choice(["Finance", "Technology", "Healthcare", "Education", "Government"]),
            random.choice(["Salary", "Business", "Investment", "Other"]),
            random_date(2020, 2024)
        ])
    generate_insert_multiple_sql(f, "Dim_Employment", ["Employer_ID", "Customer_ID", "Job_Title", "Company_Name", "Industry", "Income_Source", "Verification_Date"], employments)

    # 19. Dim_KYC_Event
    kyc_events = []
    for i in range(600):
        kyc_event_id = get_next_id("Dim_KYC_Event")
        kyc_events.append([
            kyc_event_id,
            random.choice(state["customer_ids"]),
            random.choice(["Address", "Phone", "Email", "Income", "Employment"]),
            fake.text(max_nb_chars=50),
            fake.text(max_nb_chars=50),
            random_date(2020, 2024)
        ])
    generate_insert_multiple_sql(f, "Dim_KYC_Event", ["KYC_Event_ID", "Customer_ID", "Change_Type", "Old_Value", "New_Value", "Change_Date"], kyc_events)

    # 20. Dim_Customer_Asset_Ownership
    ownerships = []
    for i in range(1000):
        ownerships.append([
            random.choice(state["customer_ids"]),
            random.choice(state["asset_ids"]),
            random.choice(["Full", "Partial", "Trust", "Joint"]),
            round(random.uniform(10, 100), 2),
            random_date(2020, 2024)
        ])
    generate_insert_multiple_sql(f, "Dim_Customer_Asset_Ownership", ["Customer_ID", "Asset_ID", "Ownership_Type", "Ownership_Percentage", "Declaration_Date"], ownerships)

    # Snapshot tables
    # 21. Dim_Customer_Wealth_Profile
    wealth_profiles = []
    for i in range(500):
        customer_id = get_next_id("Dim_Customer_Wealth_Profile")
        wealth_profiles.append([
            customer_id,
            random.choice(state["date_ids"]),
            round(random.uniform(10000, 1000000), 2),
            round(random.uniform(50000, 2000000), 2),
            round(random.uniform(30000, 300000), 2),
            round(random.uniform(0, 100000), 2),
            random.choice(["Bronze", "Silver", "Gold", "Platinum"])
        ])
    generate_insert_multiple_sql(f, "Dim_Customer_Wealth_Profile", ["Customer_ID", "Date_ID", "Total_Balance", "Total_Assets", "Estimated_Income", "Loan_Exposure", "Wealth_Tier"], wealth_profiles)

    # 22. Dim_Account_Balance_Snapshot
    balance_snapshots = []
    for i in range(1000):
        account_id = get_next_id("Dim_Account_Balance_Snapshot")
        balance_snapshots.append([
            account_id,
            random.choice(state["customer_ids"]),
            random_date(2024, 2025),
            round(random.uniform(-5000, 100000), 2),
            round(random.uniform(0, 95000), 2),
            random.choice(state["currency_codes"]),
            "Active",
            round(random.uniform(0, 10000), 2),
            random.choice(state["branch_ids"])
        ])
    generate_insert_multiple_sql(f, "Dim_Account_Balance_Snapshot", ["Account_ID", "Customer_ID", "Balance_Date", "Current_Balance", "Available_Balance", "Currency", "Account_Status", "Overdraft_Limit", "Branch_ID"], balance_snapshots)

    # 23. Dim_KYC_Profile_Snapshot
    kyc_snapshots = []
    for i in range(800):
        customer_id = get_next_id("Dim_KYC_Profile_Snapshot")
        kyc_snapshots.append([
            customer_id,
            fake.name(),
            fake.date_of_birth(),
            fake.country(),
            random.choice(["Passport", "ID Card"]),
            fake.random_int(min=100000000, max=999999999),
            fake.address(),
            round(random.uniform(20000, 200000), 2),
            random.choice(["Single", "Married"]),
            fake.phone_number(),
            fake.email(),
            random_date(2020, 2023),
            random.choice([True, False])
        ])
    generate_insert_multiple_sql(f, "Dim_KYC_Profile_Snapshot", ["Customer_ID", "Name", "DOB", "Nationality", "ID_Type", "ID_Number", "Address", "Income_Level", "Marital_Status", "Phone", "Email", "Customer_Open_Date", "PEP_Flag"], kyc_snapshots)

    # 24. Hist_Dim_Employment (Historical employment data)
    hist_employment = []
    for i in range(1200):
        employer_id = str(uuid.uuid4())
        hist_employment.append([
            employer_id,
            random.choice(state["customer_ids"]),
            fake.job(),
            fake.company(),
            random.choice(["Finance", "Technology", "Healthcare"]),
            random.choice(["Salary", "Business"]),
            random_date(2018, 2023),
            random_date(2023, 2024)  # partition date
        ])
    generate_insert_multiple_sql(f, "Hist_Dim_Employment", ["Employer_ID", "Customer_ID", "Job_Title", "Company_Name", "Industry", "Income_Source", "Verification_Date", "ds_partition_date"], hist_employment)

    # FACT TABLES
    # 25. Fact_Transaction
    transactions = []
    state["transaction_ids"] = []
    for i in range(10000):
        txn_id = get_next_id("Fact_Transaction")
        state["transaction_ids"].append(txn_id)
        transactions.append([
            txn_id,
            random.choice(state["account_ids"]),
            random.choice(state["account_ids"]),
            round(random.uniform(10, 50000), 2),
            random.choice(state["transaction_type_ids"]),
            random_date(2023, 2024),
            random.choice(state["channel_ids"]),
            random.choice(state["country_codes"]),
            random.choice(state["reason_codes"]),
            random.choice(state["currency_codes"])
        ])
    state["Transaction_ID"] = state["transaction_ids"][0]
    generate_insert_multiple_sql(f, "Fact_Transaction", ["Transaction_ID", "From_Account_ID", "To_Account_ID", "Amount", "Transaction_Type_ID", "Booking_Date", "Channel_ID", "Country_Code", "Transaction_Reason", "Currency"], transactions)

    # 26. Fact_Loan_Repayment
    loan_repayments = []
    state["loan_ids"] = []
    for i in range(2000):
        loan_id = get_next_id("Fact_Loan_Repayment")
        state["loan_ids"].append(loan_id)
        principal = round(random.uniform(100, 5000), 2)
        interest = round(random.uniform(10, 500), 2)
        loan_repayments.append([
            loan_id,
            random.choice(state["customer_ids"]),
            random_date(2023, 2024),
            principal + interest,
            principal,
            interest,
            random.choice(["Auto Debit", "Manual", "Check"]),
            round(random.uniform(0, 50000), 2)
        ])
    state["Loan_ID"] = state["loan_ids"][0]
    generate_insert_multiple_sql(f, "Fact_Loan_Repayment", ["Loan_ID", "Customer_ID", "Repayment_Date", "Repayment_Amount", "Principal_Component", "Interest_Component", "Repayment_Method", "Remaining_Balance"], loan_repayments)

    # 27. Fact_Card_Transaction
    card_transactions = []
    state["card_ids"] = []
    for i in range(5000):
        card_id = str(uuid.uuid4())
        state["card_ids"].append(card_id)
        card_txn_id = get_next_id("Fact_Card_Transaction")
        card_transactions.append([
            card_txn_id,
            card_id,
            random.choice(state["customer_ids"]),
            random_date(2023, 2024),
            round(random.uniform(5, 2000), 2),
            fake.company(),
            fake.country(),
            random.choice(state["channel_ids"]),
            random.choice(["Purchase", "Withdrawal", "Refund"])
        ])
    generate_insert_multiple_sql(f, "Fact_Card_Transaction", ["Card_Txn_ID", "Card_ID", "Customer_ID", "Txn_Date", "Amount", "Merchant", "Country", "Channel_ID", "Txn_Type"], card_transactions)

    # 28. Fact_Deposit
    deposits = []
    for i in range(3000):
        deposit_id = get_next_id("Fact_Deposit")
        start_date = random_date(2023, 2024)
        deposits.append([
            deposit_id,
            random.choice(state["customer_ids"]),
            random.choice(["Fixed", "Savings", "Current"]),
            start_date,
            start_date + timedelta(days=random.randint(30, 365)),
            round(random.uniform(1000, 100000), 2),
            round(random.uniform(1.0, 8.0), 2),
            random.choice(state["branch_ids"])
        ])
    generate_insert_multiple_sql(f, "Fact_Deposit", ["Deposit_ID", "Customer_ID", "Deposit_Type", "Start_Date", "Maturity_Date", "Amount", "Interest_Rate", "Branch_ID"], deposits)

    # 29. Fact_Cash_Deposit_Withdrawal
    cash_transactions = []
    for i in range(4000):
        txn_id = get_next_id("Fact_Cash_Deposit_Withdrawal")
        cash_transactions.append([
            txn_id,
            random.choice(state["account_ids"]),
            random_date(2023, 2024),
            random.choice(["Deposit", "Withdrawal"]),
            round(random.uniform(50, 20000), 2),
            random.choice(["ATM", "Branch", "Agent"]),
            fake.city(),
            fake.name()
        ])
    generate_insert_multiple_sql(f, "Fact_Cash_Deposit_Withdrawal", ["Txn_ID", "Account_ID", "Txn_Date", "Txn_Type", "Amount", "Channel", "Location", "Handled_By"], cash_transactions)

    # 30. Fact_Customer_Balance
    customer_balances = []
    for i in range(8000):
        customer_balances.append([
            random.choice(state["customer_ids"]),
            random.choice(state["account_ids"]),
            random.choice(state["date_ids"]),
            round(random.uniform(-1000, 50000), 2),
            random.choice(state["currency_codes"])
        ])
    generate_insert_multiple_sql(f, "Fact_Customer_Balance", ["Customer_ID", "Account_ID", "Date_ID", "Closing_Balance", "Currency"], customer_balances)

    # 31. Fact_Customer_Income
    customer_incomes = []
    for i in range(3000):
        customer_incomes.append([
            random.choice(state["customer_ids"]),
            random_date(2023, 2024).replace(day=1),  # First day of month
            round(random.uniform(1000, 20000), 2),
            random.choice(["Salary", "Business", "Investment", "Other"]),
            random.choice(["Salary", "Dividend", "Rent", "Freelance"]),
            random.choice(["Direct", "Estimated", "Declared"])
        ])
    generate_insert_multiple_sql(f, "Fact_Customer_Income", ["Customer_ID", "Month", "Inflow_Amount", "Inflow_Source", "Income_Type", "Estimation_Method"], customer_incomes)

    # 32. Fact_Alert
    alerts = []
    for i in range(1500):
        alert_id = get_next_id("Fact_Alert")
        alerts.append([
            alert_id,
            random.choice(state["customer_ids"]),
            random.choice(state["alert_type_ids"]),
            random_date(2023, 2024),
            random.choice(state["rule_ids"]),
            random.choice(["Low", "Medium", "High", "Critical"]),
            random.choice(["Open", "Under Review", "Closed", "False Positive"]),
            random.choice(["Escalated", "Cleared", "Pending", "False Positive"])
        ])
    generate_insert_multiple_sql(f, "Fact_Alert", ["Alert_ID", "Customer_ID", "Alert_Type_ID", "Triggered_On", "Triggered_By_Rule", "Severity", "Status", "Review_Outcome"], alerts)

    # 33. Fact_Risk_Score
    risk_scores = []
    for i in range(2000):
        risk_scores.append([
            random.choice(state["customer_ids"]),
            random_date(2023, 2024),
            round(random.uniform(0, 100), 2),
            random.choice(state["risk_level_names"]),
            f"Rule1,Rule2,Rule{random.randint(3,10)}",
            random.choice([True, False])
        ])
    generate_insert_multiple_sql(f, "Fact_Risk_Score", ["Customer_ID", "Score_Date", "Score_Value", "Score_Band", "Driving_Rules", "Override_Flag"], risk_scores)

    # 34. Fact_Transaction_Peer_Pair
    peer_pairs = []
    for i in range(1000):
        peer_pairs.append([
            random.choice(state["customer_ids"]),
            random.choice(state["customer_ids"]),
            random.randint(7, 90),
            random.randint(1, 20),
            round(random.uniform(100, 50000), 2),
            random_date(2023, 2024),
            random.choice([True, False])
        ])
    generate_insert_multiple_sql(f, "Fact_Transaction_Peer_Pair", ["From_Customer_ID", "To_Customer_ID", "Window_Days", "Txn_Count", "Total_Amount", "First_Txn_Date", "Bidirectional_Flag"], peer_pairs)

    # 35. Fact_Collateral_Assignment
    collateral_assignments = []
    for i in range(800):
        collateral_value = round(random.uniform(10000, 500000), 2)
        current_value = round(collateral_value * random.uniform(0.8, 1.2), 2)
        ltv = round((random.uniform(5000, 400000) / current_value) * 100, 2) if current_value > 0 else 0
        collateral_assignments.append([
            random.choice(state["loan_ids"]),
            random.choice(state["asset_ids"]),
            random.choice(state["customer_ids"]),
            random_date(2022, 2024),
            collateral_value,
            current_value,
            min(ltv, 100),  # Cap at 100%
            random.choice(state["currency_codes"])
        ])
    generate_insert_multiple_sql(f, "Fact_Collateral_Assignment", ["Loan_ID", "Collateral_ID", "Customer_ID", "Assigned_Date", "Collateral_Value", "Current_Value", "LTV", "Currency"], collateral_assignments)

    # 36. Fact_Asset_Valuation
    asset_valuations = []
    for i in range(2500):
        asset_valuations.append([
            random.choice(state["asset_ids"]),
            random_date(2023, 2024),
            round(random.uniform(5000, 1000000), 2),
            random.choice(["Bank Appraisal", "Market Value", "Insurance", "Tax Assessment"]),
            random.choice(["Market", "Replacement", "Liquidation", "Book"]),
            random.choice(state["currency_codes"])
        ])
    generate_insert_multiple_sql(f, "Fact_Asset_Valuation", ["Asset_ID", "Valuation_Date", "Valuation_Amount", "Source", "Valuation_Type", "Currency"], asset_valuations)

    # 37. Fact_Party_Linkage
    party_linkages = []
    for i in range(1200):
        party_linkages.append([
            random.choice(state["customer_ids"]),
            random.choice(state["party_ids"]),
            random.choice(state["role_names"]),
            fake.text(max_nb_chars=100),
            random_date(2020, 2024),
            round(random.uniform(0.6, 1.0), 2)
        ])
    generate_insert_multiple_sql(f, "Fact_Party_Linkage", ["Customer_ID", "Party_ID", "Link_Type", "Link_Evidence", "Relationship_Start", "Confidence_Score"], party_linkages)

    # 38. Fact_Customer_Wealth_Profile (Fact version - different from Dim version)
    wealth_profile_facts = []
    for i in range(1800):
        wealth_profile_facts.append([
            random.choice(state["customer_ids"]),
            random.choice(state["date_ids"]),
            round(random.uniform(15000, 800000), 2),
            round(random.uniform(50000, 1500000), 2),
            round(random.uniform(25000, 250000), 2),
            round(random.uniform(0, 150000), 2),
            random.choice(["Bronze", "Silver", "Gold", "Platinum", "Diamond"])
        ])
    generate_insert_multiple_sql(f, "Fact_Customer_Wealth_Profile", ["Customer_ID", "Date_ID", "Total_Balance", "Total_Assets", "Estimated_Income", "Loan_Exposure", "Wealth_Tier"], wealth_profile_facts)

    # 39. Fact_KYC_Change_Log (Final table)
    kyc_change_logs = []
    for i in range(2000):
        change_fields = ["Name", "Address", "Phone", "Email", "Income_Level", "Employment", "Marital_Status"]
        kyc_change_logs.append([
            random.choice(state["customer_ids"]),
            random.choice(change_fields),
            fake.text(max_nb_chars=50),
            fake.text(max_nb_chars=50),
            random_datetime(2023, 2024),
            random.choice(["Customer Request", "System Update", "Compliance Review", "Data Correction"]),
            random.choice(["System", "Customer", "Branch Staff", "Compliance Officer"])
        ])
    generate_insert_multiple_sql(f, "Fact_KYC_Change_Log", ["Customer_ID", "Change_Field", "Old_Value", "New_Value", "Change_Timestamp", "Change_Reason", "Initiated_By"], kyc_change_logs)

    f.write('COMMIT;\n')

print("\n🎉 SUCCESS: Generated SQL for all 39 tables in generate_data.txt!")
print("📊 Summary:")
print(f"   - Customers: {len(state['customer_ids'])}")
print(f"   - Accounts: {len(state['account_ids'])}")
print(f"   - Transactions: {len(state['transaction_ids'])}")
print(f"   - Assets: {len(state['asset_ids'])}")
print(f"   - Countries: {len(state['country_codes'])}")
print(f"   - Branches: {len(state['branch_ids'])}")
print(f"   - Date records: {len(state['date_ids'])}")

print("\nNote: The schema has type mismatches for foreign keys (int PK vs varchar FK). Update all referencing columns to INTEGER in the schema to match.")

print("\n📋 Verification Queries (run these manually to check data):")
verification_queries = [
    'SELECT COUNT(*) as customer_count FROM "Dim_Customer";',
    'SELECT COUNT(*) as transaction_count FROM "Fact_Transaction";',
    'SELECT COUNT(*) as alert_count FROM "Fact_Alert";',
    'SELECT currency, COUNT(*) FROM "Fact_Transaction" GROUP BY currency;',
    'SELECT account_type, COUNT(*) FROM "Dim_Account" GROUP BY account_type;',
    'SELECT severity, COUNT(*) FROM "Fact_Alert" GROUP BY severity;'
]

for query in verification_queries:
    print(f"   {query}")

print("\n✅ SQL generation completed successfully!")