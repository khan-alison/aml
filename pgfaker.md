# ✅ Step-by-Step Guide to Install and Run `pgfaker` Locally

## 🧱 1. Create and Activate a Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```
## 📦 2. Install `pgfaker` from PyPI
```bash
pip install pgfaker
```
# ✅ Confirm installation
```bash
pgfaker --help
```
## 📁 3. Make Sure You Have Your YAML File Ready
Example: /Users/khanhnn/Developer/DE/projects/AML/pgfaker_config.yaml

## 🛠️ 4. Generate SQL Insert Statements Using `pgfaker`
```bash
pgfaker generate \
  --config /Users/khanhnn/Developer/DE/projects/AML/pgfaker_config.yaml \
  --output /Users/khanhnn/Developer/DE/projects/AML/fake_data.sql
```
## 📥 5. Load Generated Data into PostgreSQL
```bash
psql -U postgres -d aml -f /Users/khanhnn/Developer/DE/projects/AML/fake_data.sql
```

## 📌 Notes:
- Ensure the database `aml` already exists and the schema (39 tables) is already created.
- `pgfaker` does not automatically enforce FK order. You should:
  - Keep YAML table order aligned with dependency
  - Or insert using `--insert-order` if supported (TBD)