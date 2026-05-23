"""
DRF Serializers for ShelfX — produce JSON matching Laravel's response format.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Author, Category, Book, Bundle, Order, OrderItem

User = get_user_model()


# ─── User Serializers ──────────────────────────────────────────────────────────

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'name', 'email', 'phone', 'address',
            'books_read', 'currently_reading', 'reading_goal',
            'loyalty_points', 'total_spent', 'created_at',
        ]


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirmation = serializers.CharField(min_length=6, write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("The email has already been taken.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


# ─── Author Serializers ────────────────────────────────────────────────────────

class AuthorSerializer(serializers.ModelSerializer):
    books_count = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'image', 'created_at', 'updated_at', 'books_count']


class AuthorDetailSerializer(serializers.ModelSerializer):
    """Includes nested books when viewing a single author."""
    books = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'image', 'created_at', 'updated_at', 'books']

    def get_books(self, obj):
        books = obj.books.all()
        return BookSerializer(books, many=True).data


# ─── Category Serializers ──────────────────────────────────────────────────────

class CategorySerializer(serializers.ModelSerializer):
    books_count = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'updated_at', 'books_count']


class CategoryDetailSerializer(serializers.ModelSerializer):
    """Includes nested books when viewing a single category."""
    books = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'updated_at', 'books']

    def get_books(self, obj):
        books = obj.books.all()
        return BookSerializer(books, many=True).data


# ─── Book Serializers ──────────────────────────────────────────────────────────

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True, required=False
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False
    )

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'author_id', 'category', 'category_id',
            'price', 'original_price', 'cover', 'description', 'stock',
            'rating', 'review_count', 'sales_count', 'view_count',
            'isbn', 'pages', 'publisher', 'language',
            'created_at', 'updated_at',
        ]


class BookDetailSerializer(BookSerializer):
    """Includes bundles for book detail view."""
    bundles = serializers.SerializerMethodField()

    class Meta(BookSerializer.Meta):
        fields = BookSerializer.Meta.fields + ['bundles']

    def get_bundles(self, obj):
        bundles = obj.bundles.all()
        return BundleListSerializer(bundles, many=True).data


# ─── Bundle Serializers ────────────────────────────────────────────────────────

class BundleListSerializer(serializers.ModelSerializer):
    """Simple bundle serializer (no nested books) — used in book detail."""
    class Meta:
        model = Bundle
        fields = ['id', 'name', 'description', 'price', 'original_price', 'image', 'created_at', 'updated_at']


class BundleSerializer(serializers.ModelSerializer):
    """Full bundle with nested books + authors."""
    books = serializers.SerializerMethodField()

    class Meta:
        model = Bundle
        fields = ['id', 'name', 'description', 'price', 'original_price', 'image', 'created_at', 'updated_at', 'books']

    def get_books(self, obj):
        books = obj.books.select_related('author').all()
        return BookSerializer(books, many=True).data


class BundleDetailSerializer(serializers.ModelSerializer):
    """Bundle detail with books + categories."""
    books = serializers.SerializerMethodField()

    class Meta:
        model = Bundle
        fields = ['id', 'name', 'description', 'price', 'original_price', 'image', 'created_at', 'updated_at', 'books']

    def get_books(self, obj):
        books = obj.books.select_related('author', 'category').all()
        return BookSerializer(books, many=True).data


# ─── Order Serializers ─────────────────────────────────────────────────────────

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order_id', 'book_id', 'book_title', 'book_cover', 'price', 'quantity', 'subtotal', 'created_at', 'updated_at']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer_name', 'customer_email', 'customer_phone',
            'shipping_address', 'city', 'postal_code', 'country',
            'subtotal', 'shipping_cost', 'discount', 'promo_code', 'total',
            'status', 'created_at', 'updated_at', 'items',
        ]


class CheckoutSerializer(serializers.Serializer):
    """Validates checkout request body."""
    customer_name = serializers.CharField(max_length=255)
    customer_email = serializers.EmailField()
    customer_phone = serializers.CharField(max_length=20, required=False, allow_null=True, allow_blank=True)
    shipping_address = serializers.CharField()
    city = serializers.CharField(max_length=100)
    postal_code = serializers.CharField(max_length=20)
    country = serializers.CharField(max_length=100)
    items = serializers.ListField(child=serializers.DictField(), min_length=1)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    shipping_cost = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    discount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    promo_code = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)
