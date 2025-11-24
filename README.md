# Women in Tech Blog

A Flask-based web application dedicated to building a supportive community for women in technology.

## ⚡ Quick Start

```bash
# 1. Clone and navigate
git clone <repository-url>
cd pathtotechblog

# 2. Set up environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py
```

Visit `http://localhost:5000` - Admin account auto-created:
- **Email:** `admin@techblog.com`
- **Password:** `admin123`

## Features

- ✨ Responsive design (mobile, tablet, desktop)
- 🔐 Secure user authentication (login/signup) with password hashing
- 👤 Separate User and Admin accounts with role-based dashboards
- 📝 **Blog system** - Admin-only blog post creation, editing, deletion, and publishing
- 🖼️ **File uploads** - Featured images for blog posts with secure file handling
- 👥 Community features (coming soon)
- 👨‍💼 Admin dashboard with management tools
- 🎨 Beautiful UI inspired by SheCan Code
- 🔒 CSRF protection and form validation

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation & Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd pathtotechblog
```

2. **Create and activate a virtual environment:**

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Environment variables** (already configured):
Create a `.env` file in the root directory with:
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
```

### Running the Application

```bash
python app.py
```

Or use Flask CLI:
```bash
flask run
```

The application will be available at `http://localhost:5000`

**Admin Account (Auto-Created):**
- Email: `admin@techblog.com`
- Password: `admin123`

## Project Structure

```
pathtotechblog/
├── app.py                 # Flask application factory and main routes
├── config.py              # Configuration settings for different environments
├── extension.py           # Flask extensions initialization
├── models.py              # Database models
├── forms.py               # WTForms for user input validation
├── decorators.py          # Custom decorators
├── static/
│   ├── css/
│   │   └── style.css      # Mobile-responsive stylesheet
│   └── img/               # Images directory
├── templates/
│   ├── homepage.html      # Main homepage
│   ├── login.html         # Login page
│   ├── signup.html        # Signup page
│   ├── contactus.html     # Contact page
│   ├── admin/
│   │   └── admindash.html # Admin dashboard
│   └── user/
│       └── userdash.html  # User dashboard
├── migrations/            # Database migration files
├── instance/              # Instance-specific files (database, etc.)
├── uploads/               # User uploads directory
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md              # This file
```

## Authentication System

### User Models
- **User** - Regular users who sign up with email/password
- **Admin** - Admin account (auto-created) for site management

### Features
- ✅ Email validation and uniqueness checking
- ✅ Password hashing with werkzeug security
- ✅ CSRF protection on all forms
- ✅ Session management with Flask-Login
- ✅ Role-based route protection

### Flows

**User Sign Up:**
1. Navigate to `/signup`
2. Fill in: First Name, Last Name, Email, Password
3. Click "Create Account"
4. Redirected to login page
5. Login with your email and password
6. Redirected to user dashboard at `/dashboard/user`

**Admin Login:**
1. Navigate to `/login`
2. Email: `admin@techblog.com` | Password: `admin123`
3. Redirected to admin dashboard at `/dashboard/admin`

**Logout:**
1. Click "LOGOUT" in navigation
2. Session cleared, redirected to homepage

### Session ID Bug Fix (v1.1)
Fixed critical session collision bug where User and Admin sessions would conflict:
- User `get_id()` now returns `user_{id}` format
- Admin `get_id()` now returns `admin_{id}` format
- User loader automatically routes to correct table based on prefix

## Blog System

### Admin Blog Management

**Admin-only features** available at `/admin/blog/`:
- ✅ Create blog posts with title, content, excerpt, featured image
- ✅ Edit existing posts (change content, image, status)
- ✅ Delete posts (removes from database and deletes image files)
- ✅ Publish/unpublish posts (control visibility)
- ✅ View all your posts in a dashboard

### Public Blog Access

**Anyone can view published blogs** (no login required):
- ✅ Browse all published blog posts at `/blog`
- ✅ View individual blog posts at `/blog/<id>`
- ✅ See author name and publication date
- ✅ Beautiful responsive grid layout
- ✅ Pagination (10 posts per page)

### File Upload System

**Featured image uploads:**
- 📁 Uploaded to `uploads/` folder
- 🔒 Secure filename generation with timestamps
- 📏 Max file size: 16MB
- 🖼️ Supported formats: JPG, JPEG, PNG, GIF, PDF, DOC, DOCX
- 🗑️ Automatic cleanup when posts are deleted

### Blog Database Schema

```python
BlogPost Model:
├── id (Integer, Primary Key)
├── title (String, max 200 chars)
├── content (Text, full blog content)
├── excerpt (String, max 500 chars, preview text)
├── featured_image (String, file path)
├── author_id (Foreign Key → Admin)
├── is_published (Boolean, visible to public)
├── created_at (DateTime)
├── updated_at (DateTime)
└── published_at (DateTime)
```

### Blog Routes

**Admin Routes (requires login as admin):**
```
GET    /admin/blog/create       Show create form
POST   /admin/blog/create       Create new blog post
GET    /admin/blog/list         View all your posts
GET    /admin/blog/edit/<id>    Show edit form
POST   /admin/blog/edit/<id>    Update blog post
POST   /admin/blog/delete/<id>  Delete blog post
```

**Public Routes (no login required):**
```
GET    /blog                    List all published posts
GET    /blog/<id>               View single blog post
```

### Blog Templates

**Admin templates:**
- `templates/admin/blog_create.html` - Create new blog post form
- `templates/admin/blog_list.html` - View all your posts in table format
- `templates/admin/blog_edit.html` - Edit existing blog post

**Public templates:**
- `templates/blog/blog_list.html` - Browse published blogs (grid layout)
- `templates/blog/blog_detail.html` - Read full blog post

## Technology Stack

- **Backend:** Flask, Flask-SQLAlchemy, Flask-Migrate
- **Authentication:** Flask-Login
- **Forms:** WTForms, email-validator
- **Database:** SQLite (development), PostgreSQL (production recommended)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Icons:** Font Awesome 6.4.0

## Features Overview

### ✅ Implemented
- Homepage with hero section
- Mobile-responsive design (480px, 768px breakpoints)
- Navigation menu (desktop and mobile)
- User sign up with validation
- User login/logout with session management
- Admin account auto-creation
- Admin login/logout
- User dashboard (`/dashboard/user`)
- Admin dashboard (`/dashboard/admin`)
- Form validation (email uniqueness, password matching, min length)
- Password hashing and security
- CSRF protection (Flask-WTF)
- Protected routes with @login_required
- **Blog system with admin-only post management** ✨
- **File uploads for featured images** ✨
- **Public blog viewing without login** ✨

### 🚧 Upcoming
- Blog post creation and management
- User profile pages
- Advanced admin panel
- Community features
- Comment system
- User search and filtering

## Development

### Project Structure

```
pathtotechblog/
├── app.py                 # Flask application factory with routes
├── config.py              # Configuration settings
├── extension.py           # Flask extensions initialization
├── models.py              # Database models (User, Admin)
├── forms.py               # WTForms for signup/login validation
├── decorators.py          # Custom decorators
├── static/
│   ├── css/
│   │   └── style.css      # Mobile-responsive stylesheet
│   └── img/               # Images directory
├── templates/
│   ├── base.html          # Base template with dynamic navigation
│   ├── homepage.html      # Main homepage
│   ├── login.html         # Login page
│   ├── signup.html        # Signup page
│   ├── contactus.html     # Contact page
│   ├── admin/
│   │   └── admindash.html # Admin dashboard
│   └── user/
│       └── userdash.html  # User dashboard
├── migrations/            # Database migration files (Flask-Migrate)
├── instance/              # Instance-specific files (app.db)
├── uploads/               # User uploads directory
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md              # This file
```

### Database Setup

First time only:
```bash
# Using create_all() method (tables auto-created on startup)
python app.py
```

After model changes:
```bash
# Create new migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade
```

### Running in Development

```bash
# With auto-reload
python app.py
```

The server reloads automatically when you save files.

### Adding New Features

**Example: Adding a new User field**

1. Update model in `models.py`:
```python
class User(UserMixin, db.Model):
    # ... existing fields ...
    new_field = db.Column(db.String(100))
```

2. Update form in `forms.py`:
```python
class SignUpForm(FlaskForm):
    # ... existing fields ...
    new_field = StringField('New Field', validators=[DataRequired()])
```

3. Update route in `app.py`:
```python
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            # ... existing fields ...
            new_field=form.new_field.data
        )
        # ... rest of logic
```

4. Update templates if needed

5. Create migration:
```bash
flask db migrate -m "Add new_field to User"
flask db upgrade
```

### CSS & Responsive Design

Main stylesheet: `static/css/style.css`

Breakpoints:
- **Desktop:** Full layout (> 768px)
- **Tablet:** Adjusted spacing (481px - 768px)
- **Mobile:** Single column, touch-optimized (≤ 480px)

Colors:
- Primary Orange: `#f5a623`
- Dark: `#1a1a1a`
- Text: `#333`
- Light: `#fafafa`

### Testing Checklist

Before deploying, verify:

1. **Authentication:**
   - [ ] Admin login works
   - [ ] User signup works
   - [ ] User login works
   - [ ] Logout works and clears session
   - [ ] Switching between user types maintains correct session

2. **Forms:**
   - [ ] Email validation (duplicates rejected)
   - [ ] Password strength (min 6 chars)
   - [ ] Password confirmation match
   - [ ] Required fields show errors

3. **Dashboards:**
   - [ ] User dashboard shows user info
   - [ ] Admin dashboard shows admin info
   - [ ] Protected routes redirect to login when not authenticated
   - [ ] Navigation updates based on auth state

4. **Responsive Design:**
   - [ ] Mobile view (480px)
   - [ ] Tablet view (768px)
   - [ ] Desktop view
   - [ ] Touch targets are adequate

5. **Security:**
   - [ ] CSRF tokens on forms
   - [ ] Passwords are hashed
   - [ ] Session IDs are type-prefixed (user_, admin_)

### Debugging

**Enable debug mode:**
```python
# app.py
app.run(debug=True)
```

**Database issues:**
```bash
# Reset database
rm instance/app.db
python app.py
```

**Check Flask output:**
- Routes registered
- Database queries
- Errors and warnings

**Browser debugging:**
- Press `F12` for Developer Tools
- Check Console for JavaScript errors
- Check Network for HTTP requests
- Use Inspect for CSS debugging

### Common Issues

| Issue | Solution |
|-------|----------|
| "ModuleNotFoundError: No module named 'flask'" | Activate virtual environment: `venv\Scripts\activate` |
| Database errors | Delete `instance/app.db` and restart |
| Session not persisting | Check browser cookies enabled, reload page |
| Changes not showing | Hard refresh: `Ctrl+Shift+R` |
| Admin account not created | Check `app.py` app context initialization |

### Performance Tips

1. Use database indexes for frequently queried fields
2. Cache static files in production
3. Optimize images before uploading
4. Use CDN for external libraries
5. Minimize CSS/JavaScript in production

## Contributing

### Development Workflow

1. **Create a feature branch:**
```bash
git checkout -b feature/your-feature-name
```

2. **Make code changes:**
- Edit files in the project
- Test changes at `http://localhost:5000`

3. **Commit changes:**
```bash
git add .
git commit -m "Clear description of changes"
```

4. **Push and create pull request:**
```bash
git push origin feature/your-feature-name
```

### Code Standards

- Use descriptive variable names
- Add comments for complex logic
- Update documentation when adding features
- Test responsive design on multiple screen sizes
- Ensure all forms have CSRF protection

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [WTForms Documentation](https://wtforms.readthedocs.io/)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/)
- [Font Awesome Icons](https://fontawesome.com/icons)

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check existing issues in the repository
2. Create a new issue with detailed description
3. Include steps to reproduce for bugs
4. Attach screenshots for UI issues

---

**Happy coding! 💻✨**
