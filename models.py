from extension import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """User model for regular users"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'

    def get_id(self):
        return f"user_{self.id}"
    
    def set_password(self, password):
        """Hash and set password"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches the hashed password"""
        return check_password_hash(self.password, password)


class Admin(UserMixin, db.Model):
    """Admin model for administrator accounts"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Admin {self.username}>'

    def get_id(self):
        return f"admin_{self.id}"
    
    def set_password(self, password):
        """Hash and set password"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches the hashed password"""
        return check_password_hash(self.password, password)


# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login - checks both User and Admin tables"""
    try:
        # Parse the user_id to determine type
        if '_' in user_id:
            user_type, user_id_num = user_id.split('_')
            user_id_num = int(user_id_num)
            
            if user_type == 'user':
                return User.query.get(user_id_num)
            elif user_type == 'admin':
                return Admin.query.get(user_id_num)
        else:
            # Fallback for old format (shouldn't happen)
            user_id_num = int(user_id)
            user = User.query.get(user_id_num)
            if user:
                return user
            return Admin.query.get(user_id_num)
    except (ValueError, AttributeError):
        return None
