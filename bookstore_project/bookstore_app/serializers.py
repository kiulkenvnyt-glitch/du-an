from rest_framework import serializers
from bookstore_app.models import Book, Category, Author, Review, Order

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'nationality']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    discount_percentage = serializers.SerializerMethodField()
    current_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'slug', 'author', 'category', 'description',
            'price', 'discount_price', 'quantity', 'status', 'rating',
            'reviews_count', 'discount_percentage', 'current_price'
        ]
    
    def get_discount_percentage(self, obj):
        return obj.get_discount_percentage()
    
    def get_current_price(self, obj):
        return obj.get_current_price()

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'book_title', 'user', 'rating', 'title', 'content', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_id', 'user', 'status', 'payment_status',
            'total_amount', 'created_at'
        ]
        read_only_fields = ['order_id', 'created_at']
