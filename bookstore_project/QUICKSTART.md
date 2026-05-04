# Hướng dẫn cài đặt nhanh - BookStore

## ⚡ Bắt đầu trong 5 phút

### Bước 1: Tải dự án
```bash
cd "c:/Users/Admin/du an/bookstore/bookstore_project"
```

### Bước 2: Thiết lập môi trường
```bash
# Tạo virtual environment
python -m venv venv
venv\Scripts\activate

# Cài đặt packages
pip install -r requirements.txt
```

### Bước 3: Khởi tạo database
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Bước 4: Chạy ứng dụng
```bash
python manage.py runserver
```

### Bước 5: Truy cập
- Trang chủ: http://localhost:8000
- Admin: http://localhost:8000/admin/

## 🎬 Tạo dữ liệu mẫu

```bash
# Tạo thể loại
python manage.py shell
>>> from bookstore_app.models import Category
>>> Category.objects.create(name='Tiểu thuyết', slug='tieu-thuyet')
>>> Category.objects.create(name='Khoa học', slug='khoa-hoc')

# Tạo tác giả
>>> from bookstore_app.models import Author
>>> Author.objects.create(name='Nguyễn Nhật Ánh', bio='Tác giả Việt Nam nổi tiếng')

# Tạo sách
>>> from bookstore_app.models import Book
>>> book = Book.objects.create(
...     title='Kiếp ngoài hành tinh',
...     author_id=1,
...     category_id=1,
...     description='Một tác phẩm kinh điển',
...     price=15.99,
...     quantity=50,
...     isbn='978-3-16-148410-0',
...     published_date='2020-01-01',
...     status='available'
... )
```

## 🔐 Tạo tài khoản test

```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: admin123
```

## 📦 Cấu trúc thư mục

```
bookstore_project/
├── bookstore_app/           # Ứng dụng chính
│   ├── models.py           # Database models
│   ├── views.py            # View logic
│   ├── forms.py            # Forms
│   ├── urls.py             # Routes
│   └── admin.py            # Admin customization
├── templates/              # HTML templates
│   └── bookstore_app/
├── static/                 # CSS, JS, images
├── media/                  # User uploaded files
├── bookstore_config/       # Project settings
├── manage.py              # Django CLI
└── requirements.txt       # Dependencies
```

## 🌐 URLs chính

```
Công khai:
  /                     - Trang chủ
  /books/               - Danh sách sách
  /books/<slug>/        - Chi tiết sách
  /register/            - Đăng ký
  /login/               - Đăng nhập
  /password-reset/      - Quên mật khẩu

Người dùng đã đăng nhập:
  /cart/                - Giỏ hàng
  /checkout/            - Thanh toán
  /orders/              - Đơn hàng
  /orders/<id>/         - Chi tiết đơn hàng
  /wishlist/            - Danh sách yêu thích
  /profile/             - Hồ sơ cá nhân

Admin:
  /admin/               - Trang quản lý Django
  /admin-dashboard/     - Bảng điều khiển
  /manage-books/        - Quản lý sách
  /create-book/         - Tạo sách mới
  /edit-book/<id>/      - Sửa sách
  /delete-book/<id>/    - Xóa sách

API:
  /api/                 - API root
  /api/books/           - Danh sách API
  /api/categories/      - Thể loại API
  /api/stats/           - Thống kê
```

## 📊 Thực thể dữ liệu

```
User
├── Cart
│   └── CartItem
│       └── Book
├── Order
│   └── OrderItem
│       └── Book
├── Wishlist
│   └── Books
└── Review
    └── Book

Book
├── Category
├── Author
├── Publisher
└── Review
```

## 🔍 Tìm kiếm & Lọc

Tính năng tìm kiếm hỗ trợ:
- Tìm kiếm theo tên, ISBN
- Lọc theo thể loại
- Lọc theo tác giả
- Lọc theo khoảng giá
- Sắp xếp theo: mới nhất, giá, đánh giá

## 💳 Thanh toán (Tạo đơn hàng)

1. Thêm sách vào giỏ
2. Xem giỏ hàng
3. Click "Thanh toán"
4. Điền thông tin giao hàng
5. Đặt đơn hàng

Admin sẽ xử lý thanh toán từ trang quản lý.

## 📧 Email

Hiện tại sử dụng console backend (in ra terminal). Để sử dụng Gmail:

1. Bật "Less secure app access" trên Gmail
2. Cập nhật `.env`:
```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🚀 Deploy

### Với Heroku:
```bash
git init
git add .
git commit -m "Initial commit"
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
```

### Với PythonAnywhere:
1. Upload mã
2. Tạo virtual env
3. Cấu hình WSGI
4. Chạy migrate

## ⚙️ Settings quan trọng

File `bookstore_config/settings.py`:
- `DEBUG = True` (chỉ phát triển)
- `SECRET_KEY` - Thay đổi production
- `ALLOWED_HOSTS` - Thêm domain
- `DATABASES` - Cấu hình DB
- `MEDIA_ROOT`, `STATIC_ROOT` - Đường dẫn file

## 📞 Support

Gặp lỗi? Kiểm tra:
1. Logs trong terminal
2. Check database migrations: `python manage.py showmigrations`
3. Xóa cache: `python manage.py clear_cache`
4. Check static files: `python manage.py collectstatic`

---

**Chúc bạn phát triển vui vẻ! 🎉**
