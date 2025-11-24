from flask import Flask, render_template, request, redirect, url_for, flash
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
    from models import User
    
    # Register blueprints
    with app.app_context():
        db.create_all()
    
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
        if request.method == 'POST':
            # Login logic will be added later
            email = request.form.get('email')
            password = request.form.get('password')
            flash('Login functionality coming soon!', 'info')
            return redirect(url_for('index'))
        return render_template('login.html')
    
    # Signup route
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            # Signup logic will be added later
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            flash('Sign up functionality coming soon!', 'info')
            return redirect(url_for('index'))
        return render_template('signup.html')
    
    # Blog route
    @app.route('/blog')
    def blog():
        return render_template('blog.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
