# =========================
print("CourseHub - Buoi 1")
# =========================
# Mô phỏng dữ liệu bằng list và dictionary
students = [
    {"id": "22000001", "name": "Nguyen Minh Anh", "major": "KHDL"},
    {"id": "22000002", "name": "Tran Duc Long", "major": "KHDL"},
]
courses = [
    {
    "code": "INT2204",
    "name": "Co so du lieu Web va he thong thong tin",
    "capacity": 3,
    "enrolled": 2,
    },
    {
    "code": "INT2205",
    "name": "Khai pha du lieu",
    "capacity": 2,
    "enrolled": 2,
    },
]
enrollments = [
    {"student_id": "22000001", "course_code": "INT2204"}
]
# ======================
# Duyệt dữ liệu và tính giá trị
for course in courses:
    remaining = course["capacity"] - course["enrolled"]
    print(course["code"], "- con", remaining, "cho")
# ======================
# Tách xử lý thành hàm
def find_course(course_code):
    for course in courses:
        if course["code"] == course_code:
            return course
    return None
print(find_course("INT2204"))
# ========================
# Mô phỏng quy tắc đăng ký
def can_enroll(student_id, course_code):
    course = find_course(course_code)
    if course is None:
        return False, "Hoc phan khong ton tai"
    if course["enrolled"] >= course["capacity"]:
        return False, "Lop da du so luong"
    duplicated = any(
        item["student_id"] == student_id and item["course_code"] == course_code
        for item in enrollments
    )
    if duplicated:
        return False, "Sinh vien da dang ky hoc phan nay"
    return True, "Co the dang ky"
print(can_enroll("22000002", "INT2204"))
# ======================
# Xử lý dữ liệu nhập sai
try:
    limit = int(input("Nhap so luong hoc phan muon hien thi: "))
    print(courses[:limit])
except ValueError:
    print("So luong phai la so nguyen.")
# ======================
# Hàm tìm kiếm học phần
def search_courses(keyword):
    normalized = keyword.strip().lower()
    results = []
    for course in courses:
        code = course["code"].lower()
        name = course["name"].lower()
        if normalized in code or normalized in name:
            results.append(course)
    return results
print(search_courses("web"))
# =======================
# Hàm đăng ký học phần
def enroll_student(student_id, course_code):
    student = None
    for s in students:
        if s["id"] == str(student_id):
            student = s
            break;
    course = None
    for c in courses:
        if c["code"] == str(course_code):
            course = c
            break;
    if student is None:
        print("Sinh viên không tồn tại")
        return False
    else:
        if course is None:
            print("Học phần không tồn tại")
            return False
        else:
            if course["enrolled"] >= course["capacity"]:
                print("Đăng ký thất bại do đã đủ số lượng.")
                return False
            else:
                enrollment = {"student_id": student["id"],"course_code": course["code"]}
                if enrollment in enrollments:
                    print("Sinh viên đã đăng ký học phần này rồi.")
                else:
                    enrollments.append(enrollment)
                    course["enrolled"] += 1
                    print("Đăng ký thành công.")

# ===================
# Test chương trình enroll_student
# TH1: Sinh viên không tồn tại
enroll_student(24001714,"INT2204") # Do id 24001714 không tồn tại
                                   # Nên sẽ in ra chuỗi "Sinh viên không tồn tại
# TH2: Học phần không tồn tại
enroll_student(22000001,"hehehaha") # Do course_code hehehaha không tồn tại
                                    # Nên sẽ in ra chuỗi "Học phần không tồn tại"
# TH3: Lớp học phần đã đầy
enroll_student(22000001,"INT2205")  # Do lớp INT2205 đã có đủ 2 người
                                    # Nên sẽ in ra "Đăng ký thất bại do đủ số lượng"
# TH4: Đăng ký trùng học phần
enroll_student(22000001,"INT2204") # Do id 22000001 đã đăng ký lớp INT2204
                                   # Nên sẽ in ra "Sinh viên đã đăng ký học phần này rồi"
# TH5: Đăng ký thành công
enroll_student(22000002,"INT2204") # In ra đăng ký thành công 
print(courses) # Thông tin enrolled đã được cập nhật từ 2 lên 3
print(enrollments) # Sinh viên đã được cập thêm thành công vào enrollments

