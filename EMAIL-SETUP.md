# Email Configuration for Order Notifications

Your application is now configured to send email notifications when orders are placed!

## Current Setup (Development/Testing)

By default, emails are saved to the Laravel log file instead of being sent. This is perfect for testing!

**To view sent emails:**
- Open: `storage/logs/laravel.log`
- Look for email content after placing an order

## Email Features

✅ **Automatic order confirmation emails** sent when orders are placed
✅ **Professional HTML email template** with your branding
✅ **Order details included:**
   - Order number and date
   - Customer information
   - Shipping address
   - All order items with prices
   - Order summary with totals
   - Promo code discounts (if applied)
   - Link to view order details

## Production Email Setup

When you're ready to send real emails in production, update your `.env` file:

### Option 1: Using Gmail (Free for testing)

```env
MAIL_MAILER=smtp
MAIL_HOST=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_ENCRYPTION=tls
MAIL_FROM_ADDRESS=your-email@gmail.com
MAIL_FROM_NAME="shelfX"
```

**Note:** For Gmail, you need to:
1. Enable 2-factor authentication
2. Generate an "App Password" in your Google Account settings
3. Use the app password instead of your regular password

### Option 2: Using Mailtrap (Free for testing)

```env
MAIL_MAILER=smtp
MAIL_HOST=sandbox.smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=your-mailtrap-username
MAIL_PASSWORD=your-mailtrap-password
MAIL_ENCRYPTION=tls
MAIL_FROM_ADDRESS=noreply@shelfx.com
MAIL_FROM_NAME="shelfX"
```

Sign up at [mailtrap.io](https://mailtrap.io) to get credentials.

### Option 3: Using SendGrid, Mailgun, or other services

Follow their documentation for SMTP credentials.

## Testing Email Locally

1. Place an order through your checkout page
2. Check `storage/logs/laravel.log` for the email content
3. You should see the full HTML email with all order details

## Environment Variables

Add these to your `.env` file:

```env
MAIL_FROM_ADDRESS=noreply@shelfx.com
MAIL_FROM_NAME="shelfX Bookstore"
FRONTEND_URL=http://localhost:5173
```

## Email Template Customization

To customize the email template:
- Edit: `resources/views/emails/order-confirmation.blade.php`
- Change colors, text, or layout as needed
- Restart your backend server after making changes

## Troubleshooting

**Emails not being sent?**
1. Check `storage/logs/laravel.log` for errors
2. Verify your `.env` mail settings
3. Make sure your email provider allows SMTP connections
4. For Gmail, ensure you're using an app password, not your regular password

**Email link not working?**
1. Check that `FRONTEND_URL` in `.env` matches your frontend URL
2. Default is `http://localhost:5173`

## Need Help?

If you need to set up a specific email service, let me know and I can provide detailed instructions!
