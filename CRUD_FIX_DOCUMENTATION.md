# Hướng dẫn Sửa lỗi Quản lý Sách - Kiểm tra Kỹ năng 3

## 📋 Tóm tắt những thay đổi

### ✅ Hoàn thiện chức năng CRUD (Requirement 1)
- **Create (Tạo)**: Tạo sách mới với validation đầy đủ
- **Read (Xem)**: Hiển thị danh sách sách với pagination
- **Update (Sửa)**: Chỉnh sửa thông tin sách, có thể tải lên ảnh mới
- **Delete (Xóa)**: Soft delete (đánh dấu is_active=False để giữ lịch sử)

### ✅ Tìm kiếm, lọc, sắp xếp (Requirement 2)
**File**: `bookstore_app/views.py` - hàm `manage_books()`

#### Tìm kiếm:
- Tìm theo tiêu đề sách
- Tìm theo mô tả
- Tìm theo ISBN
- Tìm theo tên tác giả

#### Lọc:
- Lọc theo thể loại
- Lọc theo trạng thái (Còn hàng, Sắp hết, Hết hàng, Ngừng bán)
- Lọc theo trạng thái hoạt động (Hoạt động/Vô hiệu)
- Lọc theo sách nổi bật

#### Sắp xếp:
- Mới nhất (mặc định)
- Tên A-Z, Z-A
- Giá thấp đến cao, cao đến thấp
- Đánh giá cao nhất
- Tồn kho thấp

### ✅ Cài đặt phân quyền (Requirement 3)
**File**: `bookstore_app/views.py`

```python
@login_required              # Chỉ người dùng đã đăng nhập
@user_passes_test(is_admin)  # Chỉ admin mới được phép
def manage_books(request):
    ...
```

Các view được bảo vệ:
- `manage_books()` - Chỉ admin
- `create_book()` - Chỉ admin
- `edit_book()` - Chỉ admin
- `delete_book()` - Chỉ admin

### ✅ Luồng nghiệp vụ (Requirement 4)
**Quy trình tạo sách:**
1. Người dùng nhập thông tin sách
2. Form validate dữ liệu
3. Tạo slug tự động từ tiêu đề
4. Kiểm tra slug trùng lặp, thêm số nếu cần
5. Lưu sách vào database
6. Tạo thông báo thành công
7. Chuyển hướng đến trang sửa để thêm chi tiết

### ✅ Trạng thái dữ liệu (Requirement 5)
**File**: `bookstore_app/models.py`

```python
STATUS_CHOICES = [
    ('available', 'Còn hàng'),
    ('low_stock', 'Sắp hết hàng'),
    ('out_of_stock', 'Hết hàng'),
    ('discontinued', 'Ngừng bán'),
]
```

Các trạng thái khác:
- `is_active`: Sách có hoạt động hay không (soft delete)
- `is_featured`: Sách có nổi bật không

### ✅ Kiểm tra file/ảnh (Requirement 6)
**File**: `bookstore_app/forms.py` - class `BookForm`

#### Kiểm tra định dạng:
```python
ALLOWED_IMAGE_FORMATS = ['jpg', 'jpeg', 'png', 'gif']

def clean_cover_image(self):
    # Kiểm tra định dạng file
    file_ext = os.path.splitext(image.name)[1][1:].lower()
    if file_ext not in self.ALLOWED_IMAGE_FORMATS:
        raise forms.ValidationError('Định dạng không hợp lệ')
```

#### Kiểm tra kích thước:
```python
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

if image.size > self.MAX_IMAGE_SIZE:
    raise forms.ValidationError('Tập tin quá lớn')
```

### ✅ Thông báo thành công/lỗi (Requirement 7)
**File**: `templates/base.html`

```html
{% if messages %}
    <div class="container alert-message">
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }}">
                {% if 'success' in message.tags %}
                    <i class="fas fa-check-circle"></i>
                {% elif 'error' in message.tags %}
                    <i class="fas fa-exclamation-circle"></i>
                {% endif %}
                {{ message }}
            </div>
        {% endfor %}
    </div>
{% endif %}
```

**Ví dụ thông báo:**
- ✓ Sách "xyz" đã được tạo thành công!
- ✓ Sách "xyz" đã được cập nhật thành công!
- ✗ Lỗi khi tạo sách: [chi tiết lỗi]

### ✅ Tổ chức code MVC/Layered (Requirement 8)
**Kiến trúc Django (MVT):**
```
bookstore_app/
├── models.py          # Model Layer - Định nghĩa cơ sở dữ liệu
├── views.py           # View Layer - Xử lý logic, truy vấn DB
├── forms.py           # Form Layer - Validation
├── serializers.py     # API Layer - Chuyển đổi JSON
├── urls.py            # URL Routing
└── templates/
    ├── manage_books.html   # Template Layer - Hiển thị
    ├── book_form.html
    └── ...
```

**Code Comment:**
- Tất cả functions có docstring
- Các bước logic được giải thích
- Validation rules được ghi chú

### ✅ Kiểm thử sơ bộ (Requirement 9)
**File**: `bookstore_app/management/commands/test_crud_operations.py`

#### Chạy test:
```bash
python manage.py test_crud_operations
```

#### Test cases:
1. **CREATE**: Tạo sách mới, kiểm tra dữ liệu
2. **READ**: Lấy sách, tìm kiếm, lọc
3. **UPDATE**: Cập nhật các trường
4. **FILTER & SORT**: Sắp xếp, lọc dữ liệu
5. **SOFT DELETE**: Xóa mềm, giữ lịch sử
6. **VALIDATION**: Kiểm tra validate

---

## 🐛 Lỗi đã sửa

### Lỗi 1: Template không hiển thị đúng trạng thái
**Vấn đề**: `manage_books.html` không có tất cả các trường cần thiết
**Giải pháp**: Cập nhật template với các cột mới:
- Thể loại
- Giá giảm
- Đánh giá
- Trạng thái hoạt động
- Sách nổi bật

### Lỗi 2: Không có bộ lọc và tìm kiếm
**Vấn đề**: Chỉ hiển thị danh sách, không thể lọc/tìm
**Giải pháp**: 
- Thêm form tìm kiếm trong template
- Cập nhật `manage_books()` view với logic lọc
- Thêm các tùy chọn sắp xếp

### Lỗi 3: Validation form không đủ
**Vấn đề**: Không kiểm tra file upload, giá tiền, v.v.
**Giải pháp**: 
- Thêm `clean_*` methods trong BookForm
- Kiểm tra định dạng ảnh
- Kiểm tra kích thước file
- Kiểm tra giá discount < giá gốc
- Kiểm tra ISBN duy nhất

### Lỗi 4: Delete không bảo tồn lịch sử đơn hàng
**Vấn đề**: Hard delete (xóa hoàn toàn) làm mất dữ liệu liên quan
**Giải pháp**: 
- Sử dụng soft delete (đánh dấu is_active=False)
- Giữ lịch sử đơn hàng, review, v.v.

### Lỗi 5: Thông báo không rõ ràng
**Vấn đề**: Thông báo lỗi không chi tiết, không có icon
**Giải pháp**: 
- Thêm icon cho từng loại thông báo
- Hiển thị chi tiết lỗi validation
- Auto-close thông báo sau 5 giây

---

## 📝 Các files được sửa

### 1. `bookstore_app/forms.py`
- Enhance `BookForm` với validation
- Thêm `clean_cover_image()` - Kiểm tra ảnh
- Thêm `clean_discount_price()` - Kiểm tra giá
- Thêm `clean_isbn()` - Kiểm tra ISBN
- Thêm `clean_quantity()` - Kiểm tra số lượng

### 2. `bookstore_app/views.py`
- Update `manage_books()` - Thêm tìm kiếm, lọc, sắp xếp
- Update `create_book()` - Cải thiện validate, slug
- Update `edit_book()` - Thêm try-except, thông báo lỗi
- Update `delete_book()` - Thay soft delete

### 3. `templates/bookstore_app/manage_books.html`
- Thêm form tìm kiếm và lọc
- Thêm cột dữ liệu mới
- Cải thiện UI/UX
- Thêm tooltip
- Cải thiện pagination

### 4. `templates/base.html`
- Cập nhật hiển thị messages
- Thêm icon cho thông báo
- Auto-close alerts

### 5. `bookstore_app/management/commands/test_crud_operations.py`
- Tạo management command mới
- 6 test cases hoàn chỉnh
- Detailed output

---

## 🚀 Cách sử dụng

### 1. Truy cập trang quản lý sách
```
URL: http://localhost:8000/admin_dashboard/
Chỉ admin mới có quyền truy cập
```

### 2. Tạo sách mới
```
1. Nhấn "Thêm sách mới"
2. Điền đầy đủ form
3. Tải lên ảnh (JPG, PNG, GIF - max 5MB)
4. Nhấn "Lưu"
```

### 3. Tìm kiếm sách
```
1. Nhập từ khóa trong ô tìm kiếm
2. Chọn thể loại (nếu cần)
3. Chọn trạng thái (nếu cần)
4. Chọn cách sắp xếp
5. Nhấn "Tìm"
```

### 4. Sửa sách
```
1. Nhấn icon chỉnh sửa (pencil icon)
2. Thay đổi thông tin
3. Nhấn "Lưu"
```

### 5. Xóa sách
```
1. Nhấn icon xóa (trash icon)
2. Xác nhận
3. Sách sẽ bị ẩn nhưng dữ liệu vẫn được lưu
```

### 6. Chạy kiểm tra
```bash
cd d:\du an\bookstore\bookstore_project
python manage.py test_crud_operations
```

---

## ✨ Tính năng bổ sung

### Batch Operations
- Có thể chọn nhiều sách cùng lúc
- Thay đổi trạng thái hàng loạt
- Xóa nhiều sách cùng lúc (trong tương lai)

### Advanced Search
- Tìm theo ISBN
- Tìm theo tên tác giả
- Lọc theo khoảng giá
- Lọc theo khoảng ngày

### Performance
- Sử dụng `select_related()` để tối ưu query
- Pagination với 20 sách/trang
- Database indexing

---

## 📊 Kiểm tra danh sách

### Requirement Checklist:
- [x] 1. Hoàn thiện chức năng CRUD cho 2 bảng chính (Book, Order)
- [x] 2. Tìm kiếm, lọc, sắp xếp hoạt động đúng
- [x] 3. Cài đặt phân quyền (Guest/User/Admin)
- [x] 4. Xử lý luồng nghiệp vụ (tạo sách, quản lý kho)
- [x] 5. Trạng thái dữ liệu (available/low_stock/out_of_stock/discontinued)
- [x] 6. Kiểm tra tải file/ảnh (định dạng + kích thước)
- [x] 7. Thông báo thành công/lỗi rõ ràng (toast alerts)
- [x] 8. Code organization (MVC layered architecture)
- [x] 9. Kiểm thử CRUD operations (automated test script)

---

## 🎯 Kết luận

Tất cả các lỗi trong phần quản lý sách đã được sửa chữa. Hệ thống giờ đã:
- ✅ Hoạt động đầy đủ với CRUD operations
- ✅ Có tìm kiếm, lọc, sắp xếp
- ✅ Có phân quyền người dùng
- ✅ Có validation đầy đủ
- ✅ Có giao diện thân thiện người dùng
- ✅ Có code comment rõ ràng
- ✅ Có test script tự động

Bạn có thể bắt đầu sử dụng hệ thống quản lý sách ngay bây giờ!
