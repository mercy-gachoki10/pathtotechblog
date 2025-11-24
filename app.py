from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from config import Config
from extension import db, migrate, login_manager
from werkzeug.utils import secure_filename
import os

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def save_upload_file(file):
    """Save uploaded file and return the relative path"""
    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to filename to make it unique
        import time
        filename = f"{int(time.time())}_{filename}"
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        return f"uploads/{filename}"
    return None

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Import models (must be after extension initialization)
    from models import User, Admin, BlogPost, Comment
    from forms import SignUpForm, LoginForm, CreateBlogForm, EditBlogForm, CommentForm, ReplyCommentForm
    
    # Add isinstance to template globals
    app.jinja_env.globals.update(isinstance=isinstance, Admin=Admin)
    
    # Register blueprints
    with app.app_context():
        # Use migrations, but create tables if they don't exist
        db.create_all()
        
        # Initialize admin account if it doesn't exist
        try:
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
        except Exception as e:
            # If there's an error querying, that's okay
            pass
    
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
    
    # Blog route - public view of all published blogs
    @app.route('/blog')
    def blog():
        """View all published blog posts"""
        page = request.args.get('page', 1, type=int)
        posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.published_at.desc()).paginate(page=page, per_page=10)
        return render_template('blog/blog_list.html', posts=posts)
    
    # Blog detail route - view single blog post (public)
    @app.route('/blog/<int:blog_id>')
    def blog_detail(blog_id):
        """View a single blog post"""
        post = BlogPost.query.get_or_404(blog_id)
        
        # Only show published posts to non-admins
        if not post.is_published and not (current_user.is_authenticated and isinstance(current_user, Admin)):
            flash('This blog post is not available.', 'error')
            return redirect(url_for('blog'))
        
        form = CommentForm()
        return render_template('blog/blog_detail.html', post=post, form=form)
    
    # Admin: Create blog post
    @app.route('/admin/blog/create', methods=['GET', 'POST'])
    @login_required
    def create_blog():
        """Create a new blog post (admin only)"""
        if not isinstance(current_user, Admin):
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('index'))
        
        form = CreateBlogForm()
        if form.validate_on_submit():
            # Handle file upload
            featured_image = None
            if form.featured_image.data:
                featured_image = save_upload_file(form.featured_image.data)
            
            # Create blog post
            blog = BlogPost(
                title=form.title.data,
                excerpt=form.excerpt.data,
                content=form.content.data,
                featured_image=featured_image,
                author_id=current_user.id
            )
            
            # Publish if checkbox was checked
            if form.is_published.data:
                blog.publish()
            
            db.session.add(blog)
            db.session.commit()
            
            flash('Blog post created successfully!', 'success')
            return redirect(url_for('admin_blog_list'))
        
        return render_template('admin/blog_create.html', form=form)
    
    # Admin: List all blog posts
    @app.route('/admin/blog/list')
    @login_required
    def admin_blog_list():
        """List all blog posts for admin"""
        if not isinstance(current_user, Admin):
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('index'))
        
        page = request.args.get('page', 1, type=int)
        posts = BlogPost.query.filter_by(author_id=current_user.id).order_by(BlogPost.created_at.desc()).paginate(page=page, per_page=10)
        return render_template('admin/blog_list.html', posts=posts)
    
    # Admin: Edit blog post
    @app.route('/admin/blog/edit/<int:blog_id>', methods=['GET', 'POST'])
    @login_required
    def edit_blog(blog_id):
        """Edit a blog post (admin only)"""
        if not isinstance(current_user, Admin):
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('index'))
        
        blog = BlogPost.query.get_or_404(blog_id)
        
        # Check if user is the author
        if blog.author_id != current_user.id:
            flash('You can only edit your own blog posts.', 'error')
            return redirect(url_for('admin_blog_list'))
        
        form = EditBlogForm()
        if form.validate_on_submit():
            blog.title = form.title.data
            blog.excerpt = form.excerpt.data
            blog.content = form.content.data
            
            # Handle file upload
            if form.featured_image.data:
                featured_image_path = save_upload_file(form.featured_image.data)
                if featured_image_path:
                    blog.featured_image = featured_image_path
            
            # Handle publish status
            if form.is_published.data and not blog.is_published:
                blog.publish()
            elif not form.is_published.data and blog.is_published:
                blog.unpublish()
            
            db.session.commit()
            flash('Blog post updated successfully!', 'success')
            return redirect(url_for('admin_blog_list'))
        
        # Pre-fill form with existing data
        elif request.method == 'GET':
            form.title.data = blog.title
            form.excerpt.data = blog.excerpt
            form.content.data = blog.content
            form.is_published.data = blog.is_published
        
        return render_template('admin/blog_edit.html', form=form, blog=blog)
    
    # Admin: Delete blog post
    @app.route('/admin/blog/delete/<int:blog_id>', methods=['POST'])
    @login_required
    def delete_blog(blog_id):
        """Delete a blog post (admin only)"""
        if not isinstance(current_user, Admin):
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('index'))
        
        blog = BlogPost.query.get_or_404(blog_id)
        
        # Check if user is the author
        if blog.author_id != current_user.id:
            flash('You can only delete your own blog posts.', 'error')
            return redirect(url_for('admin_blog_list'))
        
        # Delete featured image if it exists
        if blog.featured_image:
            try:
                filepath = os.path.join(app.root_path, blog.featured_image)
                if os.path.exists(filepath):
                    os.remove(filepath)
            except Exception as e:
                app.logger.error(f'Error deleting file: {e}')
        
        db.session.delete(blog)
        db.session.commit()
        
        flash('Blog post deleted successfully!', 'success')
        return redirect(url_for('admin_blog_list'))
    
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
    
    # Serve uploaded files
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        """Serve uploaded files from the uploads folder"""
        return send_from_directory(Config.UPLOAD_FOLDER, filename)
    
    # Comment routes
    @app.route('/blog/<int:blog_id>/comment', methods=['POST'])
    def post_comment(blog_id):
        """Post a comment on a blog post"""
        post = BlogPost.query.get_or_404(blog_id)
        
        # Check if comments are enabled for this post
        if not post.allow_comments:
            flash('Comments are disabled for this post.', 'error')
            return redirect(url_for('blog_detail', blog_id=blog_id))
        
        form = CommentForm()
        if form.validate_on_submit():
            # Get user_id if logged in
            user_id = None
            if current_user.is_authenticated:
                user_id = current_user.id
            
            comment = Comment(
                content=form.content.data,
                author_name=form.author_name.data,
                user_id=user_id,
                blog_post_id=blog_id
            )
            
            db.session.add(comment)
            db.session.commit()
            
            flash('Your comment has been posted!', 'success')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{error}', 'error')
        
        return redirect(url_for('blog_detail', blog_id=blog_id))
    
    @app.route('/blog/<int:blog_id>/comment/<int:comment_id>/reply', methods=['POST'])
    def reply_comment(blog_id, comment_id):
        """Reply to a comment on a blog post"""
        post = BlogPost.query.get_or_404(blog_id)
        parent_comment = Comment.query.get_or_404(comment_id)
        
        # Check if comments are enabled
        if not post.allow_comments:
            flash('Comments are disabled for this post.', 'error')
            return redirect(url_for('blog_detail', blog_id=blog_id))
        
        form = ReplyCommentForm()
        if form.validate_on_submit():
            # Only logged-in users can reply
            if not current_user.is_authenticated:
                flash('You must be logged in to reply to comments.', 'error')
                return redirect(url_for('login'))
            
            user_id = None
            if isinstance(current_user, User):
                user_id = current_user.id
            
            reply = Comment(
                content=form.content.data,
                author_name=form.author_name.data,
                user_id=user_id,
                blog_post_id=blog_id,
                parent_comment_id=comment_id
            )
            
            db.session.add(reply)
            db.session.commit()
            
            flash('Your reply has been posted!', 'success')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{error}', 'error')
        
        return redirect(url_for('blog_detail', blog_id=blog_id))
    
    # Admin: Toggle comments on a post
    @app.route('/admin/blog/<int:blog_id>/toggle-comments', methods=['POST'])
    @login_required
    def toggle_comments(blog_id):
        """Toggle comments on/off for a blog post"""
        if not isinstance(current_user, Admin):
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('index'))
        
        blog = BlogPost.query.get_or_404(blog_id)
        
        if blog.author_id != current_user.id:
            flash('You can only manage comments on your own blog posts.', 'error')
            return redirect(url_for('admin_blog_list'))
        
        blog.allow_comments = not blog.allow_comments
        db.session.commit()
        
        status = 'enabled' if blog.allow_comments else 'disabled'
        flash(f'Comments {status} for this post.', 'success')
        return redirect(url_for('edit_blog', blog_id=blog_id))
    
    # Admin: Delete comment
    @app.route('/admin/comment/<int:comment_id>/delete', methods=['POST'])
    @login_required
    def delete_comment(comment_id):
        """Delete a comment (admin of blog post only)"""
        if not isinstance(current_user, Admin):
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('index'))
        
        comment = Comment.query.get_or_404(comment_id)
        blog_id = comment.blog_post_id
        blog = BlogPost.query.get_or_404(blog_id)
        
        # Only admin author can delete comments on their posts
        if blog.author_id != current_user.id:
            flash('You can only delete comments on your own blog posts.', 'error')
            return redirect(url_for('blog_detail', blog_id=blog_id))
        
        db.session.delete(comment)
        db.session.commit()
        
        flash('Comment deleted successfully!', 'success')
        return redirect(url_for('blog_detail', blog_id=blog_id))
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
