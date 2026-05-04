from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bookstore_app.api_views import (
    BookViewSet, CategoryViewSet, AuthorViewSet, ReviewViewSet,
    OrderViewSet, api_stats
)

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='api-book')
router.register(r'categories', CategoryViewSet, basename='api-category')
router.register(r'authors', AuthorViewSet, basename='api-author')
router.register(r'reviews', ReviewViewSet, basename='api-review')
router.register(r'orders', OrderViewSet, basename='api-order')

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', api_stats, name='api-stats'),
]
