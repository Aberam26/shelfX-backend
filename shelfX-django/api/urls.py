"""
API URL routing — matches the exact same endpoints as Laravel's api.php routes.
"""

from django.urls import path
from . import views

urlpatterns = [
    # ── Auth (Public) ────────────────────────────────────────────────────────
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),

    # ── Auth (Protected) ─────────────────────────────────────────────────────
    path('profile', views.profile, name='profile'),
    path('logout', views.logout_view, name='logout'),
    path('refresh', views.refresh_token, name='refresh'),

    # ── Authors ──────────────────────────────────────────────────────────────
    path('authors', views.author_list, name='author-list'),
    path('authors/', views.author_list, name='author-list-slash'),
    path('authors/<int:pk>', views.author_detail, name='author-detail'),
    path('authors/<int:pk>/', views.author_detail, name='author-detail-slash'),

    # ── Categories ───────────────────────────────────────────────────────────
    path('categories', views.category_list, name='category-list'),
    path('categories/', views.category_list, name='category-list-slash'),
    path('categories/<int:pk>', views.category_detail, name='category-detail'),
    path('categories/<int:pk>/', views.category_detail, name='category-detail-slash'),

    # ── Books ────────────────────────────────────────────────────────────────
    path('books', views.book_list, name='book-list'),
    path('books/', views.book_list, name='book-list-slash'),
    path('books/<int:pk>', views.book_detail, name='book-detail'),
    path('books/<int:pk>/', views.book_detail, name='book-detail-slash'),

    # ── Bundles ──────────────────────────────────────────────────────────────
    path('bundles', views.bundle_list, name='bundle-list'),
    path('bundles/', views.bundle_list, name='bundle-list-slash'),
    path('bundles/<int:pk>', views.bundle_detail, name='bundle-detail'),
    path('bundles/<int:pk>/', views.bundle_detail, name='bundle-detail-slash'),

    # ── Promo Codes ──────────────────────────────────────────────────────────
    path('validate-promo', views.validate_promo, name='validate-promo'),

    # ── Orders ───────────────────────────────────────────────────────────────
    path('checkout', views.checkout, name='checkout'),
    path('orders/<int:pk>', views.order_detail, name='order-detail'),
    path('user-orders', views.user_orders, name='user-orders'),
]
