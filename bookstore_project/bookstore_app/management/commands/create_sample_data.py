from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import datetime, timedelta
import random
from bookstore_app.models import Category, Author, Publisher, Book, Cart, Wishlist

class Command(BaseCommand):
    help = 'Tạo dữ liệu mẫu cho ứng dụng'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Bắt đầu tạo dữ liệu mẫu...'))
        
        # Tạo thể loại
        self.stdout.write('📚 Tạo thể loại...')
        categories_data = [
            ('Tiểu thuyết', 'tieu-thuyet', 'Các tác phẩm tiểu thuyết hay'),
            ('Khoa học', 'khoa-hoc', 'Sách về khoa học tự nhiên'),
            ('Lịch sử', 'lich-su', 'Sách về lịch sử'),
            ('Tự giáo dục', 'tu-giao-duc', 'Sách phát triển kỹ năng'),
            ('Trẻ em', 'tre-em', 'Sách dành cho trẻ em'),
        ]
        
        categories = {}
        for name, slug, desc in categories_data:
            cat, created = Category.objects.get_or_create(
                name=name,
                defaults={'slug': slug, 'description': desc, 'is_active': True}
            )
            categories[name] = cat
            if created:
                self.stdout.write(f'  ✓ {name}')
        
        # Tạo tác giả
        self.stdout.write('👨‍✍️ Tạo tác giả...')
        authors_data = [
            ('Nguyễn Nhật Ánh', 'Tác giả Việt Nam nổi tiếng', 'Việt Nam'),
            ('Trần Hữu Tú', 'Nhà văn tài năng', 'Việt Nam'),
            ('Hương Giang', 'Biên kịch và tác giả', 'Việt Nam'),
            ('Tatiana de Rosnay', 'Tác giả Pháp - Anh', 'Pháp'),
            ('Stephen Hawking', 'Nhà vật lý lý thuyết', 'Anh'),
        ]
        
        authors = {}
        for name, bio, nationality in authors_data:
            author, created = Author.objects.get_or_create(
                name=name,
                defaults={'bio': bio, 'nationality': nationality}
            )
            authors[name] = author
            if created:
                self.stdout.write(f'  ✓ {name}')
        
        # Tạo nhà xuất bản
        self.stdout.write('🏢 Tạo nhà xuất bản...')
        publishers_data = [
            ('NXB Trẻ', '123 Nguyễn Huệ, Hà Nội', '+84 24 3938 5880'),
            ('NXB Kim Đồng', '456 Nguyễn Trãi, Hà Nội', '+84 24 3938 0011'),
            ('NXB Tuổi Trẻ', '789 Đinh Lễ, Hà Nội', '+84 24 3939 0601'),
            ('NXB Đại Học Quốc Gia', '144 Xuân Thủy, Hà Nội', '+84 24 3755 0202'),
            ('Penguin Books', 'London, UK', '+44 20 7010 3000'),
        ]
        
        publishers = {}
        for name, address, phone in publishers_data:
            pub, created = Publisher.objects.get_or_create(
                name=name,
                defaults={'address': address, 'phone': phone}
            )
            publishers[name] = pub
            if created:
                self.stdout.write(f'  ✓ {name}')
        
        # Tạo sách
        self.stdout.write('📖 Tạo sách...')
        books_data = [
            {
                'title': 'Kiếp ngoài hành tinh',
                'author': 'Nguyễn Nhật Ánh',
                'publisher': 'NXB Trẻ',
                'category': 'Tiểu thuyết',
                'description': 'Một cuốn tiểu thuyết hay về những góc khuất của cuộc sống.',
                'price': 15.99,
                'discount_price': 12.99,
                'quantity': 100,
                'isbn': '978-604-74-4365-8',
                'pages': 320,
                'published_date': '2020-03-15',
            },
            {
                'title': 'Dạy con yêu thương',
                'author': 'Trần Hữu Tú',
                'publisher': 'NXB Tuổi Trẻ',
                'category': 'Tự giáo dục',
                'description': 'Hướng dẫn nuôi dạy con cái với tình yêu thương.',
                'price': 18.50,
                'quantity': 85,
                'isbn': '978-604-74-1234-5',
                'pages': 280,
                'published_date': '2021-01-20',
            },
            {
                'title': 'Vũ trụ trong đôi mắt',
                'author': 'Stephen Hawking',
                'publisher': 'Penguin Books',
                'category': 'Khoa học',
                'description': 'Khám phá bí ẩn của vũ trụ với nhà vật lý vĩ đại.',
                'price': 22.00,
                'quantity': 60,
                'isbn': '978-0-553-38016-3',
                'pages': 368,
                'published_date': '2018-05-10',
            },
            {
                'title': 'Lịch sử Việt Nam qua các thời kỳ',
                'author': 'Hương Giang',
                'publisher': 'NXB Đại Học Quốc Gia',
                'category': 'Lịch sử',
                'description': 'Tìm hiểu lịch sử Việt Nam từ thời cổ đại đến hiện đại.',
                'price': 25.00,
                'discount_price': 19.99,
                'quantity': 70,
                'isbn': '978-604-67-0123-4',
                'pages': 450,
                'published_date': '2019-07-25',
            },
            {
                'title': 'Cô bé mồ côi và những chuyện lạ kỳ',
                'author': 'Tatiana de Rosnay',
                'publisher': 'NXB Kim Đồng',
                'category': 'Tiểu thuyết',
                'description': 'Một câu chuyện cảm xúc về những mộng ước và hiện thực.',
                'price': 17.50,
                'quantity': 90,
                'isbn': '978-2-02-098765-4',
                'pages': 312,
                'published_date': '2020-09-12',
            },
            {
                'title': 'Chuyện Kỳ Duyên',
                'author': 'Nguyễn Nhật Ánh',
                'publisher': 'NXB Trẻ',
                'category': 'Tiểu thuyết',
                'description': 'Những câu chuyện kỳ diệu từ xứ sở hương hoa.',
                'price': 14.99,
                'quantity': 110,
                'isbn': '978-604-74-5678-9',
                'pages': 256,
                'published_date': '2021-06-18',
            },
            {
                'title': 'Khám phá khoa học cơ bản',
                'author': 'Stephen Hawking',
                'publisher': 'Penguin Books',
                'category': 'Khoa học',
                'description': 'Giới thiệu các khái niệm khoa học cơ bản cho mọi người.',
                'price': 19.99,
                'quantity': 75,
                'isbn': '978-0-553-21311-3',
                'pages': 340,
                'published_date': '2019-02-28',
            },
        ]
        
        for book_data in books_data:
            author_name = book_data.pop('author')
            publisher_name = book_data.pop('publisher')
            category_name = book_data.pop('category')
            
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults={
                    **book_data,
                    'author': authors[author_name],
                    'publisher': publishers[publisher_name],
                    'category': categories[category_name],
                    'slug': slugify(book_data['title']),
                    'status': 'available',
                    'rating': random.uniform(3.5, 5.0),
                    'reviews_count': random.randint(5, 50),
                }
            )
            if created:
                self.stdout.write(f'  ✓ {book_data["title"]}')
        
        # Tạo người dùng mẫu
        self.stdout.write('👥 Tạo người dùng mẫu...')
        users_data = [
            ('user1', 'user1@example.com', 'user123'),
            ('user2', 'user2@example.com', 'user123'),
            ('user3', 'user3@example.com', 'user123'),
        ]
        
        for username, email, password in users_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email}
            )
            if created:
                user.set_password(password)
                user.save()
                Cart.objects.get_or_create(user=user)
                Wishlist.objects.get_or_create(user=user)
                self.stdout.write(f'  ✓ {username}')
        
        self.stdout.write(self.style.SUCCESS('✅ Tạo dữ liệu mẫu hoàn tất!'))
        self.stdout.write(self.style.WARNING('\n📝 Tài khoản mẫu:'))
        self.stdout.write('   Admin: admin / admin123')
        self.stdout.write('   User 1: user1 / user123')
        self.stdout.write('   User 2: user2 / user123')
