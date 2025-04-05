from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from config import Config
from database import db

# Initialize extensions
login_manager = LoginManager()
csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    return User.query.get(int(user_id))

# Add this after your imports
def create_dummy_user():
    from models.user import User
    dummy_user = User.query.filter_by(username='DAVE').first()
    if not dummy_user:
        dummy_user = User(
            username='DAVE',
            email='dave@test.com',
            full_name='Dave Test',
            location='Test Location',
            password_hash='dummy_hash'
        )
        db.session.add(dummy_user)
        db.session.commit()
    return dummy_user

# Modify the create_app function
def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    csrf.init_app(app)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    csrf.init_app(app)
    
    # Register routes
    from routes import init_routes
    init_routes(app)
    
    # Register view functions
    @app.route('/')
    def home():
        return render_template('home.html')
    
    @app.route('/marketplace')
    def marketplace():
        from controllers.listing_controller import get_listings
        listings_response = get_listings()
        listings = listings_response.get_json()
        return render_template('marketplace.html', listings=listings)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            data = {
                'username': request.form['username'],
                'email': request.form['email'],
                'password': request.form['password'],
                'full_name': request.form['full_name'],
                'location': request.form.get('location', 'Test Location'),  # Default location
                'phone': request.form.get('phone', '1234567890'),  # Default phone
                'bio': request.form.get('bio', 'Test user')  # Default bio
            }
            
            from controllers.user_controller import create_user
            response = create_user()
            
            if response.status_code == 201:
                # Auto-login after registration
                from models.user import User
                user = User.query.filter_by(username=data['username']).first()
                if user:
                    login_user(user)
                    flash('Registration and login successful!', 'success')
                    return redirect(url_for('marketplace'))
            else:
                error_data = response.get_json()
                flash(error_data.get('error', 'Registration failed.'), 'error')
                
        return render_template('register.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            from models.user import User
            username = request.form.get('username')
            password = request.form.get('password')
            
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Logged in successfully!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('home'))
            else:
                flash('Invalid username or password', 'error')
        return render_template('login.html')
    
    @app.route('/listings/create', methods=['GET', 'POST'])
    def create_listing_view():
        # Create dummy user if it doesn't exist
        from models.user import User
        dummy_user = User.query.filter_by(username='DAVE').first()
        if not dummy_user:
            dummy_user = User(
                username='DAVE',
                email='dave@test.com',
                full_name='Dave Test',
                location='Test Location',
                password_hash='dummy_hash'
            )
            db.session.add(dummy_user)
            db.session.commit()
        
        login_user(dummy_user)
        
        if request.method == 'POST':
            # Create listing data from form
            from controllers.listing_controller import create_listing
            # Don't modify the form directly
            # Add user_id to form data
            request.form = request.form.copy()  # Make form mutable
            request.form['user_id'] = str(dummy_user.id)
            
            response = create_listing()
            if isinstance(response, tuple) and len(response) > 1 and response[1] == 201:
                flash('Listing created successfully!', 'success')
                return redirect(url_for('marketplace'))
            else:
                error_data = response[0].json if isinstance(response, tuple) else response.get_json()
                flash(error_data.get('error', 'Error creating listing. Please try again.'), 'error')
    
        return render_template('create_listing.html')
    
    @app.route('/listings/<int:listing_id>')
    def listing_detail(listing_id):
        from controllers.listing_controller import get_listing
        response = get_listing(listing_id)
        if response.status_code == 404:
            flash('Listing not found', 'error')
            return redirect(url_for('marketplace'))
        listing = response.get_json()
        return render_template('listing_detail.html', listing=listing)
    
    @app.route('/listings/<int:listing_id>/edit', methods=['GET', 'POST'])
    def edit_listing(listing_id):
        from controllers.listing_controller import get_listing, update_listing
        
        if request.method == 'POST':
            response = update_listing(listing_id)
            if response.status_code == 200:
                flash('Listing updated successfully!', 'success')
                return redirect(url_for('listing_detail', listing_id=listing_id))
            else:
                error_data = response.get_json()
                flash(error_data.get('error', 'Error updating listing.'), 'error')
        
        response = get_listing(listing_id)
        if response.status_code == 404:
            flash('Listing not found', 'error')
            return redirect(url_for('marketplace'))
        
        listing = response.get_json()
        return render_template('edit_listing.html', listing=listing)

    @app.route('/listings/<int:listing_id>/delete', methods=['POST'])
    def delete_listing_view(listing_id):  # Changed function name to avoid conflict
        from controllers.listing_controller import delete_listing
        response = delete_listing(listing_id)
        
        if response.status_code == 200:
            flash('Listing deleted successfully!', 'success')
        else:
            error_data = response.get_json()
            flash(error_data.get('error', 'Error deleting listing.'), 'error')
        
        return redirect(url_for('marketplace'))

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Create all database tables
        db.create_all()
    app.run(debug=Config.DEBUG)