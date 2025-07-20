# 📘 Hướng dẫn Xem File `.dbml` Dưới Dạng Diagram

Dưới đây là **3 cách** để xem sơ đồ từ file `.dbml`, bao gồm sử dụng **CLI** và **2 công cụ online**.

---

## ✅ Cách 1: Dùng CLI (`@dbml/cli`) để tạo file HTML Diagram

**Yêu cầu:** Cài `Node.js` và `@dbml/cli`

#### 🔧 Bước 1 – Cài đặt CLI

```bash
npm install -g @dbml/cli
```

#### 📄 Bước 2 – Render file .dbml thành .html
```bash
dbml render ~/Developer/DE/projects/AML/doc/full_aml_schema_with_currency.dbml \
  -o /Users/khanhnn/Developer/DE/projects/AML/doc/aml_schema_diagram.html
```

#### 🌐 Bước 3 – Mở file sơ đồ

```bash
open ~/Users/khanhnn~/Developer/DE/projects/AML/doc/aml_schema_diagram.html
```

⸻

### 🌐 Cách 2: Dùng trang web dbdiagram.io

🔗 Link: https://dbdiagram.io

#### 📄 Bước 1 – Mở trang dbdiagram.io

#### 📂 Bước 2 – Nhấn “New Diagram” → Chọn tab DBML

#### 📥 Bước 3 – Copy nội dung file .dbml và dán vào ô soạn thảo

#### 📊 Bước 4 – Sơ đồ sẽ được render tự động ngay bên phải

Có thể đăng nhập để lưu, chia sẻ và xuất file.

⸻

### 🌐 Cách 3: Dùng công cụ DBML Studio

🔗 Link: https://dbml.dbdiagram.io

#### 📄 Bước 1 – Truy cập trang dbml.dbdiagram.io

#### 📥 Bước 2 – Nhấn nút “Upload .dbml file” và chọn:
```bash
~/Developer/DE/projects/AML/doc/full_aml_schema_with_currency.dbml
```

#### 🔍 Bước 3 – Xem sơ đồ được vẽ trực tiếp trên trình duyệt

DBML Studio hỗ trợ drag & drop file .dbml, hỗ trợ export sang PostgreSQL, MySQL, SQLite.


