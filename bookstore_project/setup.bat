@echo off
REM setup.bat - Setup script for BookStore on Windows

echo 🚀 Bắt đầu cài đặt BookStore...

REM Create virtual environment
echo 📦 Tạo virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔌 Kích hoạt virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📚 Cài đặt dependencies...
pip install -r requirements.txt

REM Run migrations
echo 🗄️ Khởi tạo database...
python manage.py makemigrations
python manage.py migrate

REM Create sample data
echo 📖 Tạo dữ liệu mẫu...
python manage.py create_sample_data

REM Create superuser (optional)
echo 👤 Để tạo tài khoản admin, chạy: python manage.py createsuperuser

echo.
echo ✅ Cài đặt hoàn tất!
echo.
echo 🌐 Chạy ứng dụng: python manage.py runserver
echo 📍 Truy cập: http://localhost:8000
echo 👨‍💼 Admin: http://localhost:8000/admin/
echo.
echo 📝 Tài khoản mẫu (sau khi chạy create_sample_data):
echo    user1 / user123
echo    user2 / user123
echo.
pause
