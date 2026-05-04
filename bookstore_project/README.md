# 📚 BookStore - Ứng dụng web bán sách

Ứng dụng quản lý cửa hàng bán sách trực tuyến hoàn chỉnh, được xây dựng bằng Django với các tính năng hiện đại.

## 🎯 Tính năng chính

### 1. Xác thực & Phân quyền
- ✅ Đăng ký, đăng nhập, đăng xuất
- ✅ Quên mật khẩu & đặt lại mật khẩu
- ✅ Phân quyền theo vai trò (Guest, User, Admin)
- ✅ Quản lý hồ sơ cá nhân

### 2. Quản lý Sách (CRUD)
- ✅ Thêm, xem, sửa, xóa sách
- ✅ Tìm kiếm, lọc, sắp xếp sách
- ✅ Phân loại theo thể loại
- ✅ Xem chi tiết sách
- ✅ Quản lý tác giả & nhà xuất bản

### 3. Quản lý Đơn hàng
- ✅ Thêm sách vào giỏ hàng
- ✅ Cập nhật số lượng, xóa sách khỏi giỏ
- ✅ Tạo đơn hàng từ giỏ hàng
- ✅ Xem lịch sử đơn hàng
- ✅ Theo dõi trạng thái đơn hàng

### 4. Danh sách yêu thích
- ✅ Thêm/xóa sách khỏi wishlist
- ✅ Xem danh sách sách yêu thích

### 5. Đánh giá & Bình luận
- ✅ Viết đánh giá sách
- ✅ Xem đánh giá từ người dùng khác
- ✅ Tính toán rating trung bình

### 6. Bảng điều khiển Admin
- ✅ Thống kê doanh thu
- ✅ Báo cáo đơn hàng
- ✅ Sách bán chạy nhất
- ✅ Quản lý người dùng & quyền hạn

### 7. API REST
- ✅ API lấy danh sách sách
- ✅ API tìm kiếm & lọc
- ✅ API lấy thông tin đơn hàng
- ✅ API thống kê

## 🏗️ Kiến trúc & Công nghệ

### Backend
- **Framework**: Django 4.2
- **Database**: SQLite (phát triển), PostgreSQL (production)
- **Authentication**: Django's built-in auth system
- **API**: Django REST Framework

### Frontend
- **Template Engine**: Django Templates
- **CSS Framework**: Bootstrap 5
- **Icons**: Font Awesome 6
- **JavaScript**: Vanilla JS, Bootstrap JS

### Package quan trọng
- `djangorestframework`: REST API
- `django-crispy-forms`: Form rendering
- `django-filter`: Advanced filtering
- `Pillow`: Image processing
- `python-decouple`: Environment variables

## 📊 Mô hình dữ liệu

### Thực thể chính:
1. **User** - Người dùng hệ thống
2. **Book** - Sách/sản phẩm
3. **Category** - Thể loại sách
4. **Author** - Tác giả
5. **Publisher** - Nhà xuất bản
6. **Review** - Đánh giá sách
7. **Cart** - Giỏ hàng
8. **CartItem** - Sản phẩm trong giỏ
9. **Order** - Đơn hàng
10. **OrderItem** - Sản phẩm trong đơn hàng
11. **Wishlist** - Danh sách yêu thích

## 🚀 Hướng dẫn cài đặt

### 1. Clone hoặc tải dự án
```bash
cd "c:/Users/Admin/du an/bookstore/bookstore_project"
```

### 2. Tạo virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Cấu hình environment
Tạo file `.env` trong thư mục gốc:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
```

### 5. Tạo database & migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Tạo tài khoản admin
```bash
python manage.py createsuperuser
```

### 7. Tạo dữ liệu mẫu (tùy chọn)
```bash
python manage.py loaddata sample_data.json
```

### 8. Chạy development server
```bash
python manage.py runserver
```

Truy cập: http://localhost:8000

## 📝 Tài khoản mẫu

| Username | Password | Vai trò |
|----------|----------|---------|
| admin | admin123 | Admin |
| user1 | user123 | User |
| user2 | user123 | User |

## 🔗 Các URL chính

| URL | Mô tả |
|-----|-------|
| `/` | Trang chủ |
| `/books/` | Danh sách sách |
| `/cart/` | Giỏ hàng |
| `/checkout/` | Thanh toán |
| `/orders/` | Lịch sử đơn hàng |
| `/wishlist/` | Danh sách yêu thích |
| `/admin/` | Quản lý Django |
| `/admin-dashboard/` | Bảng điều khiển admin |
| `/api/books/` | API sách |
| `/api/categories/` | API thể loại |

## 🔧 Lệnh Django hữu ích

```bash
# Tạo migrations
python manage.py makemigrations

# Áp dụng migrations
python manage.py migrate

# Tạo superuser
python manage.py createsuperuser

# Thu thập static files
python manage.py collectstatic

# Shell Django
python manage.py shell

# Chạy tests
python manage.py test

# Kiểm tra lỗi
python manage.py check
```

## 📱 Responsive Design

Ứng dụng được thiết kế fully responsive cho:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)

## 🔐 Bảo mật

- ✅ CSRF protection
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ Password hashing
- ✅ User authentication required cho sensitive operations
- ✅ File upload validation

## 📈 Tối ưu hóa

- ✅ Database indexing
- ✅ Query optimization
- ✅ Static file caching
- ✅ Pagination
- ✅ Lazy loading images

## 🐛 Troubleshooting

### Lỗi: Module not found
```bash
pip install -r requirements.txt
```

### Lỗi: Database error
```bash
python manage.py migrate --run-syncdb
```

### Static files không load
```bash
python manage.py collectstatic --noinput
```

### Port 8000 đang được sử dụng
```bash
python manage.py runserver 8001
```

## 📚 Tài liệu thêm

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.0/)

## 👨‍💻 Phát triển thêm

Những tính năng có thể thêm:
- [ ] Thanh toán online (Stripe, PayPal)
- [ ] Email notification
- [ ] SMS notification
- [ ] Image gallery
- [ ] Book recommendations (ML)
- [ ] Discussion forums
- [ ] Social features (Follow authors)
- [ ] Mobile app

## 📄 License

MIT License - Tự do sử dụng

## ✉️ Liên hệ

- Email: support@bookstore.com
- Website: https://bookstore.com
- Phone: +84 (0) 123 456 789

---

**Made with ❤️ for book lovers**
