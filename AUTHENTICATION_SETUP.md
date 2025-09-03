# Authentication Setup Guide

This guide will help you set up Clerk authentication for the AI CV Checker application.

## Overview

The application now uses Clerk for authentication, which provides:
- Social logins (Google, GitHub, etc.)
- Email/password authentication
- User management dashboard
- Secure JWT tokens
- User profile management
- Multi-factor authentication support

## Setup Steps

### 1. Create a Clerk Account

1. Go to [https://clerk.com](https://clerk.com)
2. Sign up for a free account
3. Create a new application
4. Choose your authentication options (email, social providers, etc.)

### 2. Get Your Clerk Keys

1. In your Clerk dashboard, go to **API Keys**
2. Copy the following keys:
   - **Publishable Key** (starts with `pk_test_` or `pk_live_`)
   - **Secret Key** (starts with `sk_test_` or `sk_live_`)

### 3. Configure Environment Variables

Update your `.env.local` file in the project root:

```bash
# Clerk Authentication Keys
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_YOUR_PUBLISHABLE_KEY_HERE
CLERK_SECRET_KEY=sk_test_YOUR_SECRET_KEY_HERE

# Clerk URLs (optional - defaults are fine for most cases)
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/

# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 4. Configure Backend Environment

Update your backend `.env` file:

```bash
# Clerk Webhook Secret (for user sync)
CLERK_WEBHOOK_SECRET=whsec_YOUR_WEBHOOK_SECRET_HERE

# Clerk Secret Key (for API calls)
CLERK_SECRET_KEY=sk_test_YOUR_SECRET_KEY_HERE

# Database
DATABASE_URL=sqlite:///./cv_checker.db
```

### 5. Set Up Clerk Webhooks (Optional but Recommended)

Webhooks keep your local database in sync with Clerk user data:

1. In your Clerk dashboard, go to **Webhooks**
2. Create a new webhook endpoint: `http://localhost:3000/api/webhooks/clerk`
3. Select these events:
   - `user.created`
   - `user.updated`
   - `user.deleted`
4. Copy the webhook secret and add it to your `.env` files

### 6. Install Dependencies

The required packages are already installed:
- `@clerk/nextjs` - Clerk Next.js SDK
- `svix` - Webhook verification

### 7. Database Migration

The database model has been updated to support Clerk users. Run the backend to create new tables:

```bash
cd backend
python main.py
```

## Features Implemented

### Frontend (Next.js)

1. **ClerkProvider** - Wraps the entire app for authentication context
2. **Sign-in/Sign-up pages** - Pre-built Clerk components with custom styling
3. **Header component** - Shows user info and sign-in/out buttons
4. **Protected routes** - Middleware protects authenticated pages
5. **CV Upload Form** - Integrates with Clerk authentication

### Backend (FastAPI)

1. **User model** - Updated to store Clerk user data
2. **Webhook handlers** - Sync users from Clerk events
3. **User management API** - CRUD operations for users
4. **Token verification** - Validates Clerk JWT tokens
5. **Database integration** - Links CV uploads to authenticated users

## API Endpoints

### User Management
- `GET /api/users/me` - Get current user info
- `PUT /api/users/me` - Update user profile
- `GET /api/users/stats` - Get user statistics
- `DELETE /api/users/me` - Deactivate user account

### Webhooks
- `POST /webhooks/clerk` - Handle Clerk user events

## Testing the Setup

1. **Start the backend**:
   ```bash
   cd backend
   python main.py
   ```

2. **Start the frontend**:
   ```bash
   npm run dev
   ```

3. **Test authentication**:
   - Visit `http://localhost:3000`
   - Click "Sign Up" to create an account
   - Try uploading a CV (requires authentication)
   - Check the backend logs for user creation

## Customization Options

### Styling
The Clerk components are styled to match your app's design. You can further customize:
- Colors and themes in the `appearance` prop
- Custom CSS classes
- Component overrides

### Authentication Methods
In your Clerk dashboard, you can enable:
- Social providers (Google, GitHub, Discord, etc.)
- Phone number authentication
- Multi-factor authentication
- Passwordless authentication

### User Management
The Clerk dashboard provides:
- User management interface
- Analytics and insights
- Session management
- Security settings

## Troubleshooting

### Common Issues

1. **Environment variables not loaded**
   - Restart your development servers after updating `.env` files
   - Check that variable names match exactly

2. **Webhook verification fails**
   - Ensure `CLERK_WEBHOOK_SECRET` is correct
   - Check that the webhook URL is accessible

3. **Database errors**
   - Run database migrations
   - Check database file permissions

4. **Token verification fails**
   - Verify `CLERK_SECRET_KEY` is correct
   - Check API endpoint URLs

### Debug Tips

1. Check browser console for frontend errors
2. Monitor backend logs for API issues
3. Use Clerk dashboard to view user events
4. Test webhook endpoints with tools like ngrok for local development

## Security Notes

- Never expose secret keys in client-side code
- Use HTTPS in production
- Regularly rotate API keys
- Monitor authentication logs
- Set up proper CORS policies

## Next Steps

With authentication set up, you can now:
1. Add user-specific CV history
2. Implement usage limits and pricing tiers
3. Add user preferences and settings
4. Create user dashboards
5. Implement team collaboration features

For more advanced Clerk features, see the [official documentation](https://clerk.com/docs).
