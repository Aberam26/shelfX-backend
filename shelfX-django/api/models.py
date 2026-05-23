"""
ShelfX Models — mapped to existing 'book_haven' MySQL tables.
Uses `managed = False` so Django won't try to alter existing tables.
Uses `db_table` to match Laravel's exact table names.
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


# ─── Custom User Manager ───────────────────────────────────────────────────────

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, password, **extra_fields)


# ─── User Model ────────────────────────────────────────────────────────────────

class User(AbstractBaseUser, PermissionsMixin):
    """Maps to existing 'users' table created by Laravel."""
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    password = models.CharField(max_length=255)
    remember_token = models.CharField(max_length=100, null=True, blank=True)

    # Stats fields (added by add_stats_to_users_table migration)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    books_read = models.IntegerField(default=0)
    currently_reading = models.IntegerField(default=0)
    reading_goal = models.IntegerField(default=50)
    loyalty_points = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Django auth fields (not in Laravel table, but needed for Django admin)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'users'
        managed = False

    def __str__(self):
        return self.name


# ─── Author Model ──────────────────────────────────────────────────────────────

class Author(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    bio = models.TextField()
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'authors'
        managed = False

    def __str__(self):
        return self.name


# ─── Category Model ────────────────────────────────────────────────────────────

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        managed = False

    def __str__(self):
        return self.name


# ─── Book Model ────────────────────────────────────────────────────────────────

class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books', db_column='author_id')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books', db_column='category_id')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    original_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    cover = models.CharField(max_length=255)
    description = models.TextField()
    stock = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    review_count = models.IntegerField(default=0)
    sales_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    isbn = models.CharField(max_length=255, unique=True)
    pages = models.IntegerField()
    publisher = models.CharField(max_length=255)
    language = models.CharField(max_length=255, default='English')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'books'
        managed = False

    def __str__(self):
        return self.title


# ─── Bundle Model ──────────────────────────────────────────────────────────────

class Bundle(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    original_price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Many-to-many with books via 'book_bundle' pivot table
    books = models.ManyToManyField(Book, through='BookBundle', related_name='bundles')

    class Meta:
        db_table = 'bundles'
        managed = False

    def __str__(self):
        return self.name


# ─── BookBundle Pivot Table ─────────────────────────────────────────────────────

class BookBundle(models.Model):
    """Maps to existing 'book_bundle' pivot table."""
    id = models.BigAutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='book_id')
    bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE, db_column='bundle_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'book_bundle'
        managed = False


# ─── Order Model ───────────────────────────────────────────────────────────────

class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    customer_email = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=255, null=True, blank=True)
    shipping_address = models.TextField()
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255, default='USA')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    promo_code = models.CharField(max_length=255, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        managed = False

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


# ─── OrderItem Model ──────────────────────────────────────────────────────────

class OrderItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', db_column='order_id')
    book_id = models.CharField(max_length=255)
    book_title = models.CharField(max_length=255)
    book_cover = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_items'
        managed = False

    def __str__(self):
        return f"{self.book_title} x{self.quantity}"
