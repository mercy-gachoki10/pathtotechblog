# Login/Signup Implementation - Quick Start Guide

## Running the Application

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Application
```bash
flask run
```

The app will:
- Create database tables automatically
- Create a default admin account if it doesn't exist
- Start the Flask development server on `http://localhost:5000`

---

## Using the Application

### Admin Login
1. Navigate to `http://localhost:5000/login`
2. Enter credentials:
   - **Email:** admin@techblog.com
   - **Password:** admin123
3. You'll be redirected to the admin dashboard

### Regular User Sign Up
1. Navigate to `http://localhost:5000/signup`
2. Fill in the form:
   - First Name
   - Last Name
   - Email
   - Password (minimum 6 characters)
   - Confirm Password
3. Click "Create Account"
4. You'll be redirected to login page
5. Log in with your new credentials
6. You'll be redirected to the user dashboard

### User Experience

#### Navigation Bar Changes

**When Not Logged In:**
- LOGIN
- SIGN UP
- CONTACT US
- BLOG

**When Logged In (Regular User):**
- BLOG
- Welcome, [First Name] (clickable - goes to user dashboard)
- LOGOUT
- CONTACT US

**When Logged In (Admin):**
- BLOG
- Welcome, Admin (clickable - goes to admin dashboard)
- LOGOUT
- CONTACT US

---

## Dashboard Features

### User Dashboard (`/dashboard/user`)
- Welcome message with user's first name
- Profile information display
- Quick access links to blog and contact

### Admin Dashboard (`/dashboard/admin`)
- Welcome message for admin
- Admin profile information
- Admin management links

---

## Features Implemented

✅ **Two Separate User Models**
- Regular User table (first_name, last_name, email, password)
- Admin table (username, email, password)

✅ **User Registration (Sign Up)**
- Form validation (email uniqueness, password matching)
- Password hashing with werkzeug
- Redirect to login after successful signup

✅ **User Authentication (Login)**
- Check both User and Admin tables
- Password verification
- Redirect to appropriate dashboard

✅ **Protected Routes**
- `/dashboard/user` - Only regular users
- `/dashboard/admin` - Only admins
- `/logout` - Only authenticated users

✅ **Dynamic Navigation**
- Shows login/signup for non-authenticated users
- Shows welcome message and logout for authenticated users

✅ **Automatic Admin Creation**
- Admin account created on first app startup
- Credentials: admin@techblog.com / admin123

---

## Security Features

- ✅ Password hashing (werkzeug)
- ✅ CSRF protection (Flask-WTF)
- ✅ Email validation
- ✅ Password confirmation on signup
- ✅ Login required decorator on protected routes
- ✅ Unique email constraint in database

---

## Troubleshooting

### Admin account not created?
- Delete `app.db` file in the root directory
- Run the app again

### Login showing "Invalid email or password"?
- Make sure you're using the correct email/password combination
- Check if user exists in database
- For admin, use: admin@techblog.com / admin123

### Forms not showing validation errors?
- Make sure `SECRET_KEY` is set in config.py (already configured)
- Clear browser cache and try again

---

## Next Steps

1. Create more users by signing up through the app
2. Test admin and regular user workflows
3. Add more features to dashboards
4. Implement password reset functionality
5. Add email verification for new users
