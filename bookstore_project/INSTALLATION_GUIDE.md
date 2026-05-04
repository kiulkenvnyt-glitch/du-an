# 📖 HƯỚNG DẪN HOÀN CHỈNH - BookStore Project

## ✨ Tổng Quan Dự Án

**BookStore** là ứng dụng web quản lý bán sách hoàn chỉnh, được phát triển bằng **Django Framework**. Ứng dụng cung cấp một nền tảng mạnh mẽ cho cửa hàng bán sách trực tuyến với đầy đủ tính năng từ phía người dùng đến quản lý.

### 🎯 Mục Tiêu Dự Án

1. **Xây dựng ứng dụng web hoàn chỉnh** với cơ sở dữ liệu quan hệ
2. **Quản lý 5+ thực thể dữ liệu** có liên kết (Users, Books, Orders, Reviews, Categories)
3. **Cung cấp giao diện người dùng** thân thiện và responsive
4. **Triển khai chức năng nghiệp vụ** đầy đủ từ đầu đến cuối

## 🏗️ Kiến Trúc Hệ Thống

### Công Nghệ Sử Dụng

```
Frontend:
├── HTML5
├── Bootstrap 5 (CSS Framework)
├── Font Awesome (Icons)
└── Vanilla JavaScript

Backend:
├── Django 4.2 (Web Framework)
├── Django REST Framework (API)
├── SQLite/PostgreSQL (Database)
└── Pillow (Image Processing)

DevOps:
├── Git (Version Control)
├── Virtual Environment (Python)
└── pip (Package Manager)
```

### Kiến Trúc MVC

```
Models (bookstore_app/models.py)
   ↓
Views (bookstore_app/views.py)
   ↓
Templates (templates/bookstore_app/*.html)
   ↓
URLs (bookstore_app/urls.py)
```

## 📊 Cơ Sở Dữ Liệu

### 11 Thực Thể Chính

1. **User** - Người dùng hệ thống (tích hợp Django)
2. **Category** - Thể loại sách
3. **Author** - Tác giả sách
4. **Publisher** - Nhà xuất bản
5. **Book** - Sản phẩm sách
6. **Review** - Đánh giá & nhận xét
7. **Cart** - Giỏ hàng
8. **CartItem** - Sản phẩm trong giỏ
9. **Order** - Đơn hàng
10. **OrderItem** - Sản phẩm trong đơn hàng
11. **Wishlist** - Danh sách yêu thích

### Quan Hệ Dữ Liệu

```
User (1) ──→ (1) Cart
         ├──→ (M) Order
         ├──→ (1) Wishlist
         └──→ (M) Review

Book (1) ──→ (M) Review
      ├──→ (M) CartItem
      ├──→ (M) OrderItem
      ├──→ (1) Author
      ├──→ (1) Publisher
      └──→ (1) Category

Cart (1) ──→ (M) CartItem
Order (1) ──→ (M) OrderItem
Wishlist (1) ──→ (M) Book
```

## 🎯 Chức Năng Chính (6+ Features)

### 1. ✅ Xác Thực & Phân Quyền

**Đăng ký (Register)**
- Form validation
- Email uniqueness check
- Password strength validation
- Auto create Cart & Wishlist

**Đăng nhập (Login)**
- Session management
- Remember functionality
- Redirect to intended page
- Error handling

**Quên mật khẩu**
- Email verification
- Reset token generation
- Password reset link

**Phân quyền theo vai trò**
- Guest: View public content
- User: Full CRUD operations
- Admin: Manage all entities

### 2. ✅ Quản Lý Sách (CRUD)

**Create (Tạo sách mới)**
```
POST /create-book/
- Yêu cầu: Admin
- Fields: Title, Author, Category, Price, etc.
- Upload cover image
- Auto slug generation
```

**Read (Xem sách)**
```
GET /books/ - List all books
GET /books/<slug>/ - Book detail
Features:
- Pagination (12 items/page)
- Advanced search
- Filter by category, author, price
- Sort by: latest, price, rating
```

**Update (Sửa sách)**
```
POST /edit-book/<id>/
- Yêu cầu: Admin
- Update all fields
- Re-upload image
```

**Delete (Xóa sách)**
```
POST /delete-book/<id>/
- Yêu cầu: Admin
- Soft delete option
- Confirmation dialog
```

### 3. ✅ Tìm Kiếm & Lọc

**Search Features**
- Full-text search by title, ISBN
- Search by author name
- Case-insensitive matching

**Filter Options**
- By category
- By price range (min-max)
- By author
- By status (available, out_of_stock)

**Sort Options**
- Newest first
- Price: Low to High
- Price: High to Low
- Highest Rating
- Best Sellers

### 4. ✅ Giỏ Hàng & Đặt Hàng

**Shopping Cart**
```
Add to Cart:
- POST /cart/add/<book_id>/
- Quantity selection
- Item validation (stock check)
- AJAX support

Update Cart:
- POST /cart/update/<item_id>/
- Quantity modification
- Real-time total calculation

Remove Item:
- POST /cart/remove/<item_id>/
- Item deletion
- Stock restoration
```

**Checkout & Order Creation**
```
Process:
1. View cart (/cart/)
2. Click checkout
3. Fill shipping info
4. Review order
5. Submit (/checkout/)
6. Order confirmation

Order Details:
- Auto-generated Order ID
- Customer info
- Shipping address
- Item list
- Total calculation
- Status tracking
```

### 5. ✅ Đánh Giá & Bình Luận (2 Workflows)

**Workflow 1: User Reviews Book**
```
Before:
- User views book detail
- User has purchased the book
- No previous review

Action:
- Click "Write Review"
- Select rating (1-5 stars)
- Enter title & content
- Submit

After:
- Review saved
- Book rating updated
- Review appears in list
- User badge (Verified Purchase)
```

**Workflow 2: Moderate Reviews**
```
Admin:
- View all reviews
- Mark as helpful
- Hide inappropriate reviews
- Respond to reviews
```

### 6. ✅ Thống Kê & Báo Cáo

**Dashboard Metrics**
```
/admin-dashboard/

Real-time Stats:
- Total Books: 15
- Total Users: 50
- Total Orders: 200
- Total Revenue: $5,000

Charts:
- Orders by status (pie/bar)
- Revenue by date (line graph - 7 days)
- Top selling books (top 5)
- User growth
```

## 🔧 Hướng Dẫn Cài Đặt Chi Tiết

### Yêu Cầu Hệ Thống
- Python 3.8+
- pip (Python package manager)
- Git
- 2GB disk space

### Bước 1: Clone/Download Dự Án

```bash
# Nếu từ git
git clone <repository-url>

# Hoặc vào thư mục dự án
cd "c:/Users/Admin/du an/bookstore/bookstore_project"
```

### Bước 2: Tạo Virtual Environment

```bash
# Tạo venv
python -m venv venv

# Kích hoạt venv (Windows)
venv\Scripts\activate

# Kích hoạt venv (Linux/Mac)
source venv/bin/activate
```

### Bước 3: Cài Đặt Dependencies

```bash
# Cập nhật pip
python -m pip install --upgrade pip

# Cài đặt requirements
python -m pip install -r requirements.txt
```

### Bước 4: Cấu Hình Môi Trường

```bash
# Copy .env.example thành .env
cp .env.example .env

# Sửa file .env
# SECRET_KEY=your-secret-key
# DEBUG=True
# DATABASE_URL=sqlite:///db.sqlite3
```

### Bước 5: Khởi Tạo Database

```bash
# Tạo migrations
python manage.py makemigrations

# Áp dụng migrations
python manage.py migrate

# Kiểm tra database
python manage.py showmigrations
```

### Bước 6: Tạo Dữ Liệu Mẫu

```bash
# Tạo dữ liệu sample (categories, authors, books, users)
python manage.py create_sample_data

# Hoặc tạo manual:
python manage.py shell
>>> from bookstore_app.models import Category
>>> cat = Category.objects.create(name='Fiction', slug='fiction')
```

### Bước 7: Tạo Tài Khoản Admin

```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: admin123456
```

### Bước 8: Chạy Development Server

```bash
python manage.py runserver
# Hoặc chỉ định port
python manage.py runserver 8001
```

### Bước 9: Truy Cập Ứng Dụng

```
Website: http://localhost:8000
Admin: http://localhost:8000/admin/
API: http://localhost:8000/api/
```

## 📝 Tài Khoản Mẫu

| Username | Email | Password | Role |
|----------|-------|----------|------|
| admin | admin@example.com | admin123 | Admin |
| user1 | user1@example.com | user123 | Customer |
| user2 | user2@example.com | user123 | Customer |
| user3 | user3@example.com | user123 | Customer |

## 🌐 API Endpoints

### Books API
```
GET /api/books/                    - List all books
GET /api/books/<id>/               - Book detail
GET /api/books/?search=title       - Search
GET /api/books/?category=1         - Filter by category
GET /api/books/?ordering=-price    - Sort
```

### Categories API
```
GET /api/categories/               - List all categories
GET /api/categories/<id>/          - Category detail
```

### Authors API
```
GET /api/authors/                  - List all authors
GET /api/authors/<id>/             - Author detail
```

### Reviews API
```
GET /api/reviews/                  - List all reviews
GET /api/reviews/?book=<id>        - Book reviews
```

### Orders API (Auth Required)
```
GET /api/orders/                   - User's orders
GET /api/orders/<id>/              - Order detail
```

### Statistics
```
GET /api/stats/                    - General statistics
```

## 🎨 Giao Diện & UX

### Pages & Layout

1. **Home** (`/`)
   - Featured books carousel
   - Best sellers section
   - Top rated books
   - Category navigation

2. **Books** (`/books/`)
   - Sidebar filters
   - Book grid (12 per page)
   - Search & sort options
   - Pagination

3. **Book Detail** (`/books/<slug>/`)
   - Large book cover
   - Detailed information
   - Related books
   - Review section
   - Add to cart button

4. **Shopping Cart** (`/cart/`)
   - Item list with images
   - Quantity controls
   - Subtotal per item
   - Order summary
   - Checkout button

5. **Checkout** (`/checkout/`)
   - Shipping form
   - Billing info
   - Order review
   - Submit order

6. **Orders** (`/orders/`)
   - Order history table
   - Status badges
   - Order details link
   - Filter options

7. **Wishlist** (`/wishlist/`)
   - Favorite books grid
   - Move to cart
   - Remove option

8. **Admin Dashboard** (`/admin-dashboard/`)
   - Statistics cards
   - Charts & graphs
   - Quick actions

### Responsive Design

```
Desktop (1200px+):
- 3-column layout
- Full sidebar

Tablet (768px-1199px):
- 2-column layout
- Collapsible sidebar

Mobile (<768px):
- 1-column layout
- Hamburger menu
- Bottom navigation
```

## 🔐 Fitur Keamanan

1. **Authentication**
   - Secure password hashing
   - Session management
   - CSRF protection
   - XSS prevention

2. **Authorization**
   - Role-based access control
   - User permission checking
   - Admin-only views protection

3. **Data Validation**
   - Form validation
   - File upload checks
   - SQL injection prevention
   - Input sanitization

4. **API Security**
   - Token-based auth (optional)
   - Rate limiting (optional)
   - CORS configuration

## 📈 Performance Optimization

1. **Database**
   - Query optimization
   - Index creation
   - Select_related for joins
   - Pagination

2. **Frontend**
   - Static file minification
   - Image optimization
   - CSS/JS bundling
   - Lazy loading

3. **Caching**
   - Template fragment caching
   - Database query caching
   - Static file caching

## 🧪 Testing

### Unit Tests (Optional)
```bash
python manage.py test bookstore_app

# Specific test
python manage.py test bookstore_app.tests.BookTestCase
```

### Manual Testing Checklist
- [ ] User registration
- [ ] User login
- [ ] Book search & filter
- [ ] Add to cart
- [ ] Checkout process
- [ ] Order creation
- [ ] Admin panel access
- [ ] Book management (CRUD)
- [ ] Review submission

## 🚀 Deployment

### Heroku Deployment
```bash
# Install heroku CLI
# Login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main

# Migrate database
heroku run python manage.py migrate
```

### PythonAnywhere Deployment
1. Upload code
2. Create virtual environment
3. Install requirements
4. Configure WSGI
5. Set up database
6. Reload web app

### AWS/DigitalOcean Deployment
- Use Gunicorn as application server
- Use Nginx as reverse proxy
- Configure PostgreSQL database
- Set up static file serving

## 📚 Thư Mục Dự Án

```
bookstore_project/
├── bookstore_app/              # Main app
│   ├── models.py              # Database models (11 entities)
│   ├── views.py               # Views (18+ functions)
│   ├── forms.py               # Forms for CRUD
│   ├── urls.py                # URL routing
│   ├── admin.py               # Admin customization
│   ├── serializers.py         # DRF serializers
│   ├── api_views.py           # API viewsets
│   ├── api_urls.py            # API routes
│   ├── context_processors.py  # Template context
│   ├── management/            # Management commands
│   │   └── commands/
│   │       └── create_sample_data.py
│   └── migrations/            # Database migrations
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   └── bookstore_app/        # App templates (15+ files)
├── static/                   # CSS, JS, images
├── media/                    # User uploads
├── bookstore_config/         # Project config
│   ├── settings.py           # Configuration
│   ├── urls.py               # Main routing
│   └── wsgi.py               # WSGI config
├── manage.py                 # Django CLI
├── requirements.txt          # Dependencies
├── README.md                 # Documentation
├── QUICKSTART.md             # Quick guide
├── .env.example              # Env template
├── .gitignore                # Git ignore
├── setup.bat                 # Windows setup
└── setup.sh                  # Linux setup
```

## 🔧 Các Lệnh Django Hữu Ích

```bash
# Management Commands
python manage.py runserver              # Start dev server
python manage.py migrate                # Apply migrations
python manage.py makemigrations         # Create migrations
python manage.py createsuperuser        # Create admin
python manage.py create_sample_data     # Sample data
python manage.py shell                  # Interactive shell
python manage.py collectstatic          # Gather static files
python manage.py check                  # Check for errors
python manage.py test                   # Run tests
```

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'django'"
```bash
# Đảm bảo venv được kích hoạt
venv\Scripts\activate
python -m pip install -r requirements.txt
```

### "No such table" error
```bash
python manage.py migrate --run-syncdb
```

### Static files not showing
```bash
python manage.py collectstatic --noinput
```

### Port 8000 đang được dùng
```bash
python manage.py runserver 8001
```

### Database locked
```bash
# Xóa db.sqlite3 và tạo lại
rm db.sqlite3
python manage.py migrate
python manage.py create_sample_data
```

## 📞 Hỗ Trợ

- **Tài liệu Django**: https://docs.djangoproject.com/
- **Django REST**: https://www.django-rest-framework.org/
- **Bootstrap**: https://getbootstrap.com/

## 📄 License

MIT License - Tự do sử dụng, sửa đổi và phân phối

---

**BookStore - Ứng dụng web bán sách hoàn chỉnh | Made with ❤️ for book lovers**
