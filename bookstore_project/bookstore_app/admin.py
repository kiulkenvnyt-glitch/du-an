from django.contrib import admin
from django.utils.html import format_html
from bookstore_app.forms import BookAdminForm
from bookstore_app.models import (
    Category, Author, Publisher, Book, Review, Cart, CartItem,
    Order, OrderItem, Wishlist
)

def format_vnd(value):
    try:
        return f"{int(round(float(value))):,}".replace(",", ".") + " đ"
    except (TypeError, ValueError):
        return value

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


# Author Admin
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'nationality', 'birth_date')
    list_filter = ('nationality', 'created_at')
    search_fields = ('name', 'bio')


# Publisher Admin
@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email', 'website')


# Book Admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm
    list_display = ('title', 'author', 'category', 'price_display', 'quantity', 'status', 'is_featured', 'rating_display')
    list_filter = ('status', 'category', 'author', 'is_featured', 'is_active', 'created_at')
    search_fields = ('title', 'isbn', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('title', 'slug', 'description', 'short_description', 'cover_image')
        }),
        ('Tác giả & Nhà xuất bản', {
            'fields': ('author', 'publisher', 'category')
        }),
        ('Giá & Kho (nhập VNĐ)', {
            'fields': ('price', 'discount_price', 'quantity', 'status'),
            'description': 'Giá bìa và giá khuyến mãi nhập bằng VNĐ (số nguyên đồng), lưu đúng giá trị đã nhập.',
        }),
        ('Chi tiết sách', {
            'fields': ('isbn', 'pages', 'language', 'published_date')
        }),
        ('Đánh giá', {
            'fields': ('rating', 'reviews_count')
        }),
        ('Cài đặt', {
            'fields': ('is_featured', 'is_active', 'created_by', 'created_at', 'updated_at')
        }),
    )
    
    def price_display(self, obj):
        if obj.discount_price:
            return format_html(
                '<span style="text-decoration: line-through; color: #6b7280;">{}</span> <span style="color: #dc2626; font-weight: 700;">{}</span>',
                format_vnd(obj.get_price_vnd()),
                format_vnd(obj.get_discount_price_vnd()),
            )
        return format_vnd(obj.get_price_vnd())
    price_display.short_description = 'Giá (VNĐ)'
    
    def rating_display(self, obj):
        color = 'green' if obj.rating >= 4 else 'orange' if obj.rating >= 3 else 'red'
        # format_html escapes args to SafeString; do not use "{:.1f}" on those placeholders
        rating_txt = f"{float(obj.rating or 0):.1f}"
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}⭐ ({} đánh giá)</span>',
            color, rating_txt, obj.reviews_count,
        )
    rating_display.short_description = 'Đánh giá'


# Review Admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating_stars', 'is_verified_purchase', 'created_at')
    list_filter = ('rating', 'is_verified_purchase', 'created_at')
    search_fields = ('book__title', 'user__username', 'title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    
    def rating_stars(self, obj):
        return '⭐' * obj.rating
    rating_stars.short_description = 'Đánh giá'


# Cart Admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_count', 'total_price', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    
    def item_count(self, obj):
        return obj.get_total_items()
    item_count.short_description = 'Số lượng sản phẩm'
    
    def total_price(self, obj):
        return format_vnd(obj.get_total_price_vnd())
    total_price.short_description = 'Tổng tiền (VNĐ)'


# CartItem Admin
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    change_list_template = 'admin/bookstore_app/cartitem/change_list.html'
    list_display = ('cart', 'book', 'quantity', 'total_price')
    list_filter = ('added_at',)
    search_fields = ('cart__user__username', 'book__title')
    
    def total_price(self, obj):
        return format_vnd(obj.get_total_price_vnd())
    total_price.short_description = 'Tổng tiền (VNĐ)'


# Order Admin
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ('book', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'status_badge', 'payment_status_badge', 'total_amount_vnd', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('order_id', 'user__username', 'email', 'first_name', 'last_name')
    readonly_fields = ('order_id', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Thông tin đơn hàng', {
            'fields': ('order_id', 'user', 'status', 'payment_status', 'created_at', 'updated_at')
        }),
        ('Thông tin khách hàng', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Địa chỉ giao hàng', {
            'fields': ('address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Tài chính', {
            'fields': ('total_amount', 'shipping_cost', 'discount_amount', 'tax_amount')
        }),
        ('Ghi chú', {
            'fields': ('notes',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'confirmed': 'blue',
            'processing': 'purple',
            'shipped': 'navy',
            'delivered': 'green',
            'cancelled': 'red',
            'returned': 'gray',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Trạng thái'
    
    def payment_status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'paid': 'green',
            'failed': 'red',
            'refunded': 'gray',
        }
        color = colors.get(obj.payment_status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_payment_status_display()
        )
    payment_status_badge.short_description = 'Trạng thái thanh toán'

    def total_amount_vnd(self, obj):
        return format_vnd(obj.total_amount)
    total_amount_vnd.short_description = 'Tổng tiền'


# OrderItem Admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'book', 'quantity', 'price', 'total_price')
    list_filter = ('order__created_at',)
    search_fields = ('order__order_id', 'book__title')
    readonly_fields = ('total_price',)
    
    def total_price(self, obj):
        return format_vnd(obj.get_total_price())
    total_price.short_description = 'Tổng tiền'


# Wishlist Admin
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'book_count')
    search_fields = ('user__username', 'user__email')
    
    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = 'Số sách yêu thích'


# Customize admin site
admin.site.site_header = 'Trang quản trị BookStore'
admin.site.site_title = 'Quản trị BookStore'
admin.site.index_title = 'Tổng quan quản trị hệ thống'
