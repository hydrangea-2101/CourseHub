# CourseHub - Buổi 5: Xây dựng Frontend với React kết nối FastAPI

## 1. Kiến trúc hệ thống
- **Frontend**: React 18 + Vite 7 (chạy tại `http://127.0.0.1:5173`).
- **Backend**: FastAPI + SQLAlchemy Core + PostgreSQL (chạy tại `http://127.0.0.1:8000`).
- **CORS Middleware**: Cấu hình tại `backend/app/main.py` cho phép origin `http://127.0.0.1:5173` và `http://localhost:5173`.
- **Database**: Giữ nguyên schema, view `v_section_summary`, transaction khóa dòng `FOR UPDATE` và bảng nhật ký `enrollment_events`.

---

## 2. Hướng dẫn khởi chạy

### Terminal 1: Khởi chạy Backend
```powershell
.venv\Scripts\Activate.ps1
python -m uvicorn backend.app.main:app --reload
```
- Kiểm tra trạng thái: `http://127.0.0.1:8000/health` (HTTP 200)
- API Docs: `http://127.0.0.1:8000/docs`

### Terminal 2: Khởi chạy Frontend
```powershell
cd frontend
npm run dev
```
- Mở trình duyệt tại: `http://127.0.0.1:5173/`

---

## 3. Cấu trúc thư mục Frontend
```text
frontend/
├── package.json
├── package-lock.json
├── vite.config.js
├── index.html
├── .env.example
├── .env.local
├── tests/
│   └── api.test.mjs
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── api.js
    ├── styles.css
    └── components/
        ├── Notice.jsx
        ├── SectionTable.jsx
        └── EnrollmentList.jsx
```

---

## 4. Các kịch bản kiểm thử giao diện & API

1. **Xem danh sách lớp và đăng ký WEB-01**:
   - Chọn sinh viên `22000004` -> Bấm *Xem đăng ký*.
   - Bấm *Đăng ký* lớp `WEB-01` -> Trạng thái trả về 201 Created.
   - Nút chuyển thành *Đã đăng ký*, số chỗ còn lại giảm về `0`.

2. **Hủy đăng ký WEB-01**:
   - Trong vùng *Lớp đã đăng ký*, bấm *Hủy đăng ký* -> Hộp thoại xác nhận -> Trạng thái trả về 204 No Content.
   - Lớp `WEB-01` được xóa khỏi danh sách đăng ký của sinh viên, số chỗ còn lại phục hồi về `1`.

3. **Kiểm tra tranh chấp đồng thời (Race condition) trên lớp RACE-01**:
   - Mở 2 tab/cửa sổ trình duyệt: Cửa sổ A chọn sinh viên `22000002`, cửa sổ B chọn `22000004`.
   - Cả hai cùng thấy lớp `RACE-01` còn 1 chỗ.
   - Cửa sổ A bấm *Đăng ký* thành công (201).
   - Cửa sổ B bấm *Đăng ký* ngay sau đó -> Backend từ chối với lỗi 409 Conflict ("Lop hoc phan da het cho").
   - Giao diện cửa sổ B hiển thị thông báo lỗi và tự động cập nhật lại trạng thái thành *Hết chỗ*.

4. **Kiểm thử tự động unit test cho api.js**:
   - Lệnh chạy: `npm test` trong thư mục `frontend/`.
   - Kết quả: 8/8 tình huống giả lập HTTP đều PASS.

---

## 5. Đối chiếu CSDL PostgreSQL
Chạy file script `database/13_week05_verify.sql` trong Query Tool của pgAdmin để xác nhận dữ liệu:
- Bảng `enrollments`: Kiểm tra sự tồn tại hoặc đã bị xóa của cặp `(student_id, class_section_id)`.
- Bảng `enrollment_events`: Xác nhận có bản ghi sự kiện `CREATED` khi đăng ký và `CANCELLED` khi hủy.
- View `v_section_summary`: Xác nhận `capacity`, `enrolled` và `remaining` tính toán chính xác.
