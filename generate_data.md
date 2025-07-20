# 🔧 Mock Data Generator Tools for AML Tables

## 🌐 1. Mockaroo – Best for Structured CSV/SQL Export
- **Link**: https://mockaroo.com
- ✅ Hỗ trợ cấu hình tên cột, kiểu dữ liệu, format chuẩn
- ✅ Xuất trực tiếp ra CSV / JSON / SQL
- ✅ Hỗ trợ logic như `unique`, `regex`, ràng buộc foreign key giả
- 🔒 Không cần đăng ký để dùng cơ bản

### 👣 Cách dùng:
1. Truy cập [mockaroo.com](https://mockaroo.com)
2. Nhập schema giống các bảng như `"Customer_ID"` → kiểu `Row Number`, `"Name"` → `Full Name`, `"DOB"` → `Date`...
3. Chọn số lượng bản ghi → Chọn định dạng CSV/SQL
4. Click **Download Data**

---

## 🌐 2. GenerateData.com – Free schema-based generator
- **Link**: https://generatedata.com
- ✅ Giao diện trực quan, có preset cho tên, ngày, email, phone,...
- ✅ Hỗ trợ CSV, Excel, SQL, JSON
- ⚠️ Giới hạn 100 bản ghi khi chưa đăng ký

---

## 🌐 3. Faker.js Online (JSFiddle-style generator)
- **Link**: https://fakerjs.dev/ or [https://www.fakergenerator.com](https://www.fakergenerator.com)
- ✅ Tùy biến tốt nếu bạn quen JavaScript
- ✅ Hỗ trợ tên người, địa chỉ, email, số ngẫu nhiên, v.v.
- 🔧 Không hỗ trợ xuất SQL trực tiếp nhưng dễ copy/paste

---

## 🌐 4. SQL Data Generator – Redgate (Desktop tool)
- **Link**: https://www.red-gate.com/products/sql-development/sql-data-generator/
- ✅ Mạnh mẽ cho các hệ thống thực tế
- ✅ Có thể connect trực tiếp với PostgreSQL
- ❌ Trả phí (có trial 14 ngày)

---

## 🌐 5. Random Data Generator via CSV Builder
- **Link**: https://extendsclass.com/csv-generator.html
- ✅ Dễ tạo bảng CSV đơn giản nhanh chóng
- ✅ Có hàm mẫu như `firstName`, `email`, `date`, `number`, `uuid`
- ❌ Không quá chuyên sâu cho quan hệ bảng

---

### 🧠 Gợi ý khi tạo dữ liệu:
- Dùng **Mockaroo** để tạo bảng `Dim_Customer`, `Dim_Account`, `Fact_Transaction` dễ dàng.
- Giữ nguyên tên cột khớp với schema Postgres.
- Nếu cần join giữa các bảng, nên generate các bảng dimension trước, rồi dùng `customer_id`, `account_id` của chúng để build `Fact_*`.

---

Bạn muốn mình giúp tạo sẵn cấu hình Mockaroo cho 1 bảng cụ thể không?