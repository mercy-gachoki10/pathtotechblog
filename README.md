# Women in Tech Blog

A Flask-based web application dedicated to building a supportive community for women in technology.

## Features

- ✨ Responsive design (mobile, tablet, desktop)
- 🔐 User authentication (login/signup)
- 📝 Blog/article posting
- 👥 Community features
- 👨‍💼 Admin dashboard
- 🎨 Beautiful UI inspired by SheCan Code

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

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

4. **Set up environment variables:**

Create a `.env` file in the root directory (it's already created, just verify the values):
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
```

5. **Initialize the database:**
```bash
flask db upgrade
```

### Running the Application

```bash
flask run
```

The application will be available at `http://localhost:5000`

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

## Development

See [dev guide.md](dev%20guide.md) for detailed development guidelines.

## Technology Stack

- **Backend:** Flask, Flask-SQLAlchemy, Flask-Migrate
- **Authentication:** Flask-Login
- **Forms:** WTForms, email-validator
- **Database:** SQLite (development), PostgreSQL (production recommended)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Icons:** Font Awesome 6.4.0

## Features Overview

### Current Features
- Homepage with hero section
- Mobile-responsive design
- Navigation menu (desktop and mobile)
- Search functionality (UI ready for implementation)

### Upcoming Features
- User registration and login
- Blog post creation and management
- User profiles
- Admin panel
- Community features
- Comment system

## Contributing

Please follow the development guidelines in [dev guide.md](dev%20guide.md)

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please create an issue in the repository.

---

**Happy coding! 💻✨**
