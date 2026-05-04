#!/bin/bash
# setup.sh - Setup script for BookStore

echo "🚀 Bắt đầu cài đặt BookStore..."

# Create virtual environment
echo "📦 Tạo virtual environment..."
python -m venv venv

# Activate virtual environment
echo "🔌 Kích hoạt virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Cài đặt dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️ Khởi tạo database..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "👤 Tạo tài khoản admin..."
python manage.py createsuperuser

# Collect static files
echo "📁 Thu thập static files..."
python manage.py collectstatic --noinput

echo "✅ Cài đặt hoàn tất!"
echo "🌐 Chạy: python manage.py runserver"
echo "📍 Truy cập: http://localhost:8000"
echo "👨‍💼 Admin: http://localhost:8000/admin/"
