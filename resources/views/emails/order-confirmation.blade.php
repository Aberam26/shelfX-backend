<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background-color: #8B4513;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px 5px 0 0;
        }
        .content {
            background-color: #f9f9f9;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 0 0 5px 5px;
        }
        .order-info {
            background-color: white;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }
        .order-items {
            margin: 20px 0;
        }
        .order-item {
            display: flex;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }
        .order-item:last-child {
            border-bottom: none;
        }
        .item-details {
            flex: 1;
        }
        .item-price {
            text-align: right;
            font-weight: bold;
        }
        .summary {
            background-color: white;
            padding: 15px;
            margin-top: 20px;
            border-radius: 5px;
        }
        .summary-row {
            display: flex;
            justify-content: space-between;
            padding: 5px 0;
        }
        .total {
            font-size: 1.2em;
            font-weight: bold;
            border-top: 2px solid #333;
            padding-top: 10px;
            margin-top: 10px;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: #666;
            font-size: 0.9em;
        }
        .button {
            display: inline-block;
            background-color: #8B4513;
            color: white;
            padding: 12px 30px;
            text-decoration: none;
            border-radius: 5px;
            margin: 15px 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛍️ shelfX</h1>
        <p>Thank You for Your Order!</p>
    </div>
    
    <div class="content">
        <p>Hello {{ $order->customer_name }},</p>
        
        <p>Thank you for your order! We're excited to get your books to you.</p>
        
        <div class="order-info">
            <h2>Order Details</h2>
            <p><strong>Order Number:</strong> #{{ $order->id }}</p>
            <p><strong>Order Date:</strong> {{ $order->created_at->format('F d, Y') }}</p>
            <p><strong>Status:</strong> <span style="text-transform: capitalize;">{{ $order->status }}</span></p>
        </div>

        <div class="order-info">
            <h2>Shipping Address</h2>
            <p>
                {{ $order->customer_name }}<br>
                {{ $order->shipping_address }}<br>
                {{ $order->city }}, {{ $order->postal_code }}<br>
                {{ $order->country }}
            </p>
        </div>

        <div class="order-items">
            <h2>Order Items</h2>
            @foreach($order->items as $item)
            <div class="order-item">
                <div class="item-details">
                    <strong>{{ $item->book_title }}</strong><br>
                    <span style="color: #666;">Quantity: {{ $item->quantity }} × ${{ number_format($item->price, 2) }}</span>
                </div>
                <div class="item-price">
                    ${{ number_format($item->subtotal, 2) }}
                </div>
            </div>
            @endforeach
        </div>

        <div class="summary">
            <h2>Order Summary</h2>
            <div class="summary-row">
                <span>Subtotal:</span>
                <span>${{ number_format($order->subtotal, 2) }}</span>
            </div>
            <div class="summary-row">
                <span>Shipping:</span>
                <span>{{ $order->shipping_cost == 0 ? 'Free' : '$' . number_format($order->shipping_cost, 2) }}</span>
            </div>
            @if($order->discount > 0)
            <div class="summary-row" style="color: green;">
                <span>Discount @if($order->promo_code)({{ $order->promo_code }})@endif:</span>
                <span>-${{ number_format($order->discount, 2) }}</span>
            </div>
            @endif
            <div class="summary-row total">
                <span>Total:</span>
                <span>${{ number_format($order->total, 2) }}</span>
            </div>
        </div>

        <div style="text-align: center;">
            <p>You can track your order status at any time:</p>
            <a href="{{ config('app.frontend_url') }}/orders/{{ $order->id }}" class="button">View Order Details</a>
        </div>

        <p>If you have any questions about your order, please contact us.</p>
        
        <p>Happy reading!<br>The shelfX Team</p>
    </div>
    
    <div class="footer">
        <p>This is an automated message. Please do not reply to this email.</p>
        <p>&copy; {{ date('Y') }} shelfX. All rights reserved.</p>
    </div>
</body>
</html>
