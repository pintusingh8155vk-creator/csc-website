import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import current_user
from extensions import db, login_manager, migrate
from config import config
from routes import blueprints
from models import User, Subscription
from whitenoise import WhiteNoise
from sqlalchemy import text
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'production')
    
    app = Flask(__name__)
    
    # Load configuration
    try:
        app.config.from_object(config[config_name])
    except KeyError:
        app.config.from_object(config['default'])
        logger.warning(f"Config {config_name} not found, using default")
    
    logger.info(f"Starting app with config: {config_name}")
    logger.info(f"Database URL: {app.config.get('SQLALCHEMY_DATABASE_URI')[:50]}...")
    
    # WhiteNoise for static files
    try:
        app.wsgi_app = WhiteNoise(app.wsgi_app, root='static')
    except Exception as e:
        logger.warning(f"WhiteNoise initialization warning: {e}")
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
        logger.info(f"Registered blueprint: {blueprint.name}")
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except Exception as e:
            logger.error(f"Error loading user {user_id}: {e}")
            return None
    
    @login_manager.unauthorized_handler
    def unauthorized():
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.login'))
    
    # Context processor
    @app.context_processor
    def inject_user():
        return {'current_user': current_user}
    
    # Routes
    @app.route('/')
    def index():
        """Homepage"""
        try:
            if current_user.is_authenticated:
                return redirect(url_for('dashboard.index'))
        except Exception as e:
            logger.error(f"Error in index route: {e}")
        return render_template('index.html')
    
    @app.route('/pricing')
    def pricing():
        """Pricing page"""
        plans = {
            'free': {'price': 0, 'features': ['5 Customers', 'Basic Dashboard', 'Email Support']},
            'starter': {'price': 499, 'features': ['Unlimited Customers', 'Advanced Reports', 'Priority Support']},
            'professional': {'price': 999, 'features': ['All Starter', 'Payment Processing', 'API Access']},
            'enterprise': {'price': 2999, 'features': ['All Features', 'Dedicated Support', 'Custom Integration']}
        }
        return render_template('pricing.html', plans=plans)
    
    @app.route('/about')
    def about():
        """About page"""
        return render_template('about.html')
    
    @app.route('/contact')
    def contact():
        """Contact page"""
        return render_template('contact.html')
    
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        try:
            db.session.rollback()
        except Exception as e:
            logger.error(f"Error rolling back session: {e}")
        return render_template('errors/500.html'), 500
    
    # Create upload folder
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except Exception as e:
        logger.warning(f"Could not create upload folder: {e}")
    
    # Create app context and initialize database
    with app.app_context():
        try:
            # Test database connection
            with db.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            logger.info("✅ Database connection successful")
            
            # Create all tables
            db.create_all()
            logger.info("✅ Database tables created/verified")
            
            # Create default admin user if not exists
            admin_exists = User.query.filter_by(email='admin@cybercafe.com').first()
            if not admin_exists:
                admin = User(
                    full_name='Admin',
                    shop_name='CyberCafe Admin',
                    mobile_number='9999999999',
                    email='admin@cybercafe.com',
                    is_admin=True,
                    is_active=True
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                logger.info("✅ Admin user created")
            
        except Exception as e:
            logger.error(f"❌ Database initialization error: {e}")
            logger.error(f"Make sure DATABASE_URL is set correctly")
    
    return app

# Create app instance
try:
    app = create_app()
    logger.info("✅ Application created successfully")
except Exception as e:
    logger.error(f"❌ Failed to create application: {e}")
    raise

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
