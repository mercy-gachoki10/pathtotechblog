# Development Guide

For general setup and features, see **README.md**.

## Quick Start

```bash
# 1. Setup
python -m venv venv
venv\Scripts\activate  # Windows

# 2. Install
pip install -r requirements.txt

# 3. Run
python app.py
```

Visit: `http://localhost:5000`

## Database Management

**Initial Setup (auto-created on startup):**
```bash
python app.py
```

**After Model Changes:**
```bash
# Create migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade
```

**Reset Database:**
```bash
rm instance/app.db
python app.py
```

## Project Structure

```
├── app.py                      # Flask app factory + routes (9 routes)
├── models.py                   # Database models (User, Admin, BlogPost)
├── forms.py                    # WTForms validation (Login, SignUp, Blog)
├── config.py                   # Configuration + upload settings
├── extension.py                # Flask extensions
├── decorators.py               # Custom decorators
├── static/css/style.css        # Responsive styling
├── templates/
│   ├── base.html               # Base template with navigation
│   ├── homepage.html           # Main page
│   ├── login.html              # Login page
│   ├── signup.html             # Sign up page
│   ├── contactus.html          # Contact page
│   ├── blog/                   # PUBLIC blog templates
│   │   ├── blog_list.html      # Browse published blogs (grid)
│   │   └── blog_detail.html    # View single blog post
│   ├── admin/
│   │   ├── admindash.html      # Admin dashboard
│   │   ├── blog_create.html    # Create new post form
│   │   ├── blog_list.html      # View all user's posts
│   │   └── blog_edit.html      # Edit post form
│   └── user/userdash.html      # User dashboard
├── migrations/                 # Database migrations
├── instance/app.db             # SQLite database
└── uploads/                    # Uploaded featured images
```

## Development Workflow

### Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### Code Changes

**Adding a Model Field:**
```python
# models.py
class User(db.Model):
    # existing fields...
    new_field = db.Column(db.String(100))
```

**Adding a Form Field:**
```python
# forms.py
class SignUpForm(FlaskForm):
    # existing fields...
    new_field = StringField('Label', validators=[DataRequired()])
```

**Adding a Route:**
```python
# app.py
@app.route('/new-route', methods=['GET', 'POST'])
@login_required  # Optional
def new_route():
    form = NewForm()
    if form.validate_on_submit():
        # Handle submission
        pass
    return render_template('template.html', form=form)
```

## Blog System Development

### Blog Model Structure

Located in `models.py`:
```python
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(500))
    featured_image = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    def publish(self):
        """Mark post as published."""
        self.is_published = True
        self.published_at = datetime.utcnow()
    
    def unpublish(self):
        """Mark post as draft."""
        self.is_published = False
        self.published_at = None
```

### Blog Forms

Located in `forms.py`:
```python
class CreateBlogForm(FlaskForm):
    title = StringField('Blog Title', validators=[
        DataRequired(), Length(min=5, max=200)
    ])
    excerpt = StringField('Excerpt', validators=[Length(max=500)])
    content = TextAreaField('Content', validators=[
        DataRequired(), Length(min=10)
    ])
    featured_image = FileField('Featured Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'])
    ])
    is_published = BooleanField('Publish Immediately')
    submit = SubmitField('Create Blog Post')

class EditBlogForm(FlaskForm):
    # Same as CreateBlogForm
```

### Blog Routes

**Admin Routes** (require admin login, `app.py`):
```python
@app.route('/admin/blog/create', methods=['GET', 'POST'])
@login_required
def create_blog():
    """Create new blog post - admin only."""
    if not isinstance(current_user, Admin):
        flash('Permission denied', 'error')
        return redirect(url_for('index'))
    
    form = CreateBlogForm()
    if form.validate_on_submit():
        featured_image = None
        if form.featured_image.data:
            featured_image = save_upload_file(form.featured_image.data)
        
        blog = BlogPost(
            title=form.title.data,
            excerpt=form.excerpt.data,
            content=form.content.data,
            featured_image=featured_image,
            author_id=current_user.id
        )
        
        if form.is_published.data:
            blog.publish()
        
        db.session.add(blog)
        db.session.commit()
        flash('Blog post created!', 'success')
        return redirect(url_for('admin_blog_list'))
    
    return render_template('admin/blog_create.html', form=form)

@app.route('/admin/blog/list')
@login_required
def admin_blog_list():
    """View all admin's blog posts."""
    if not isinstance(current_user, Admin):
        flash('Permission denied', 'error')
        return redirect(url_for('index'))
    
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.filter_by(author_id=current_user.id)\
        .order_by(BlogPost.created_at.desc())\
        .paginate(page=page, per_page=10)
    
    return render_template('admin/blog_list.html', posts=posts)

@app.route('/admin/blog/edit/<int:blog_id>', methods=['GET', 'POST'])
@login_required
def edit_blog(blog_id):
    """Edit blog post - owner only."""
    if not isinstance(current_user, Admin):
        flash('Permission denied', 'error')
        return redirect(url_for('index'))
    
    blog = BlogPost.query.get_or_404(blog_id)
    
    if blog.author_id != current_user.id:
        flash('Can only edit your own posts', 'error')
        return redirect(url_for('admin_blog_list'))
    
    form = EditBlogForm()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.excerpt = form.excerpt.data
        blog.content = form.content.data
        
        if form.featured_image.data:
            featured_image_path = save_upload_file(form.featured_image.data)
            if featured_image_path:
                blog.featured_image = featured_image_path
        
        if form.is_published.data and not blog.is_published:
            blog.publish()
        elif not form.is_published.data and blog.is_published:
            blog.unpublish()
        
        db.session.commit()
        flash('Blog post updated!', 'success')
        return redirect(url_for('admin_blog_list'))
    
    elif request.method == 'GET':
        form.title.data = blog.title
        form.excerpt.data = blog.excerpt
        form.content.data = blog.content
        form.is_published.data = blog.is_published
    
    return render_template('admin/blog_edit.html', form=form, blog=blog)

@app.route('/admin/blog/delete/<int:blog_id>', methods=['POST'])
@login_required
def delete_blog(blog_id):
    """Delete blog post - owner only."""
    if not isinstance(current_user, Admin):
        flash('Permission denied', 'error')
        return redirect(url_for('index'))
    
    blog = BlogPost.query.get_or_404(blog_id)
    
    if blog.author_id != current_user.id:
        flash('Can only delete your own posts', 'error')
        return redirect(url_for('admin_blog_list'))
    
    # Clean up featured image
    if blog.featured_image:
        try:
            filepath = os.path.join(app.root_path, blog.featured_image)
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            app.logger.error(f'Error deleting file: {e}')
    
    db.session.delete(blog)
    db.session.commit()
    flash('Blog post deleted!', 'success')
    return redirect(url_for('admin_blog_list'))
```

**Public Routes** (no login required):
```python
@app.route('/blog')
def blog():
    """Browse all published blog posts."""
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.filter_by(is_published=True)\
        .order_by(BlogPost.published_at.desc())\
        .paginate(page=page, per_page=10)
    
    return render_template('blog/blog_list.html', posts=posts)

@app.route('/blog/<int:blog_id>')
def blog_detail(blog_id):
    """View single blog post."""
    post = BlogPost.query.get_or_404(blog_id)
    
    # Allow admin author or public if published
    if not post.is_published and not (
        current_user.is_authenticated and isinstance(current_user, Admin)
        and post.author_id == current_user.id
    ):
        flash('This blog post is not available', 'error')
        return redirect(url_for('blog'))
    
    return render_template('blog/blog_detail.html', post=post)
```

### File Upload Helper Functions

Located in `app.py`:
```python
from werkzeug.utils import secure_filename
import time

def allowed_file(filename):
    """Check if file type is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def save_upload_file(file):
    """Save uploaded file with timestamp prefix."""
    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to prevent collisions
        filename = f"{int(time.time())}_{filename}"
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        return f"uploads/{filename}"
    return None
```

### Upload Configuration

Located in `config.py`:
```python
import os

class Config:
    # ... existing config ...
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}
    
    @classmethod
    def init_app(cls, app):
        """Initialize upload folder on startup."""
        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)
```

### Template Globals

In `app.py` (inside `create_app()` function):
```python
# Allow templates to use isinstance() and Admin class
app.jinja_env.globals.update(isinstance=isinstance, Admin=Admin)
```

This enables templates to check:
```html
{% if isinstance(current_user, Admin) and current_user.id == post.author_id %}
    <!-- Show edit/delete buttons -->
{% endif %}
```

### Testing Blog Features

**Create a blog post:**
1. Login as admin (admin@techblog.com / admin123)
2. Go to `/admin/blog/create`
3. Fill in title, content, optional image
4. Click "Create Blog Post"
5. Check `/admin/blog/list` to see post

**Edit a blog post:**
1. Go to `/admin/blog/list`
2. Click "Edit" on any post
3. Update fields
4. Click "Update Blog Post"

**Delete a blog post:**
1. Go to `/admin/blog/list`
2. Click "Delete" on any post
3. Confirm deletion

**View public blog:**
1. Go to `/blog` (no login needed)
2. See all published posts
3. Click post title to view full content
4. Navigate between pages

**Publish/unpublish:**
1. Create post with "Publish Immediately" unchecked (draft)
2. Edit post and check "Publish Immediately" to publish
3. Uncheck to unpublish (post becomes draft)

### Blog Templates Reference

**Admin Templates:**
- `templates/admin/blog_create.html` - Create form
- `templates/admin/blog_list.html` - All posts table
- `templates/admin/blog_edit.html` - Edit form with image preview

**Public Templates:**
- `templates/blog/blog_list.html` - Grid of blog cards
- `templates/blog/blog_detail.html` - Full blog view

All templates use `base.html` for consistent styling and navigation.

### Test & Commit
```bash
# Test at http://localhost:5000
# Commit
git add .
git commit -m "Description of changes"
git push origin feature/your-feature-name
```

## Authentication

**Protected Routes:**
```python
from flask_login import login_required, current_user

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)
```

**Check User Type:**
```python
if isinstance(current_user, Admin):
    # Admin only
    pass
elif isinstance(current_user, User):
    # User only
    pass
```

**Session Management:**
```python
from flask_login import login_user, logout_user

login_user(user, remember=True)
logout_user()
```

## CSS Styling

Mobile breakpoints in `static/css/style.css`:
- **Desktop:** > 768px
- **Tablet:** 481px - 768px  
- **Mobile:** ≤ 480px

Colors:
- **Primary:** `#f5a623` (Orange)
- **Dark:** `#1a1a1a`
- **Text:** `#333`

Example responsive CSS:
```css
.element { font-size: 16px; padding: 10px; }

@media (min-width: 768px) {
    .element { font-size: 18px; padding: 15px; }
}
```

## Debugging

**Enable debug mode:**
```bash
# Already enabled in .env (FLASK_ENV=development)
python app.py
```

**Python debugger:**
```python
import pdb
pdb.set_trace()  # Execution pauses here
```

**Browser DevTools (F12):**
- Console: JavaScript errors
- Network: HTTP requests
- Inspect: CSS debugging
- Device toolbar: Responsive testing

**Check logs:**
- Terminal output shows routes, queries, errors
- Flask logger: `app.logger.debug('message')`

## Common Issues

| Issue | Solution |
|-------|----------|
| Virtual env not activated | `venv\Scripts\activate` |
| Module not found | `pip install -r requirements.txt` |
| Database locked | Delete `instance/app.db`, restart |
| Changes not showing | Hard refresh: `Ctrl+Shift+R` |
| Port in use | `flask run --port 5001` |
| Form validation fails | Check CSRF token in template |

## Code Standards

- **Functions:** `lowercase_with_underscores`
- **Classes:** `PascalCase`  
- **Constants:** `UPPERCASE`
- Add docstrings to functions
- Comment complex logic

**Example:**
```python
def validate_user_email(email: str) -> bool:
    """Check if email is registered."""
    return User.query.filter_by(email=email).first() is not None
```

## Resources

- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [WTForms](https://wtforms.readthedocs.io/)
- [Flask-Login](https://flask-login.readthedocs.io/)

---

See **README.md** for full setup, testing, and deployment info!

**Happy Development! 🚀**
