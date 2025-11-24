# Step-by-Step Testing Guide

## Prerequisites
- Python 3.7+
- All packages from `requirements.txt` installed
- Terminal/Command Prompt

---

## Test 1: Initial Setup & Admin Account Creation ✅

### Steps:
1. **Delete existing database** (if any):
   ```bash
   # Make sure you're in the project root directory
   # Delete app.db if it exists
   rm app.db
   ```

2. **Run the Flask application**:
   ```bash
   python app.py
   # OR
   flask run
   ```

3. **Expected Output**:
   ```
   Admin account created successfully!
    * Running on http://127.0.0.1:5000
   ```

4. **Verify**: Open browser and go to `http://localhost:5000`
   - Should see homepage
   - Navigation shows: BLOG, LOGIN, SIGN UP, CONTACT US

✅ **Test Passed**: Admin account automatically created

---

## Test 2: Admin Login ✅

### Steps:
1. **Navigate to login page**: `http://localhost:5000/login`

2. **Enter credentials**:
   - Email: `admin@techblog.com`
   - Password: `admin123`

3. **Click "Login"**

### Expected Results:
- ✅ Flash message: "Welcome admin!"
- ✅ Redirected to: `http://localhost:5000/dashboard/admin`
- ✅ See: "Welcome, Admin! 👨‍💼" heading
- ✅ Admin profile shows: username, email, member since date
- ✅ Navigation bar updated: "Welcome, Admin" + "LOGOUT" visible

---

## Test 3: Admin Logout ✅

### Steps:
1. **From admin dashboard, click "LOGOUT"** in navigation

### Expected Results:
- ✅ Flash message: "You have been logged out successfully."
- ✅ Redirected to: `http://localhost:5000/`
- ✅ Navigation reverted: Shows LOGIN and SIGN UP again

---

## Test 4: User Sign Up ✅

### Steps:
1. **Navigate to sign up page**: `http://localhost:5000/signup`

2. **Fill in the form**:
   - First Name: `John`
   - Last Name: `Doe`
   - Email: `john@example.com`
   - Password: `password123`
   - Confirm Password: `password123`

3. **Click "Create Account"**

### Expected Results:
- ✅ Flash message: "Account created successfully! Please log in."
- ✅ Redirected to: `http://localhost:5000/login`

---

## Test 5: User Login ✅

### Steps:
1. **At login page, enter new user credentials**:
   - Email: `john@example.com`
   - Password: `password123`

2. **Click "Login"**

### Expected Results:
- ✅ Flash message: "Welcome back, John!"
- ✅ Redirected to: `http://localhost:5000/dashboard/user`
- ✅ See: "Welcome, John! 👋" heading
- ✅ User profile shows: Full name, email, member since date
- ✅ Navigation bar updated: "Welcome, John" + "LOGOUT" visible

---

## Test 6: User Dashboard Access ✅

### Steps:
1. **From user dashboard, verify profile information displays**
2. **Click "Read Blog Posts"** - Should navigate to blog
3. **Click "Contact Us"** - Should navigate to contact
4. **Click "Back to Home"** - Should navigate to homepage
5. **Click "Welcome, John"** - Should stay on user dashboard

### Expected Results:
- ✅ All links work correctly
- ✅ Still logged in after clicking links (except logout)

---

## Test 7: User Logout ✅

### Steps:
1. **From user dashboard, click "LOGOUT"**

### Expected Results:
- ✅ Flash message: "You have been logged out successfully."
- ✅ Redirected to: `http://localhost:5000/`
- ✅ Navigation reverted: Shows LOGIN and SIGN UP again

---

## Test 8: Invalid Login Credentials ❌

### Steps:
1. **Navigate to login page**: `http://localhost:5000/login`
2. **Enter invalid credentials**:
   - Email: `wrong@example.com`
   - Password: `wrongpassword`
3. **Click "Login"**

### Expected Results:
- ✅ Flash message: "Invalid email or password."
- ✅ Stay on login page
- ✅ Form is cleared

---

## Test 9: Duplicate Email Sign Up ❌

### Steps:
1. **Navigate to sign up page**: `http://localhost:5000/signup`
2. **Try to sign up with email already used**:
   - Email: `john@example.com` (already used)
   - Other fields: Any valid data
3. **Click "Create Account"**

### Expected Results:
- ✅ Error message below email field: "Email already registered. Please use a different email."
- ✅ Stay on signup page
- ✅ Form data preserved (except password fields)

---

## Test 10: Password Mismatch on Sign Up ❌

### Steps:
1. **Navigate to sign up page**: `http://localhost:5000/signup`
2. **Enter mismatched passwords**:
   - Password: `password123`
   - Confirm Password: `password456`
3. **Click "Create Account"**

### Expected Results:
- ✅ Error message below confirm password: "Passwords must match"
- ✅ Stay on signup page

---

## Test 11: Short Password ❌

### Steps:
1. **Navigate to sign up page**: `http://localhost:5000/signup`
2. **Enter password less than 6 characters**:
   - Password: `pass`
   - Confirm Password: `pass`
3. **Click "Create Account"**

### Expected Results:
- ✅ Error message: "Password must be at least 6 characters long"
- ✅ Stay on signup page

---

## Test 12: Protected Route - User Cannot Access Admin Dashboard ❌

### Steps:
1. **Log in as regular user** (John)
2. **Try to manually navigate to**: `http://localhost:5000/dashboard/admin`

### Expected Results:
- ✅ Flash message: "You do not have permission to access this page."
- ✅ Redirected to: `http://localhost:5000/`

---

## Test 13: Protected Route - Access Without Login ❌

### Steps:
1. **Make sure you're logged out**
2. **Try to navigate to**: `http://localhost:5000/dashboard/user`

### Expected Results:
- ✅ Redirected to: `http://localhost:5000/login`
- ✅ Message displayed: "Please log in to access this page."

---

## Test 14: Multiple Users Can Register ✅

### Steps:
1. **Sign up another user**:
   - First Name: `Jane`
   - Last Name: `Smith`
   - Email: `jane@example.com`
   - Password: `test12345`
   - Confirm: `test12345`

2. **Log in as Jane**:
   - Email: `jane@example.com`
   - Password: `test12345`

3. **Verify dashboard shows Jane's info**

### Expected Results:
- ✅ New user created successfully
- ✅ Dashboard shows: "Welcome, Jane! 👋"
- ✅ Profile shows: "Name: Jane Smith"

---

## Test 15: Form Validation - Empty Fields ❌

### Steps:
1. **Go to signup page**
2. **Try to submit form with empty fields**
3. **Browser should show required field warnings**

### Expected Results:
- ✅ Browser validation (HTML5) prevents submission
- ✅ If browser validation bypassed, server shows errors

---

## Test 16: Email Format Validation ❌

### Steps:
1. **Go to signup page**
2. **Enter invalid email**: `notanemail`
3. **Try to submit**

### Expected Results:
- ✅ Browser email validation triggered OR
- ✅ Server validation error: "Invalid email address"

---

## Test 17: Session Persistence ✅

### Steps:
1. **Log in as John**
2. **Navigate to different pages**: `/blog`, `/contact`, `/`
3. **Navigation bar still shows**: "Welcome, John"
4. **Try to go to `/dashboard/user`** - Should work

### Expected Results:
- ✅ Session persists across pages
- ✅ Can access protected routes while logged in

---

## Test 18: Admin Cannot Access User Dashboard ❌

### Steps:
1. **Log in as admin**
2. **Try to navigate to**: `http://localhost:5000/dashboard/user`

### Expected Results:
- ✅ Redirected to: `http://localhost:5000/dashboard/admin`

---

## Test 19: Navigation Header Responsive ✅

### Steps:
1. **Log in as user**
2. **Click on "Welcome, John"** in navigation
3. **Should navigate to user dashboard**

### Expected Results:
- ✅ Clicking welcome message is clickable and functional
- ✅ Links to correct dashboard

---

## Test 20: Complete User Journey ✅

### Steps:
1. Start at homepage (`/`)
2. Click "SIGN UP"
3. Create account
4. Should redirect to login
5. Log in
6. Should see user dashboard
7. Click "LOGOUT"
8. Should see login/signup links again

### Expected Results:
- ✅ All steps complete successfully
- ✅ Navigation updates at each step
- ✅ Proper flash messages throughout

---

## Summary Checklist

- [ ] Admin account auto-created on startup
- [ ] Admin login works correctly
- [ ] User signup with validation works
- [ ] User login works correctly
- [ ] Logout works and clears session
- [ ] Navigation updates based on auth state
- [ ] Dashboards show correct information
- [ ] Protected routes redirect properly
- [ ] Invalid credentials show errors
- [ ] Duplicate emails are rejected
- [ ] Password validation works
- [ ] Form validation errors display correctly
- [ ] Users cannot access each other's pages
- [ ] Flash messages display appropriately
- [ ] All links and buttons work correctly

---

## Common Issues & Solutions

### Issue: Admin account not created
**Solution**: Delete `app.db` and restart the app

### Issue: "User already exists" error on subsequent runs
**Solution**: This is expected - admin is only created once. Try signing up as different user.

### Issue: Login page shows errors but form submits anyway
**Solution**: Clear browser cache and try again

### Issue: Session not persisting
**Solution**: Check that cookies are enabled in browser, restart Flask app

### Issue: Redirect loops
**Solution**: Clear browser cache and cookies, restart the app

---

## Performance Notes

- First app startup: Creates admin account (one-time only)
- Login/Logout: Fast (simple database query)
- Form validation: Real-time client-side + server-side
- Database: SQLite (suitable for development)

---

## Ready to Test! 🚀

All systems go. Run the app and follow the tests in order. Each test should pass. If any fail, check the error messages and logs.
