# 🧱 Raw Layer Setup: Tạo Cơ sở Dữ liệu và Bảng Nguồn cho AML

Quy trình này hướng dẫn cách tạo cơ sở dữ liệu `aml` và toàn bộ 39 bảng dimension + fact phục vụ cho raw layer trong hệ thống AML, sử dụng **PostgreSQL** và CLI.

---

## ✅ 1. Khởi tạo Database `aml`

Mở terminal và đăng nhập vào PostgreSQL:
```bash
psql -U <your_postgres_user>
```

Tạo database:
```sql
CREATE DATABASE aml;
```

Kết nối vào database:
```sql
\c aml
```

---

## 📂 2. File DDL để tạo bảng

Tạo một file SQL chứa toàn bộ cấu trúc bảng:

**File path:**
```bash
~/Developer/DE/projects/AML/aml/create_table.sql
```

**Nội dung:** chứa 39 bảng `CREATE TABLE` và `ALTER TABLE` để tạo foreign key (xem chi tiết trong `create_table.sql`)

---

## 🚀 3. Thực thi file DDL

Chạy lệnh sau để tạo tất cả bảng:
```bash
psql -U <your_postgres_user> -d aml -f ~/Developer/DE/projects/AML/aml/create_table.sql
```

Nếu bạn đang trong CLI đã kết nối sẵn:
```bash
\i ~/Developer/DE/projects/AML/aml/create_table.sql
```

---

## 🧪 4. Kiểm tra kết quả

Sau khi chạy file SQL, kiểm tra tất cả bảng đã được tạo:

```sql
\dt
```

Bạn sẽ thấy danh sách đầy đủ 39 bảng đã được khởi tạo, bao gồm:
- 23 bảng Dimension (e.g. `Dim_Customer`, `Dim_Account`, `Dim_Country`, ...)
- 15 bảng Fact (e.g. `Fact_Transaction`, `Fact_Alert`, ...)
- 1 bảng lịch sử: `Hist_Dim_Employment`

---

## 🧷 5. Lưu ý Khi Sử Dụng Foreign Key

Một số `ALTER TABLE ... ADD FOREIGN KEY` sẽ **thất bại** nếu bảng bị thiếu `PRIMARY KEY` hoặc `UNIQUE`. Đã được cập nhật lại như sau:

- `Dim_Risk_Level` ➝ thêm UNIQUE(`Level_Name`)
- `Dim_Customer` ➝ thêm UNIQUE(`ID_Number`)
- `Dim_Party_Role` ➝ thêm UNIQUE(`Role_Name`)
- `Dim_Asset` ➝ thêm UNIQUE(`Asset_Type`)

---

## 📌 Tổng kết

- ✅ Số lượng bảng: **39**
- ✅ Toàn bộ bảng trống phục vụ làm nguồn cho raw zone
- ✅ Tạo bằng file SQL và CLI, phù hợp với project local / Docker / cloud migration

Bạn có thể bắt đầu ingest dữ liệu thực tế vào các bảng này trong bước tiếp theo của pipeline.