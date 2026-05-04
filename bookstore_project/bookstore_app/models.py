# Django
from decimal import Decimal, ROUND_HALF_UP

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.shortcuts import reverse

# Category Model
class Category(models.Model):
    """Product categories"""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


# Author Model
class Author(models.Model):
    """Book authors"""
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='authors/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


# Publisher Model
class Publisher(models.Model):
    """Book publishers"""
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    established_year = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


# Book/Product Model
class Book(models.Model):
    """Book products"""
    STATUS_CHOICES = [
        ('available', 'Còn hàng'),
        ('low_stock', 'Sắp hết hàng'),
        ('out_of_stock', 'Hết hàng'),
        ('discontinued', 'Ngừng bán'),
    ]
    
    title = models.CharField('Tiêu đề', max_length=300)
    slug = models.SlugField('Slug (URL)', max_length=300, unique=True)
    author = models.ForeignKey(Author, verbose_name='Tác giả', on_delete=models.SET_NULL, null=True, related_name='books')
    publisher = models.ForeignKey(Publisher, verbose_name='Nhà xuất bản', on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    category = models.ForeignKey(Category, verbose_name='Thể loại', on_delete=models.SET_NULL, null=True, related_name='books')
    
    description = models.TextField('Mô tả đầy đủ')
    short_description = models.CharField('Mô tả ngắn', max_length=500, blank=True)
    cover_image = models.ImageField('Ảnh bìa', upload_to='books/')
    
    price = models.DecimalField(
        'Giá bìa (VNĐ)',
        max_digits=12,
        decimal_places=0,
        validators=[MinValueValidator(0)],
        help_text='Số tiền Việt Nam Đồng, không quy đổi.',
    )
    discount_price = models.DecimalField(
        'Giá khuyến mãi (VNĐ)',
        max_digits=12,
        decimal_places=0,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text='Để trống nếu không giảm giá.',
    )
    quantity = models.IntegerField('Số lượng tồn kho', validators=[MinValueValidator(0)])
    
    pages = models.IntegerField('Số trang', null=True, blank=True)
    isbn = models.CharField('Mã ISBN', max_length=20, unique=True)
    published_date = models.DateField('Ngày xuất bản')
    language = models.CharField('Ngôn ngữ', max_length=50, default='Tiếng Việt')
    
    rating = models.FloatField('Điểm trung bình', default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    reviews_count = models.IntegerField('Số lượt đánh giá', default=0)
    
    status = models.CharField(
        'Trạng thái kho',
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
    )
    
    created_by = models.ForeignKey(
        User, verbose_name='Người tạo', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_books'
    )
    created_at = models.DateTimeField('Ngày tạo', auto_now_add=True)
    updated_at = models.DateTimeField('Ngày cập nhật', auto_now=True)
    is_featured = models.BooleanField('Sách nổi bật', default=False)
    is_active = models.BooleanField('Hiển thị trên cửa hàng', default=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'status']),
            models.Index(fields=['author']),
            models.Index(fields=['is_featured']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'slug': self.slug})
    
    def get_price_vnd(self):
        """Giá bìa hiển thị (VNĐ) — trùng trường price."""
        if self.price is None:
            return 0
        return int(Decimal(str(self.price)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

    def get_discount_price_vnd(self):
        if self.discount_price is None:
            return None
        return int(Decimal(str(self.discount_price)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

    def get_current_price(self):
        """Đơn giá bán hiện tại (VNĐ, Decimal)."""
        return self.discount_price if self.discount_price is not None else self.price

    def get_current_price_vnd(self):
        return self.get_discount_price_vnd() or self.get_price_vnd()

    def get_discount_percentage(self):
        if self.discount_price and self.price and self.price > 0:
            discount = ((self.price - self.discount_price) / self.price) * 100
            return max(0, int(discount))
        return 0


# Review/Rating Model
class Review(models.Model):
    """Book reviews and ratings"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    content = models.TextField()
    helpful_count = models.IntegerField(default=0)
    is_verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('book', 'user')
    
    def __str__(self):
        return f"{self.book.title} - {self.rating} stars by {self.user.username}"


# Cart Model
class Cart(models.Model):
    """Shopping cart"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart for {self.user.username}"
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_price_vnd(self):
        """Tổng tiền giỏ (VNĐ) — dùng hiển thị; get_total_price() cùng đơn vị (VNĐ)."""
        return sum(item.get_total_price_vnd() for item in self.items.all())
    
    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())


# CartItem Model
class CartItem(models.Model):
    """Items in shopping cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('cart', 'book')
    
    def __str__(self):
        return f"{self.quantity}x {self.book.title} in {self.cart.user.username}'s cart"
    
    def get_total_price(self):
        return self.book.get_current_price() * self.quantity

    def get_total_price_vnd(self):
        """Thành tiền dòng (VNĐ) = đơn giá VNĐ × số lượng."""
        return self.book.get_current_price_vnd() * self.quantity


# Order Model
class Order(models.Model):
    """Customer orders"""
    ORDER_STATUS = [
        ('pending', 'Chờ xử lý'),
        ('confirmed', 'Đã xác nhận'),
        ('processing', 'Đang xử lý'),
        ('shipped', 'Đã giao hàng'),
        ('delivered', 'Giao hàng thành công'),
        ('cancelled', 'Đã hủy'),
        ('returned', 'Đã hoàn trả'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Chờ thanh toán'),
        ('paid', 'Đã thanh toán'),
        ('failed', 'Thanh toán thất bại'),
        ('refunded', 'Đã hoàn tiền'),
    ]
    
    order_id = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    
    # Customer info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Shipping info
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='Vietnam')
    
    # Order details
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            import uuid
            self.order_id = f"ORD-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


# OrderItem Model
class OrderItem(models.Model):
    """Items in orders"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of order
    
    def __str__(self):
        title = self.book.title if self.book else '(đã xóa)'
        return f"{self.quantity}x {title} in Order {self.order.order_id}"
    
    def get_total_price(self):
        return self.price * self.quantity


# Wishlist Model
class Wishlist(models.Model):
    """User wishlist"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    books = models.ManyToManyField(Book, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Wishlist for {self.user.username}"
