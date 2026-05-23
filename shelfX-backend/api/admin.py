"""
Django Admin configuration for ShelfX.
Bonus: Django gives you a free admin panel at /admin/
"""

from django.contrib import admin
from .models import Author, Category, Book, Bundle, Order, OrderItem


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'created_at']
    search_fields = ['name', 'slug']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'category', 'price', 'stock', 'rating']
    list_filter = ['category', 'language']
    search_fields = ['title', 'isbn']


@admin.register(Bundle)
class BundleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'original_price']
    search_fields = ['name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_email', 'total', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['customer_name', 'customer_email']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'book_title', 'price', 'quantity', 'subtotal']
