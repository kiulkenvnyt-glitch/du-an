from rest_framework import viewsets, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from bookstore_app.models import Book, Category, Author, Review, Order
from bookstore_app.serializers import (
    BookSerializer, CategorySerializer, AuthorSerializer,
    ReviewSerializer, OrderSerializer
)

class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """API for books"""
    queryset = Book.objects.filter(is_active=True)
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author', 'status']
    search_fields = ['title', 'description', 'isbn']
    ordering_fields = ['price', 'rating', 'created_at']

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API for categories"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer

class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    """API for authors"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    """API for reviews"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['book']

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """API for user orders"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def api_stats(request):
    """Get general statistics"""
    stats = {
        'total_books': Book.objects.count(),
        'total_categories': Category.objects.count(),
        'total_authors': Author.objects.count(),
        'total_reviews': Review.objects.count(),
    }
    return Response(stats)
