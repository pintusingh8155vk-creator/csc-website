import os
from flask import Flask, render_template, redirect, url_for
from flask_login import current_user
from extensions import db, login_manager, migrate
from config import config
from routes import blueprints
from models import User
from whitenoise import WhiteNoise

def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # WhiteNoise for static files
    app.wsgi_app = WhiteNoise(app.wsgi_app, root='static')
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    
    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Context processor
    @app.context_processor
    def inject_user():
        return {'current_user': current_user}
    
    # Routes
    @app.route('/')
    def index():
        """Homepage"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
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
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Create upload folder
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)