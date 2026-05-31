from .auth import auth_bp
from .dashboard import dashboard_bp
from .customer import customer_bp
from .service import service_bp
from .admin import admin_bp

blueprints = [auth_bp, dashboard_bp, customer_bp, service_bp, admin_bp]

__all__ = ['blueprints']