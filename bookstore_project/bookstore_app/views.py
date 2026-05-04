from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Sum, Count, Avg, F
from django.db.models.functions import TruncDate
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse, HttpResponseForbidden
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP

from django.utils import timezone

from bookstore_app.models import (
    Book, Category, Author, Review, Cart, CartItem, Order, OrderItem,
    Wishlist, Publisher
)
from bookstore_app.forms import (
    CustomUserCreationForm, CustomUserChangeForm, ReviewForm, OrderForm,
    BookSearchForm, BookForm
)
from bookstore_app.query_params import parse_decimal, parse_positive_int

# Helper function to check if user is admin
def is_admin(user):
    return user.is_staff or user.is_superuser

# Home Page
def home(request):
    """Home page with featured books and categories"""
    featured_books = Book.objects.filter(is_featured=True, is_active=True)[:6]
    categories = Category.objects.filter(is_active=True)
    best_sellers = Book.objects.filter(is_active=True).order_by('-reviews_count')[:6]
    top_rated = Book.objects.filter(is_active=True).order_by('-rating')[:5]
    hero_books = Book.objects.filter(is_active=True).order_by('-reviews_count')[:6]  # Top 6 for hero
    
    context = {
        'featured_books': featured_books,
        'categories': categories,
        'best_sellers': best_sellers,
        'top_rated': top_rated,
        'hero_books': hero_books,
        'filter_category_id': parse_positive_int(request.GET.get('category')),
    }
    return render(request, 'bookstore_app/home.html', context)

@require_GET
def search_suggestions(request):
    """Return live search suggestions for navbar search."""
    query = request.GET.get('q', '').strip()
    if len(query) < 2:
        return JsonResponse({'results': []})

    books = Book.objects.filter(
        is_active=True
    ).filter(
        Q(title__icontains=query) |
        Q(author__name__icontains=query) |
        Q(category__name__icontains=query)
    ).select_related('author')[:6]

    results = []
    for book in books:
        price_vnd = book.get_current_price_vnd()
        formatted_price = f"{price_vnd:,}".replace(',', '.') + " đ"
        results.append({
            'title': book.title,
            'author': book.author.name if book.author else 'Đang cập nhật',
            'price': formatted_price,
            'url': f"/books/{book.slug}/",
        })

    return JsonResponse({'results': results})

# Book Management Views
def book_list(request):
    """List all books with search, filter, and sort"""
    books = Book.objects.filter(is_active=True)
    form = BookSearchForm(request.GET)
    
    # Search
    query = request.GET.get('query', '')
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(isbn__icontains=query)
        )
    
    # Filter by category (ignore invalid ?category=… to avoid ValueError)
    filter_category_id = parse_positive_int(request.GET.get('category'))
    if filter_category_id is not None:
        books = books.filter(category_id=filter_category_id)
    
    # Filter by author
    author = request.GET.get('author', '')
    if author:
        books = books.filter(author__name__icontains=author)
    
    # Filter by price range
    min_price = parse_decimal(request.GET.get('min_price'))
    max_price = parse_decimal(request.GET.get('max_price'))
    if min_price is not None and min_price >= 0:
        books = books.filter(price__gte=min_price)
    if max_price is not None and max_price >= 0:
        books = books.filter(price__lte=max_price)
    
    # Sort
    sort_by = request.GET.get('sort_by', 'latest')
    if sort_by == 'price_low':
        books = books.order_by('price')
    elif sort_by == 'price_high':
        books = books.order_by('-price')
    elif sort_by == 'rating':
        books = books.order_by('-rating')
    elif sort_by == 'best_seller':
        books = books.order_by('-reviews_count')
    else:
        books = books.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(books, 12)
    page = request.GET.get('page')
    books = paginator.get_page(page)
    
    context = {
        'books': books,
        'form': form,
        'query': query,
        'total_books': paginator.count,
        'filter_category_id': filter_category_id,
    }
    return render(request, 'bookstore_app/book_list.html', context)

def book_detail(request, slug):
    """Book detail page with reviews"""
    book = get_object_or_404(Book, slug=slug, is_active=True)
    reviews = book.reviews.all().order_by('-created_at')
    related_books = Book.objects.filter(category=book.category, is_active=True).exclude(id=book.id)[:4]
    
    review_form = ReviewForm()
    user_has_reviewed = False
    user_review = None
    
    if request.user.is_authenticated:
        user_has_reviewed = Review.objects.filter(book=book, user=request.user).exists()
        user_review = Review.objects.filter(book=book, user=request.user).first()
    
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            
            # Update book rating
            avg_rating = book.reviews.aggregate(Avg('rating'))['rating__avg']
            book.rating = avg_rating or 0
            book.reviews_count = book.reviews.count()
            book.save()
            
            messages.success(request, 'Đánh giá của bạn đã được lưu!')
            return redirect('book_detail', slug=slug)
    
    context = {
        'book': book,
        'reviews': reviews,
        'related_books': related_books,
        'review_form': review_form,
        'user_has_reviewed': user_has_reviewed,
        'user_review': user_review,
    }
    return render(request, 'bookstore_app/book_detail.html', context)

# Cart Views
@login_required
def view_cart(request):
    """View shopping cart"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    
    context = {
        'cart': cart,
        'items': items,
        'total_items': cart.get_total_items(),
    }
    return render(request, 'bookstore_app/cart.html', context)

@login_required
@require_POST
def add_to_cart(request, book_id):
    """Add book to cart"""
    book = get_object_or_404(Book, id=book_id, is_active=True)
    
    if book.status == 'out_of_stock' or book.quantity <= 0:
        messages.error(request, f'Sách "{book.title}" hiện đã hết hàng!')
        return redirect('book_detail', slug=book.slug)
    
    quantity = int(request.POST.get('quantity', 1))
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'Đã thêm "{book.title}" vào giỏ hàng!')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'cart_items': cart.get_total_items()})
    
    return redirect('view_cart')

@login_required
@require_POST
def update_cart_item(request, item_id):
    """Update cart item quantity"""
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        item.quantity = quantity
        item.save()
        messages.success(request, 'Giỏ hàng đã được cập nhật!')
    
    return redirect('view_cart')

@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    book_title = item.book.title
    item.delete()
    messages.success(request, f'Đã xóa "{book_title}" khỏi giỏ hàng!')
    
    return redirect('view_cart')

# Order Views
@login_required
def checkout(request):
    """Checkout and create order"""
    cart = get_object_or_404(Cart, user=request.user)
    
    if not cart.items.exists():
        messages.warning(request, 'Giỏ hàng của bạn trống!')
        return redirect('view_cart')
    
    # Check stock for all items
    for item in cart.items.all():
        if item.book.status == 'out_of_stock' or item.book.quantity < item.quantity:
            messages.error(request, f'Sách "{item.book.title}" không đủ số lượng hoặc đã hết hàng!')
            return redirect('view_cart')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = cart.get_total_price()
            order.save()
            
            # Create order items and update stock
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    book=cart_item.book,
                    quantity=cart_item.quantity,
                    price=cart_item.book.get_current_price()
                )
                # Decrease stock
                cart_item.book.quantity -= cart_item.quantity
                if cart_item.book.quantity <= 0:
                    cart_item.book.status = 'out_of_stock'
                cart_item.book.save()
            
            # Clear cart
            cart.items.all().delete()
            
            messages.success(request, 'Đơn hàng của bạn đã được tạo thành công!')
            return redirect('order_detail', order_id=order.id)
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = OrderForm(initial=initial_data)
    
    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'bookstore_app/checkout.html', context)

@login_required
def order_list(request):
    """List user orders"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    orders = paginator.get_page(page)
    
    context = {
        'orders': orders,
    }
    return render(request, 'bookstore_app/order_list.html', context)

@login_required
def order_detail(request, order_id):
    """View order details"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()
    
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'bookstore_app/order_detail.html', context)

# User Authentication Views
def register(request):
    """User registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create cart and wishlist for new user
            Cart.objects.create(user=user)
            Wishlist.objects.create(user=user)
            
            messages.success(request, 'Đăng ký thành công! Vui lòng đăng nhập.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'bookstore_app/register.html', context)

def user_login(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Chào mừng {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không chính xác!')
    
    return render(request, 'bookstore_app/login.html')

def user_logout(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Bạn đã đăng xuất thành công!')
    return redirect('home')

@login_required
def profile(request):
    """User profile"""
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hồ sơ đã được cập nhật!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    # Order statistics
    total_orders = Order.objects.filter(user=request.user).count()
    total_spent = Order.objects.filter(user=request.user, payment_status='paid').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    pending_orders = Order.objects.filter(user=request.user, status__in=['pending', 'confirmed', 'processing']).count()
    delivered_orders = Order.objects.filter(user=request.user, status='delivered').count()
    
    context = {
        'form': form,
        'total_orders': total_orders,
        'total_spent': total_spent,
        'pending_orders': pending_orders,
        'delivered_orders': delivered_orders,
    }
    return render(request, 'bookstore_app/profile.html', context)

@require_POST
def newsletter_subscribe(request):
    """Handle newsletter subscription"""
    email = request.POST.get('email', '').strip()
    if email:
        # Here you could save to a model or send to service
        messages.success(request, 'Đăng ký nhận tin thành công! Cảm ơn bạn đã quan tâm.')
    else:
        messages.error(request, 'Vui lòng nhập địa chỉ email hợp lệ.')
    
    return redirect('home')

# Admin Views
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard with statistics"""
    total_books = Book.objects.count()
    total_users = User.objects.count()
    total_orders = Order.objects.count()
    rev_sum = Order.objects.filter(payment_status='paid').aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0')
    total_revenue = int(
        Decimal(str(rev_sum)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    )

    # Orders by status
    status_mapping = dict(Order.ORDER_STATUS)
    orders_by_status = [
        {
            'status': item['status'],
            'label': status_mapping.get(item['status'], item['status']),
            'count': item['count'],
        }
        for item in Order.objects.values('status').annotate(count=Count('id'))
    ]
    
    # Revenue by date (last 7 days), đơn vị VNĐ (trùng total_amount đơn hàng)
    seven_days_ago = timezone.now() - timedelta(days=7)
    raw_revenue = Order.objects.filter(
        created_at__gte=seven_days_ago,
        payment_status='paid'
    ).annotate(date=TruncDate('created_at')).values('date').annotate(revenue=Sum('total_amount')).order_by('date')
    revenue_by_date = []
    for row in raw_revenue:
        rev = row.get('revenue') or 0
        vnd = int(Decimal(str(rev)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)) if rev else 0
        revenue_by_date.append({'date': row['date'], 'revenue': vnd})
    
    # Top books
    top_books = Book.objects.annotate(sales=Count('orderitem')).order_by('-sales')[:5]
    
    context = {
        'total_books': total_books,
        'total_users': total_users,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'orders_by_status': list(orders_by_status),
        'revenue_by_date': revenue_by_date,
        'top_books': top_books,
    }
    return render(request, 'bookstore_app/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_orders(request):
    """Admin order management"""
    orders = Order.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(orders, 20)
    page = request.GET.get('page')
    orders = paginator.get_page(page)
    
    context = {
        'orders': orders,
    }
    return render(request, 'bookstore_app/admin_orders.html', context)

@login_required
@user_passes_test(is_admin)
@require_POST
def delete_order(request, order_id):
    """Delete order (admin only)"""
    order = get_object_or_404(Order, id=order_id)
    
    # Store order details for message
    order_id_str = order.order_id
    
    # Delete order items first (due to foreign key constraints)
    order.items.all().delete()
    
    # Delete the order
    order.delete()
    
    messages.success(request, f'Đã xóa đơn hàng {order_id_str} thành công!')
    return redirect('admin_orders')

@login_required
@user_passes_test(is_admin)
def manage_books(request):
    """Manage books (CRUD)"""
    books = Book.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(books, 20)
    page = request.GET.get('page')
    books = paginator.get_page(page)
    
    context = {
        'books': books,
    }
    return render(request, 'bookstore_app/manage_books.html', context)

@login_required
@user_passes_test(is_admin)
def create_book(request):
    """Create new book"""
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.created_by = request.user
            base_slug = slugify(book.title) or 'sach'
            slug = base_slug
            n = 1
            while Book.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{n}'
                n += 1
            book.slug = slug
            book.save()
            messages.success(request, 'Sách đã được tạo thành công!')
            return redirect('edit_book', pk=book.id)
    else:
        form = BookForm()
    
    context = {'form': form, 'title': 'Tạo sách mới'}
    return render(request, 'bookstore_app/book_form.html', context)

@login_required
@user_passes_test(is_admin)
def edit_book(request, pk):
    """Edit existing book"""
    book = get_object_or_404(Book, id=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sách đã được cập nhật!')
            if book.is_active:
                return redirect('book_detail', slug=book.slug)
            return redirect('manage_books')
    else:
        form = BookForm(instance=book)
    
    context = {'form': form, 'title': f'Chỉnh sửa: {book.title}', 'book': book}
    return render(request, 'bookstore_app/book_form.html', context)

@login_required
@user_passes_test(is_admin)
@require_POST
def delete_book(request, pk):
    """Delete book"""
    book = get_object_or_404(Book, id=pk)
    book_title = book.title
    book.delete()
    messages.success(request, f'Sách "{book_title}" đã được xóa!')
    return redirect('manage_books')

# Wishlist Views
@login_required
def wishlist(request):
    """View user wishlist"""
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    books = wishlist.books.all()
    
    context = {
        'wishlist': wishlist,
        'books': books,
    }
    return render(request, 'bookstore_app/wishlist.html', context)

@login_required
@require_POST
def add_to_wishlist(request, book_id):
    """Add book to wishlist"""
    book = get_object_or_404(Book, id=book_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.books.add(book)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Đã thêm vào wishlist!'})
    
    messages.success(request, 'Đã thêm vào wishlist!')
    return redirect('book_detail', slug=book.slug)

@login_required
@require_POST
def remove_from_wishlist(request, book_id):
    """Remove book from wishlist"""
    book = get_object_or_404(Book, id=book_id)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    wishlist.books.remove(book)
    
    messages.success(request, 'Đã xóa khỏi wishlist!')
    return redirect('wishlist')

# Custom Password Reset Views
class CustomPasswordResetView(PasswordResetView):
    template_name = 'bookstore_app/password_reset.html'
    email_template_name = 'bookstore_app/password_reset_email.html'
    subject_template_name = 'bookstore_app/password_reset_subject.txt'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'bookstore_app/password_reset_confirm.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'bookstore_app/password_reset_complete.html'

# Context processor for cart
def cart_context(request):
    """Add cart to all templates"""
    cart_items = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_items = cart.get_total_items()
    
    return {'cart_items': cart_items}
