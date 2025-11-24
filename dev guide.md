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
├── app.py                 # Flask app factory + routes
├── models.py              # Database models (User, Admin)
├── forms.py               # WTForms validation (SignUp, Login)
├── config.py              # Configuration (Dev, Test, Prod)
├── extension.py           # Flask extensions (db, migrate, login_manager)
├── decorators.py          # Custom decorators
├── static/css/style.css   # Responsive styling
├── templates/             # Jinja2 templates
│   ├── base.html          # Base template with navigation
│   ├── homepage.html
│   ├── login.html
│   ├── signup.html
│   ├── contactus.html
│   ├── admin/admindash.html
│   └── user/userdash.html
├── migrations/            # Database migrations (Flask-Migrate)
├── instance/app.db        # SQLite database
└── uploads/               # User file uploads
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
