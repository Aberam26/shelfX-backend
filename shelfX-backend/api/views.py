"""
ShelfX API Views — replaces all Laravel Controllers.
Produces identical JSON responses so the React frontend works without changes.
"""

import logging
from django.db import transaction
from django.db.models import Count, F, Q
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model

from .models import Author, Category, Book, Bundle, Order, OrderItem
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    AuthorSerializer, AuthorDetailSerializer,
    CategorySerializer, CategoryDetailSerializer,
    BookSerializer, BookDetailSerializer,
    BundleSerializer, BundleDetailSerializer,
    OrderSerializer, OrderItemSerializer, CheckoutSerializer,
)

User = get_user_model()
logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
#  AUTH VIEWS
# ═══════════════════════════════════════════════════════════════════════════════

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user — POST /api/register"""
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    data = serializer.validated_data
    user = User.objects.create_user(
        email=data['email'],
        name=data['name'],
        password=data['password'],
    )

    refresh = RefreshToken.for_user(user)

    return Response({
        'success': True,
        'message': 'User registered successfully',
        'user': UserSerializer(user).data,
        'token': str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login user — POST /api/login"""
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    user = authenticate(request, email=email, password=password)

    if user is None:
        return Response({
            'success': False,
            'message': 'Invalid email or password'
        }, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)

    return Response({
        'success': True,
        'message': 'Login successful',
        'user': UserSerializer(user).data,
        'token': str(refresh.access_token),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Get authenticated user profile — GET /api/profile"""
    return Response({
        'success': True,
        'user': UserSerializer(request.user).data,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout user — POST /api/logout"""
    try:
        # Blacklist the refresh token if provided
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
    except Exception:
        pass

    return Response({
        'success': True,
        'message': 'Successfully logged out'
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_token(request):
    """Refresh JWT token — POST /api/refresh"""
    try:
        refresh = request.data.get('refresh')
        if not refresh:
            return Response({
                'success': False,
                'message': 'Refresh token required'
            }, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh)
        return Response({
            'success': True,
            'token': str(token.access_token),
        })
    except Exception:
        return Response({
            'success': False,
            'message': 'Token refresh failed'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ═══════════════════════════════════════════════════════════════════════════════
#  AUTHOR VIEWS
# ═══════════════════════════════════════════════════════════════════════════════

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def author_list(request):
    """GET /api/authors — list all authors with book counts
       POST /api/authors — create a new author"""
    if request.method == 'GET':
        authors = Author.objects.annotate(books_count=Count('books')).all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def author_detail(request, pk):
    """GET/PUT/DELETE /api/authors/{id}"""
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        return Response({'message': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AuthorDetailSerializer(author)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AuthorSerializer(author, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    elif request.method == 'DELETE':
        author.delete()
        return Response({'message': 'Author deleted successfully'})


# ═══════════════════════════════════════════════════════════════════════════════
#  CATEGORY VIEWS
# ═══════════════════════════════════════════════════════════════════════════════

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def category_list(request):
    """GET /api/categories — list all categories with book counts
       POST /api/categories — create a new category"""
    if request.method == 'GET':
        categories = Category.objects.annotate(books_count=Count('books')).all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def category_detail(request, pk):
    """GET/PUT/DELETE /api/categories/{id}"""
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({'message': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategoryDetailSerializer(category)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    elif request.method == 'DELETE':
        category.delete()
        return Response({'message': 'Category deleted successfully'})


# ═══════════════════════════════════════════════════════════════════════════════
#  BOOK VIEWS
# ═══════════════════════════════════════════════════════════════════════════════

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def book_list(request):
    """GET /api/books — list books with filters/search/sort
       POST /api/books — create a new book"""
    if request.method == 'GET':
        queryset = Book.objects.select_related('author', 'category').all()

        # Filter by category
        category_id = request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Filter by author
        author_id = request.query_params.get('author_id')
        if author_id:
            queryset = queryset.filter(author_id=author_id)

        # Search
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        # Sort
        sort_by = request.query_params.get('sort_by', 'created_at')
        sort_order = request.query_params.get('sort_order', 'desc')
        if sort_order == 'desc':
            sort_by = f'-{sort_by}'
        queryset = queryset.order_by(sort_by)

        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            book = serializer.save()
            # Reload with relations
            book = Book.objects.select_related('author', 'category').get(pk=book.pk)
            return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def book_detail(request, pk):
    """GET/PUT/DELETE /api/books/{id}"""
    try:
        book = Book.objects.select_related('author', 'category').get(pk=pk)
    except Book.DoesNotExist:
        return Response({'message': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Increment view count (same as Laravel)
        Book.objects.filter(pk=pk).update(view_count=F('view_count') + 1)
        book.refresh_from_db()
        serializer = BookDetailSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            book = serializer.save()
            book = Book.objects.select_related('author', 'category').get(pk=book.pk)
            return Response(BookSerializer(book).data)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    elif request.method == 'DELETE':
        book.delete()
        return Response({'message': 'Book deleted successfully'})


# ═══════════════════════════════════════════════════════════════════════════════
#  BUNDLE VIEWS
# ═══════════════════════════════════════════════════════════════════════════════

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def bundle_list(request):
    """GET /api/bundles — list bundles with books and authors
       POST /api/bundles — create a new bundle"""
    if request.method == 'GET':
        bundles = Bundle.objects.prefetch_related('books__author').all()
        serializer = BundleSerializer(bundles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        book_ids = data.pop('book_ids', []) if isinstance(data, dict) else []

        serializer = BundleSerializer(data=data)
        if serializer.is_valid():
            bundle = Bundle(
                name=data.get('name'),
                description=data.get('description'),
                price=data.get('price'),
                original_price=data.get('original_price'),
                image=data.get('image'),
            )
            bundle.save()

            # Attach books via pivot table
            from .models import BookBundle
            for book_id in book_ids:
                BookBundle.objects.create(book_id=book_id, bundle=bundle)

            bundle = Bundle.objects.prefetch_related('books').get(pk=bundle.pk)
            return Response(BundleSerializer(bundle).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def bundle_detail(request, pk):
    """GET/PUT/DELETE /api/bundles/{id}"""
    try:
        bundle = Bundle.objects.prefetch_related('books__author', 'books__category').get(pk=pk)
    except Bundle.DoesNotExist:
        return Response({'message': 'Bundle not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BundleDetailSerializer(bundle)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data
        book_ids = data.pop('book_ids', None) if isinstance(data, dict) else None

        for field in ['name', 'description', 'price', 'original_price', 'image']:
            if field in data:
                setattr(bundle, field, data[field])
        bundle.save()

        if book_ids is not None:
            from .models import BookBundle
            BookBundle.objects.filter(bundle=bundle).delete()
            for book_id in book_ids:
                BookBundle.objects.create(book_id=book_id, bundle=bundle)

        bundle = Bundle.objects.prefetch_related('books').get(pk=bundle.pk)
        return Response(BundleSerializer(bundle).data)

    elif request.method == 'DELETE':
        bundle.delete()
        return Response({'message': 'Bundle deleted successfully'})


# ═══════════════════════════════════════════════════════════════════════════════
#  ORDER VIEWS
# ═══════════════════════════════════════════════════════════════════════════════

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_orders(request):
    """GET /api/user-orders — get orders for authenticated user"""
    user = request.user
    orders = Order.objects.filter(customer_email=user.email).prefetch_related('items').order_by('-created_at')

    return Response({
        'success': True,
        'orders': OrderSerializer(orders, many=True).data,
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def checkout(request):
    """POST /api/checkout — place an order"""
    serializer = CheckoutSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    data = serializer.validated_data

    try:
        with transaction.atomic():
            # Create the order
            order = Order.objects.create(
                customer_name=data['customer_name'],
                customer_email=data['customer_email'],
                customer_phone=data.get('customer_phone'),
                shipping_address=data['shipping_address'],
                city=data['city'],
                postal_code=data['postal_code'],
                country=data['country'],
                subtotal=data['subtotal'],
                shipping_cost=data['shipping_cost'],
                discount=data['discount'],
                promo_code=data.get('promo_code'),
                total=data['total'],
                status='pending',
            )

            # Create order items
            for item in data['items']:
                OrderItem.objects.create(
                    order=order,
                    book_id=item.get('book_id', ''),
                    book_title=item.get('book_title', ''),
                    book_cover=item.get('book_cover', ''),
                    price=item.get('price', 0),
                    quantity=item.get('quantity', 1),
                    subtotal=float(item.get('price', 0)) * int(item.get('quantity', 1)),
                )

        # Send order confirmation email
        try:
            order_with_items = Order.objects.prefetch_related('items').get(pk=order.pk)
            html_message = render_to_string('emails/order_confirmation.html', {
                'order': order_with_items,
                'frontend_url': settings.FRONTEND_URL,
            })
            send_mail(
                subject=f'Order Confirmation - Order #{order.id}',
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.customer_email],
                html_message=html_message,
                fail_silently=True,
            )
        except Exception as e:
            logger.error(f'Failed to send order confirmation email: {e}')

        order_with_items = Order.objects.prefetch_related('items').get(pk=order.pk)
        return Response({
            'success': True,
            'message': 'Order placed successfully!',
            'order_id': order.id,
            'order': OrderSerializer(order_with_items).data,
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            'success': False,
            'message': 'Failed to place order. Please try again.',
            'error': str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def order_detail(request, pk):
    """GET /api/orders/{id} — get order details"""
    try:
        order = Order.objects.prefetch_related('items').get(pk=pk)
    except Order.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Order not found',
        }, status=status.HTTP_404_NOT_FOUND)

    return Response({
        'success': True,
        'order': OrderSerializer(order).data,
    })


# ═══════════════════════════════════════════════════════════════════════════════
#  PROMO CODE VIEW
# ═══════════════════════════════════════════════════════════════════════════════

# Same promo codes as Laravel
PROMO_CODES = {
    'SAVE10': 10,
    'BOOK5': 5,
    'WELCOME20': 20,
    'FREESHIP': 100,
    'SUMMER15': 15,
    'EXTRA25': 25,
    'READMORE': 12,
}


@api_view(['POST'])
@permission_classes([AllowAny])
def validate_promo(request):
    """POST /api/validate-promo — validate a promo code"""
    code = request.data.get('code', '')
    if not code:
        # Also check JSON body
        code = request.data.get('code', '')

    code = code.upper() if code else ''

    if code in PROMO_CODES:
        return Response({
            'valid': True,
            'discount': PROMO_CODES[code],
        })

    return Response({
        'valid': False,
        'discount': 0,
    })
