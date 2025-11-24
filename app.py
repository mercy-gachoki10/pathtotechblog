from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from config import Config
from extension import db, migrate, login_manager
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Import models (must be after extension initialization)
    from models import User, Admin
    from forms import SignUpForm, LoginForm
    
    # Register blueprints
    with app.app_context():
        db.create_all()
        
        # Initialize admin account if it doesn't exist
        admin_user = Admin.query.filter_by(email='admin@techblog.com').first()
        if not admin_user:
            admin_user = Admin(
                username='admin',
                email='admin@techblog.com'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("Admin account created successfully!")
    
    # Home route
    @app.route('/')
    def index():
        return render_template('homepage.html')
    
    # Contact Us route
    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        if request.method == 'POST':
            # Form submission logic will be added later
            flash('Thank you for your message! We will get back to you soon.', 'success')
            return redirect(url_for('contact'))
        return render_template('contactus.html')
    
    # Login route
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            # Check if user is admin or regular user
            if isinstance(current_user, Admin):
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        
        form = LoginForm()
        if form.validate_on_submit():
            # Try to authenticate as regular user first
            user = User.query.filter_by(email=form.email.data).first()
            
            if user and user.check_password(form.password.data):
                login_user(user)
                flash(f'Welcome back, {user.first_name}!', 'success')
                return redirect(url_for('user_dashboard'))
            
            # Try to authenticate as admin
            admin = Admin.query.filter_by(email=form.email.data).first()
            
            if admin and admin.check_password(form.password.data):
                login_user(admin)
                flash('Welcome admin!', 'success')
                return redirect(url_for('admin_dashboard'))
            
            # Invalid credentials
            flash('Invalid email or password.', 'error')
        
        return render_template('login.html', form=form)
    
    # Signup route
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if current_user.is_authenticated:
            return redirect(url_for('user_dashboard'))
        
        form = SignUpForm()
        if form.validate_on_submit():
            # Create new user
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        
        return render_template('signup.html', form=form)
    
    # Blog route
    @app.route('/blog')
    def blog():
        return render_template('blog.html')
    
    # User Dashboard route
    @app.route('/dashboard/user')
    @login_required
    def user_dashboard():
        if isinstance(current_user, Admin):
            return redirect(url_for('admin_dashboard'))
        return render_template('user/userdash.html', user=current_user)
    
    # Admin Dashboard route
    @app.route('/dashboard/admin')
    @login_required
    def admin_dashboard():
        if not isinstance(current_user, Admin):
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('index'))
        return render_template('admin/admindash.html', admin=current_user)
    
    # Logout route
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out successfully.', 'success')
        return redirect(url_for('index'))
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
