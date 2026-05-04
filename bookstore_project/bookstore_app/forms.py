from decimal import Decimal, ROUND_HALF_UP

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, SetPasswordForm
from bookstore_app.models import Review, Order, Book

# User Authentication Forms
class CustomUserCreationForm(UserCreationForm):
    """Form for user registration"""
    email = forms.EmailField(required=True, help_text='Vui lòng nhập email hợp lệ để nhận thông báo đơn hàng.')
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email này đã được đăng ký.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Tên đăng nhập'
        self.fields['username'].help_text = 'Tối đa 150 ký tự. Chỉ gồm chữ cái, số và ký tự @/./+/-/_.'
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ví dụ: nguyenvana'})
        self.fields['email'].label = 'Email'
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'you@example.com'})
        self.fields['first_name'].label = 'Tên'
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Tên của bạn'})
        self.fields['last_name'].label = 'Họ'
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Họ của bạn'})
        self.fields['password1'].label = 'Mật khẩu'
        self.fields['password1'].help_text = 'Mật khẩu nên có ít nhất 8 ký tự và không quá phổ biến.'
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nhập mật khẩu'})
        self.fields['password2'].label = 'Xác nhận mật khẩu'
        self.fields['password2'].help_text = 'Nhập lại mật khẩu để xác nhận.'
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nhập lại mật khẩu'})


class CustomUserChangeForm(UserChangeForm):
    """Form for user profile update"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class CustomPasswordResetForm(PasswordResetForm):
    """Form for password reset"""
    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )


class CustomSetPasswordForm(SetPasswordForm):
    """Form for setting new password"""
    new_password1 = forms.CharField(
        label=("Mật khẩu mới"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=("Xác nhận mật khẩu mới"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )


# Book/Product Forms
class BookForm(forms.ModelForm):
    """
    Form tạo / sửa sách (quản trị web).
    Giá nhập và lưu trực tiếp bằng VNĐ (số nguyên đồng), không quy đổi USD.
    """

    class Meta:
        model = Book
        fields = [
            'title', 'author', 'publisher', 'category', 'description',
            'short_description', 'cover_image', 'price', 'discount_price',
            'quantity', 'pages', 'isbn', 'published_date', 'language',
            'status', 'is_featured', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'publisher': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'short_description': forms.TextInput(attrs={'class': 'form-control'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '0'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'pages': forms.NumberInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'published_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Tiêu đề sách',
            'author': 'Tác giả',
            'publisher': 'Nhà xuất bản',
            'category': 'Thể loại',
            'description': 'Mô tả đầy đủ',
            'short_description': 'Mô tả ngắn',
            'cover_image': 'Ảnh bìa',
            'price': 'Giá bìa (VNĐ)',
            'discount_price': 'Giá khuyến mãi (VNĐ)',
            'quantity': 'Số lượng tồn kho',
            'pages': 'Số trang',
            'isbn': 'Mã ISBN',
            'published_date': 'Ngày xuất bản',
            'language': 'Ngôn ngữ',
            'status': 'Trạng thái kho',
            'is_featured': 'Sách nổi bật',
            'is_active': 'Đang hiển thị trên cửa hàng',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['discount_price'].required = False
        self.fields['price'].help_text = (
            'Nhập số tiền VNĐ (ví dụ 175000). Lưu đúng số đã nhập, không quy đổi.'
        )
        self.fields['discount_price'].help_text = (
            'Để trống nếu không giảm. Nhập VNĐ và phải thấp hơn giá bìa.'
        )
        if self.instance.pk and self.instance.price is not None:
            self.fields['price'].initial = int(
                Decimal(str(self.instance.price)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
            )
        if self.instance.pk and self.instance.discount_price:
            self.fields['discount_price'].initial = int(
                Decimal(str(self.instance.discount_price)).quantize(
                    Decimal('1'), rounding=ROUND_HALF_UP
                )
            )

    def clean_price(self):
        raw = self.cleaned_data.get('price')
        if raw in (None, ''):
            raise forms.ValidationError('Vui lòng nhập giá bìa (VNĐ).')
        try:
            vnd = Decimal(str(raw)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        except Exception:
            raise forms.ValidationError('Giá bìa không hợp lệ.')
        if vnd <= 0:
            raise forms.ValidationError('Giá phải lớn hơn 0.')
        return vnd

    def clean_discount_price(self):
        raw = self.cleaned_data.get('discount_price')
        if raw in (None, ''):
            return None
        try:
            vnd = Decimal(str(raw)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        except Exception:
            raise forms.ValidationError('Giá khuyến mãi không hợp lệ.')
        if vnd < 0:
            raise forms.ValidationError('Giá phải ≥ 0.')
        if vnd == 0:
            return None
        return vnd

    def clean(self):
        cleaned = super().clean()
        price = cleaned.get('price')
        discount = cleaned.get('discount_price')
        if discount is not None and price is not None and discount >= price:
            self.add_error(
                'discount_price',
                'Giá khuyến mãi phải thấp hơn giá bìa.',
            )
        return cleaned


class BookAdminForm(BookForm):
    """
    Form sách trên Django admin — giá VNĐ giống BookForm, thêm slug theo fieldsets admin.
    """

    class Meta(BookForm.Meta):
        fields = [
            'title', 'slug', 'author', 'publisher', 'category', 'description',
            'short_description', 'cover_image', 'price', 'discount_price',
            'quantity', 'pages', 'isbn', 'published_date', 'language',
            'status', 'is_featured', 'is_active',
        ]
        widgets = dict(
            BookForm.Meta.widgets,
            slug=forms.TextInput(attrs={'maxlength': 300}),
        )
        labels = dict(
            BookForm.Meta.labels,
            slug='Slug (URL)',
        )


# Review/Rating Forms
class ReviewForm(forms.ModelForm):
    """Form for creating book reviews"""
    class Meta:
        model = Review
        fields = ['rating', 'title', 'content']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} sao') for i in range(1, 6)]),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tiêu đề đánh giá'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Nội dung đánh giá'}),
        }


# Order Forms
class OrderForm(forms.ModelForm):
    """Form đặt hàng / thanh toán — nhãn tiếng Việt cho người dùng."""
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'address', 'city', 'state', 'postal_code', 'country', 'notes'
        ]
        labels = {
            'first_name': 'Tên',
            'last_name': 'Họ',
            'email': 'Email',
            'phone': 'Số điện thoại',
            'address': 'Địa chỉ nhận hàng',
            'city': 'Tỉnh / Thành phố',
            'state': 'Quận / Huyện',
            'postal_code': 'Mã bưu điện',
            'country': 'Quốc gia',
            'notes': 'Ghi chú thêm (không bắt buộc)',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: Văn A'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ví dụ: Nguyễn'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '09xx xxx xxx'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Số nhà, đường, phường...'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Thành phố Hồ Chí Minh'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quận 1'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '700000'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Việt Nam'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Giao giờ hành chính, gọi trước khi giao...'}),
        }


class BookSearchForm(forms.Form):
    """Form for searching books"""
    SORT_CHOICES = [
        ('latest', 'Mới nhất'),
        ('price_low', 'Giá thấp'),
        ('price_high', 'Giá cao'),
        ('rating', 'Đánh giá cao'),
        ('best_seller', 'Bán chạy'),
    ]
    
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tìm kiếm sách...'})
    )
    category = forms.ModelChoiceField(
        queryset=None,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    author = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tác giả'})
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Giá tối thiểu'})
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Giá tối đa'})
    )
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from bookstore_app.models import Category
        self.fields['category'].queryset = Category.objects.filter(is_active=True)
        self.fields['category'].label = 'Thể loại'
