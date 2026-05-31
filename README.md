# CyberCafe ERP - Complete Business Management System

## Overview

CyberCafe ERP is a comprehensive, production-ready SaaS solution designed specifically for managing cyber cafes. It provides complete management of customers, services, payments, subscriptions, and analytics.

## Features

### Core Features
- 👥 **Customer Management** - Complete customer profiles with contact details and history
- 🔧 **Service Tracking** - Manage services from submission to completion
- 💰 **Payment Processing** - Record and track payments with multiple methods
- 📊 **Analytics & Reports** - Beautiful dashboards and revenue charts
- 🔐 **Secure Admin Panel** - Hidden admin system for administrators
- 📱 **Mobile Friendly** - Fully responsive design
- 🔔 **Notifications** - Real-time notifications system
- 📋 **Subscription Plans** - Flexible subscription management

### Tech Stack
- **Backend**: Python 3.12, Flask 3.x
- **Database**: PostgreSQL (Production), SQLite (Development)
- **ORM**: SQLAlchemy
- **Frontend**: Tailwind CSS, Chart.js
- **Deployment**: Render, Gunicorn, WhiteNoise
- **Authentication**: Flask-Login with password hashing

## Project Structure

```
cybercafe-erp/
├── app.py                  # Main application
├── config.py              # Configuration settings
├── extensions.py          # Flask extensions
├── requirements.txt       # Python dependencies
├── Procfile              # Render deployment config
├── render.yaml           # Render configuration
├── .env.example          # Environment variables template
│
├── models/               # Database models
│   ├── user.py
│   ├── customer.py
│   ├── service.py
│   ├── payment.py
│   ├── subscription.py
│   └── notification.py
│
├── routes/               # API routes and blueprints
│   ├── auth.py          # Authentication routes
│   ├── dashboard.py     # Dashboard routes
│   ├── customer.py      # Customer management
│   ├── service.py       # Service management
│   └── admin.py         # Admin panel routes
│
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Homepage
│   ├── pricing.html     # Pricing page
│   ├── auth/            # Authentication templates
│   ├── dashboard/       # Dashboard templates
│   ├── customer/        # Customer templates
│   ├── service/         # Service templates
│   ├── admin/           # Admin templates
│   └── errors/          # Error templates
│
├── static/              # Static files
│   └── style.css        # Custom styles
│
├── uploads/             # File upload storage
└── migrations/          # Database migrations
```

## Installation & Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/pintusingh8155vk-creator/csc-website.git
   cd csc-website
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. **Run application**
   ```bash
   python app.py
   ```
   
   Application will be available at `http://localhost:5000`

## Deployment on Render

### One-Click Deployment

1. **Fork the repository** on GitHub

2. **Connect to Render**
   - Go to [render.com](https://render.com)
   - Connect your GitHub account
   - Create new Web Service
   - Select your repository

3. **Configure Environment**
   - Name: `cybercafe-erp`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Add environment variables from `.env`

4. **Add PostgreSQL Database**
   - Create new PostgreSQL database on Render
   - Copy connection string to `DATABASE_URL`

5. **Deploy**
   - Click Deploy
   - Wait for build and deployment to complete

## Database Models

### User
- `id`, `full_name`, `shop_name`, `mobile_number`, `email`
- `password_hash`, `district`, `address`
- `is_admin`, `is_active`, `created_at`, `updated_at`

### Customer
- `id`, `user_id`, `full_name`, `mobile_number`
- `aadhaar_last_4`, `address`, `village`, `notes`
- `created_at`, `updated_at`

### Service
- `id`, `customer_id`, `service_type`, `status`
- `amount`, `submission_date`, `completion_date`
- `notes`, `created_at`, `updated_at`

### Payment
- `id`, `user_id`, `service_id`, `amount`
- `payment_method`, `payment_status`, `transaction_id`
- `notes`, `created_at`, `updated_at`

### Subscription
- `id`, `user_id`, `plan_name`, `start_date`, `expiry_date`
- `is_active`, `created_at`, `updated_at`
- Plans: free, starter, professional, enterprise

### Notification
- `id`, `user_id`, `type`, `title`, `message`
- `is_read`, `created_at`

## Subscription Plans

| Plan | Price | Features |
|------|-------|----------|
| Free | ₹0 | 5 Customers, Basic Dashboard, Email Support |
| Starter | ₹499/mo | Unlimited Customers, Advanced Reports, Priority Support |
| Professional | ₹999/mo | All Starter + Payment Processing, API Access |
| Enterprise | ₹2999/mo | All Features, Dedicated Support, Custom Integration |

## Admin Panel

### Secure Access
- URL: `/secure-admin-panel-login`
- No public link in navbar
- Email and password authentication
- Admin-only features

### Admin Features
- View all users and their statistics
- Manage user status (active/inactive)
- View subscription breakdown
- Monitor system usage
- User account management

## Security Features

✅ Password hashing with Werkzeug
✅ CSRF protection on all forms
✅ Session management with Flask-Login
✅ SQL injection prevention with SQLAlchemy ORM
✅ Rate limiting ready (can be added)
✅ Secure cookies (HTTPS in production)
✅ Data validation on all inputs

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/logout` - User logout
- `GET /auth/profile` - View profile
- `POST /auth/profile` - Update profile

### Dashboard
- `GET /dashboard/` - Main dashboard
- `GET /dashboard/api/chart-data` - Chart data

### Customers
- `GET /customers/` - List customers
- `POST /customers/create` - Create customer
- `GET /customers/<id>` - View customer
- `POST /customers/<id>` - Update customer
- `POST /customers/<id>/delete` - Delete customer
- `GET /customers/api/search` - Search customers

### Services
- `GET /services/` - List services
- `POST /services/create` - Create service
- `GET /services/<id>` - View service
- `POST /services/<id>` - Update service
- `POST /services/<id>/delete` - Delete service
- `POST /services/<id>/payment` - Record payment

## Environment Variables

```
FLASK_ENV=production
FLASK_APP=app.py
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@host:5432/dbname
ADMIN_SECRET_KEY=admin-secret-key
```

## Development

### Running Tests
```bash
pytest
```

### Database Migrations
```bash
# Create migration
flask db migrate -m "Description"

# Apply migrations
flask db upgrade
```

### Creating Admin User
```python
from app import app
from extensions import db
from models.user import User

with app.app_context():
    admin = User(
        full_name="Admin User",
        shop_name="admin_shop",
        mobile_number="9999999999",
        email="admin@example.com",
        is_admin=True,
        is_active=True
    )
    admin.set_password("admin_password")
    db.session.add(admin)
    db.session.commit()
```

## Troubleshooting

### Database Connection Issues
- Check DATABASE_URL format
- Verify PostgreSQL is running
- Check credentials

### Static Files Not Loading
- Run `python app.py` in production mode
- Check WhiteNoise configuration
- Verify static folder exists

### Login Issues
- Clear browser cookies
- Check email/password
- Verify database connection

## Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - See LICENSE file for details

## Support

For support, email support@cybercafeerp.com or contact us through the website.

## Changelog

### Version 1.0.0 (Initial Release)
- ✅ Complete customer management
- ✅ Service tracking system
- ✅ Payment processing
- ✅ Subscription management
- ✅ Analytics dashboard
- ✅ Admin panel
- ✅ Mobile responsive design
- ✅ Production ready deployment
