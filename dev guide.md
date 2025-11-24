# Development Guide

## Project Setup

### 1. Virtual Environment

Create and activate a virtual environment to isolate project dependencies:

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

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

The `.env` file is already created. Verify these settings:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
```

**For production, change:**
- `FLASK_ENV=production`
- `SECRET_KEY` to a strong random key
- `DATABASE_URL` to your production database

### 4. Database Initialization

**First time only:**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

**After each model change:**
```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

## Running the Application

Start the development server:

```bash
flask run
```

The app will be available at `http://localhost:5000`

The server automatically reloads when you make code changes.

## Project Structure Overview

```
├── app.py                 # Flask application factory
│                          # - create_app() function
│                          # - Route definitions
│
├── config.py              # Configuration classes
│                          # - Config (base)
│                          # - DevelopmentConfig
│                          # - TestingConfig
│                          # - ProductionConfig
│
├── extension.py           # Flask extensions
│                          # - SQLAlchemy (db)
│                          # - Migrate (db migrations)
│                          # - LoginManager (authentication)
│
├── models.py              # Database models
│                          # - User model
│                          # - BlogPost model
│                          # - Other models
│
├── forms.py               # WTForms for validation
│                          # - LoginForm
│                          # - SignupForm
│                          # - BlogPostForm
│
├── decorators.py          # Custom decorators
│                          # - @login_required
│                          # - @admin_required
│
├── static/                # Static files (not served by Flask in production)
│   ├── css/
│   │   └── style.css      # Main stylesheet (mobile-responsive)
│   └── img/               # Images directory
│
├── templates/             # Jinja2 HTML templates
│   ├── homepage.html      # Main homepage
│   ├── login.html         # Login page
│   ├── signup.html        # Signup page
│   ├── contactus.html     # Contact form page
│   ├── admin/
│   │   └── admindash.html # Admin dashboard
│   └── user/
│       └── userdash.html  # User dashboard
│
├── migrations/            # Alembic database migrations
│                          # - Generated automatically with flask db migrate
│
└── instance/              # Instance-specific files (ignored in git)
    └── app.db             # SQLite database
```

## Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Code Changes

- Edit files in the project
- Flask development server auto-reloads on save
- Test your changes at `http://localhost:5000`

### 3. Update Database (if needed)

If you modify models in `models.py`:

```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

### 4. Commit Changes
```bash
git add .
git commit -m "Description of changes"
```

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

## Adding New Features

### Example: Creating a New Model

**1. Add to `models.py`:**
```python
from extension import db
from datetime import datetime

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```

**2. Create migration:**
```bash
flask db migrate -m "Add BlogPost model"
flask db upgrade
```

**3. Create a form in `forms.py`:**
```python
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
```

**4. Add routes in `app.py`:**
```python
@app.route('/post/create', methods=['GET', 'POST'])
def create_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        # Handle form submission
        pass
    return render_template('create_post.html', form=form)
```

**5. Create template `templates/create_post.html`**

## CSS Styling

### Mobile-Responsive Design

The main stylesheet is `static/css/style.css` with responsive breakpoints:

- **Desktop:** Full layout
- **Tablet (≤768px):** Adjusted spacing and font sizes
- **Mobile (≤480px):** Single column, optimized touch targets

### Colors Used

- **Primary Orange:** `#f5a623`
- **Dark Background:** `#1a1a1a`
- **Text Color:** `#333`
- **Light Background:** `#fafafa`

### Example: Adding Responsive CSS

```css
/* Desktop */
.element {
    font-size: 20px;
    padding: 20px;
}

/* Tablet */
@media (max-width: 768px) {
    .element {
        font-size: 18px;
        padding: 15px;
    }
}

/* Mobile */
@media (max-width: 480px) {
    .element {
        font-size: 16px;
        padding: 10px;
    }
}
```

## Debugging

### Enable Debug Mode

Set `FLASK_ENV=development` in `.env` (already done)

### Use Python Debugger

```python
import pdb

@app.route('/debug-route')
def debug_route():
    pdb.set_trace()  # Execution will pause here
    return render_template('page.html')
```

### View Flask Output

Check the terminal where `flask run` is executing for:
- Route information
- Database queries
- Errors and warnings

### Use Browser Developer Tools

- Press `F12` to open Developer Tools
- Check Console tab for JavaScript errors
- Check Network tab for HTTP requests
- Use Inspect Element to debug CSS

## Testing

### Manual Testing

1. Start `flask run`
2. Open `http://localhost:5000`
3. Test all pages and features
4. Check responsive design (F12 → Toggle Device Toolbar)

### Automated Testing (Future)

As the project grows, add unit tests:

```bash
pytest tests/
```

## Common Issues

### "ModuleNotFoundError: No module named 'flask'"

**Solution:** Make sure virtual environment is activated
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### Database errors

**Solution:** Reset the database
```bash
rm instance/app.db
flask db upgrade
```

### Changes not showing up

**Solution:** Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)

## Performance Tips

1. **Use database indexes** for frequently queried fields
2. **Cache static files** in production
3. **Optimize images** before uploading
4. **Use CDN** for external libraries (already using Font Awesome CDN)
5. **Minimize CSS/JavaScript** in production

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [WTForms Documentation](https://wtforms.readthedocs.io/)
- [Font Awesome Icons](https://fontawesome.com/icons)

---

**Happy Development! 🚀**
