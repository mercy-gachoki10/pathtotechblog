# Login/Signup Flow Diagrams & Workflow

## 1. Sign Up Flow

```
User visits /signup
    ↓
Form displayed (First Name, Last Name, Email, Password, Confirm Password)
    ↓
User fills and submits form
    ↓
Form validation:
├─ Check email format ✓
├─ Check password length (min 6) ✓
├─ Check passwords match ✓
└─ Check email not already registered ✓
    ↓
If validation passes:
├─ Create User object
├─ Hash password with werkzeug
├─ Save to database
└─ Flash success message
    ↓
Redirect to /login
    ↓
User logs in with credentials
    ↓
Redirect to user dashboard
```

---

## 2. Login Flow

```
User visits /login
    ↓
Form displayed (Email, Password)
    ↓
User enters credentials and submits
    ↓
Form validation:
├─ Check email format ✓
└─ Check password not empty ✓
    ↓
System checks credentials:
├─ Query User table by email
│  ├─ If found: Check password hash
│  │  ├─ Match: Login user → Redirect to /dashboard/user
│  │  └─ No match: Continue
│  └─ Not found: Continue
│
├─ Query Admin table by email
│  ├─ If found: Check password hash
│  │  ├─ Match: Login user → Redirect to /dashboard/admin
│  │  └─ No match: Show error
│  └─ Not found: Show error
│
└─ Show error: "Invalid email or password"
```

---

## 3. Navigation Bar Changes

### Unauthenticated User
```
┌─────────────────────────────────────────────┐
│  🔗 TechBlog    BLOG  LOGIN  SIGNUP  CONTACT │
└─────────────────────────────────────────────┘
```

### Regular User (Logged In)
```
┌─────────────────────────────────────────────────────────────┐
│  🔗 TechBlog    BLOG  Welcome, John →   LOGOUT  CONTACT     │
│                      (clicks → /dashboard/user)              │
└─────────────────────────────────────────────────────────────┘
```

### Admin User (Logged In)
```
┌─────────────────────────────────────────────────────────────┐
│  🔗 TechBlog    BLOG  Welcome, Admin →   LOGOUT  CONTACT    │
│                       (clicks → /dashboard/admin)            │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Route Protection & Access Control

```
┌─────────────────────────────────────────────────────────────┐
│                      PROTECTED ROUTES                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  /dashboard/user                                              │
│  ├─ Only regular users (User model)                          │
│  ├─ Admin access → Redirects to /dashboard/admin             │
│  └─ Not authenticated → Redirects to /login                  │
│                                                               │
│  /dashboard/admin                                             │
│  ├─ Only admins (Admin model)                                │
│  ├─ Regular user access → Error + Redirect to /              │
│  └─ Not authenticated → Redirects to /login                  │
│                                                               │
│  /logout                                                      │
│  ├─ All authenticated users                                  │
│  └─ Not authenticated → Redirects to /login                  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. User Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│ Welcome, John! 👋                                             │
│ You are now logged in to your account                         │
├──────────────────┬──────────────────────────────────────────┤
│                  │                                            │
│  Your Profile    │      Quick Links                           │
│                  │                                            │
│  Name: John Doe  │  • Read Blog Posts                        │
│  Email: j@t.com  │  • Contact Us                             │
│  Member Since:   │  • Back to Home                           │
│  Nov 24, 2024    │                                            │
│                  │                                            │
└──────────────────┴──────────────────────────────────────────┘
```

---

## 6. Admin Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│ Welcome, Admin! 👨‍💼                                             │
│ Administrator Dashboard                                       │
├──────────────────┬──────────────────────────────────────────┤
│                  │                                            │
│  Admin Profile   │      Admin Functions                       │
│                  │                                            │
│  Username: admin │  • Manage Blog Posts                      │
│  Email:          │  • View Messages                          │
│  admin@          │  • Back to Home                           │
│  techblog.com    │                                            │
│  Member Since:   │                                            │
│  Nov 24, 2024    │                                            │
│  Role: Admin     │                                            │
│                  │                                            │
└──────────────────┴──────────────────────────────────────────┘
```

---

## 7. Database Tables

### User Table
```
┌──────┬────────────┬───────────┬────────────┬──────────┬────────────┬────────────┐
│ ID   │ First Name │ Last Name │ Email      │ Password │ Created At │ Updated At │
├──────┼────────────┼───────────┼────────────┼──────────┼────────────┼────────────┤
│ 1    │ John       │ Doe       │ john@t.com │ hash...  │ 2024-11-24 │ 2024-11-24 │
│ 2    │ Jane       │ Smith     │ jane@t.com │ hash...  │ 2024-11-24 │ 2024-11-24 │
└──────┴────────────┴───────────┴────────────┴──────────┴────────────┴────────────┘
```

### Admin Table
```
┌──────┬──────────┬──────────────────────┬──────────┬────────────┬────────────┐
│ ID   │ Username │ Email                │ Password │ Created At │ Updated At │
├──────┼──────────┼──────────────────────┼──────────┼────────────┼────────────┤
│ 1    │ admin    │ admin@techblog.com   │ hash...  │ 2024-11-24 │ 2024-11-24 │
└──────┴──────────┴──────────────────────┴──────────┴────────────┴────────────┘
```

---

## 8. Form Validation Chain

### Sign Up Form
```
Input → Check Required Fields → Check Email Format → Check Email Unique
  ↓         ✓                        ✓                    ✓
Check Password Length (min 6) → Check Passwords Match → Validation Complete
  ✓                              ✓
```

### Login Form
```
Input → Check Required Fields → Check Email Format → Validation Complete
  ↓         ✓                        ✓
Check Credentials in Database → Generate Session → Redirect to Dashboard
  ✓
```

---

## 9. Password Security

```
User enters password "MyPassword123"
         ↓
Check length (min 6 chars) ✓
         ↓
Hash with werkzeug:
    generate_password_hash("MyPassword123")
    ↓
    "pbkdf2:sha256$.............................."
         ↓
Store in database
         ↓

During Login:
         ↓
User enters "MyPassword123"
         ↓
Retrieve stored hash from database
         ↓
Compare: check_password_hash(stored_hash, "MyPassword123")
         ↓
Return True/False
```

---

## 10. Session Management

```
User Login Successful
         ↓
Flask-Login creates session
         ↓
current_user becomes accessible
         ↓
Protected routes check @login_required decorator
         ↓
User makes requests with valid session
         ↓
User logs out
         ↓
Flask-Login destroys session
         ↓
current_user = None
         ↓
Redirect to homepage
```

---

## 11. Error Handling & Flash Messages

```
Form Submission
         ↓
Form Validation
├─ Success → Process request → flash("Success message") → Redirect
└─ Error → flash("Error message", "error") → Re-render form with errors
         ↓
User sees:
- Error messages below each field
- Alert box at top of form
```

---

## 12. Testing Credentials

```
ADMIN USER
├─ Email: admin@techblog.com
├─ Password: admin123
└─ Expected Redirect: /dashboard/admin

REGULAR USER (Create via Sign Up)
├─ Email: example@example.com
├─ Password: MyPassword123 (min 6 chars)
└─ Expected Redirect: /dashboard/user
```

---

## 13. Current User Detection

```
In Template:
{{ current_user.is_authenticated }}  → True/False
{{ current_user.__class__.__name__ }}  → "User" or "Admin"

In Python:
isinstance(current_user, Admin)  → True/False
isinstance(current_user, User)   → True/False

Usage:
{% if current_user.is_authenticated %}
    {% if current_user.__class__.__name__ == 'Admin' %}
        Admin specific content
    {% else %}
        User specific content
    {% endif %}
{% endif %}
```

---

## 14. Routes Summary

```
Public Routes:
├─ GET  / ........................... Homepage
├─ GET  /blog ...................... Blog page
├─ GET/POST  /contact .............. Contact page
├─ GET/POST  /login ................ Login page
└─ GET/POST  /signup ............... Sign up page

Protected Routes:
├─ GET  /dashboard/user ........... User dashboard (Users only)
├─ GET  /dashboard/admin .......... Admin dashboard (Admin only)
└─ GET  /logout ................... Logout (All authenticated)
```

---

## 15. Implementation Checklist

- [x] Create User model with first_name, last_name, email, password
- [x] Create Admin model with username, email, password
- [x] Add password hashing with werkzeug
- [x] Create SignUpForm with validation
- [x] Create LoginForm with validation
- [x] Implement /signup route with logic
- [x] Implement /login route with logic
- [x] Implement /logout route
- [x] Create /dashboard/user route (protected)
- [x] Create /dashboard/admin route (protected)
- [x] Update base.html navigation
- [x] Create user dashboard template
- [x] Create admin dashboard template
- [x] Auto-create admin on startup
- [x] Add form error display
- [x] Add flash message display
- [x] Add CSRF protection
- [x] Add role-based access control
