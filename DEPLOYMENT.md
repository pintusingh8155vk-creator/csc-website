# CyberCafe ERP - Deployment & Setup Guide

## ✅ Project Complete and Ready to Deploy

Your complete, fully functional **Cyber Cafe ERP** system is now ready for deployment on Render. All features have been implemented exactly as per your requirements.

---

## 📋 What's Included

### Core Features ✓
- ✅ Complete User Management (Registration, Login, Profile)
- ✅ Customer Management System (CRUD operations)
- ✅ Service Tracking & Management
- ✅ Payment Processing & Recording
- ✅ Subscription Management (4 Plans: Free, Starter, Professional, Enterprise)
- ✅ Dashboard with Analytics
- ✅ Hidden Admin Panel (`/secure-admin-panel-login`)
- ✅ Notification System
- ✅ Responsive Mobile Design

### Technical Stack ✓
- Python 3.12 with Flask 3.x
- PostgreSQL (Production) / SQLite (Development)
- SQLAlchemy ORM
- Flask-Login for authentication
- Tailwind CSS for styling
- Chart.js for analytics
- WhiteNoise for static files
- Gunicorn for WSGI server

### Database Models ✓
- User (with password hashing)
- Customer (with Aadhaar support)
- Service (with status tracking)
- Payment (with multiple methods)
- Subscription (with 4 tiers)
- Notification

### Endpoints ✓
All CRUD operations for:
- Authentication (`/auth/*`)
- Dashboard (`/dashboard/*`)
- Customers (`/customers/*`)
- Services (`/services/*`)
- Admin Panel (`/secure-admin-panel/*`)

---

## 🚀 One-Click Deployment on Render

### Step 1: Prepare Your GitHub Repository ✓
Repository is already set up at: `https://github.com/pintusingh8155vk-creator/csc-website`

All files are committed and ready:
- Backend code (Python/Flask)
- Frontend templates (HTML/Tailwind CSS)
- Database models
- Configuration files
- Dependencies (requirements.txt)

### Step 2: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub account
3. Authorize Render to access your GitHub

### Step 3: Create Web Service on Render
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `csc-website`
3. Fill in the details:
   - **Name**: `cybercafe-erp`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free (or upgrade to paid for production)

### Step 4: Add Environment Variables
Add these to Render dashboard:
```
FLASK_ENV=production
SECRET_KEY=generate-secure-random-key
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Step 5: Add PostgreSQL Database
1. Click **"New +"** → **"PostgreSQL"**
2. Create new database with these details:
   - **Name**: `cybercafe-erp-db`
   - **Plan**: Free (or paid)
3. Copy the connection string to `DATABASE_URL`

### Step 6: Deploy
1. Render will automatically build and deploy
2. Your app will be live at: `https://cybercafe-erp.onrender.com`
3. Check logs for any issues

---

## 🔐 Security Features Implemented

✓ **Password Hashing**: Werkzeug security for passwords
✓ **CSRF Protection**: Flask-WTF forms protection
✓ **Session Management**: Secure session cookies
✓ **SQL Injection Prevention**: SQLAlchemy ORM parameterized queries
✓ **HTTPS**: Automatic on Render
✓ **Admin Secret**: Hidden admin panel (`/secure-admin-panel-login`)
✓ **Input Validation**: Email, mobile, Aadhaar validation
✓ **Role-Based Access**: User vs Admin permissions

---

## 📱 Application Structure

```
cybercafe-erp/
├── app.py                 # Main application
├── config.py             # Configuration
├── extensions.py         # Flask extensions
├── requirements.txt      # Dependencies
├── Procfile             # Render config
├── render.yaml          # Render deployment
├── .env.example         # Environment template
│
├── models/              # Database models
│   ├── user.py
│   ├── customer.py
│   ├── service.py
│   ├── payment.py
│   ├── subscription.py
│   └── notification.py
│
├── routes/              # API endpoints
│   ├── auth.py
│   ├── dashboard.py
│   ├── customer.py
│   ├── service.py
│   └── admin.py
│
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── pricing.html
│   ├── auth/
│   ├── dashboard/
│   ├── customer/
│   ├── service/
│   ├── admin/
│   ├── errors/
│   └── contact.html
│
├── static/              # CSS & JS
│   └── style.css
│
├── utils/               # Utilities
│   ├── validators.py
│   ├── decorators.py
│   └── __init__.py
│
└── uploads/             # User uploads
```

---

## 🎯 Key URLs

### Public Pages
- Home: `/`
- Pricing: `/pricing`
- About: `/about`
- Contact: `/contact`

### Authentication
- Register: `/auth/register`
- Login: `/auth/login`
- Logout: `/auth/logout`
- Profile: `/auth/profile`

### Dashboard
- Dashboard: `/dashboard/`
- Chart API: `/dashboard/api/chart-data`

### Customers
- List: `/customers/`
- Create: `/customers/create`
- View: `/customers/<id>`
- Delete: `/customers/<id>/delete`

### Services
- List: `/services/`
- Create: `/services/create`
- View: `/services/<id>`
- Record Payment: `/services/<id>/payment`

### Admin Panel (Hidden)
- Login: `/secure-admin-panel-login`
- Dashboard: `/secure-admin-panel-dashboard`
- Users: `/secure-admin-panel-users`
- Subscriptions: `/secure-admin-panel-subscriptions`

---

## 🛠 Local Development

### Setup Local Environment
```bash
# Clone repository
git clone https://github.com/pintusingh8155vk-creator/csc-website.git
cd csc-website

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Initialize database
flask db init
flask db migrate
flask db upgrade

# Run application
python app.py
```

Visit: `http://localhost:5000`

---

## 👤 Creating Admin User (Production)

```python
from app import app
from extensions import db
from models.user import User

with app.app_context():
    admin = User(
        full_name="Admin",
        shop_name="admin_shop",
        mobile_number="9999999999",
        email="admin@cybercafe.com",
        is_admin=True,
        is_active=True
    )
    admin.set_password("secure_password_here")
    db.session.add(admin)
    db.session.commit()
    print("Admin user created!")
```

---

## 📊 Database Schema

### Users Table
- id, full_name, shop_name, mobile_number, email
- password_hash, district, address
- is_admin, is_active, created_at, updated_at

### Customers Table
- id, user_id, full_name, mobile_number
- aadhaar_last_4, address, village, notes
- created_at, updated_at

### Services Table
- id, customer_id, service_type, status
- amount, submission_date, completion_date
- notes, created_at, updated_at

### Payments Table
- id, user_id, service_id, amount
- payment_method, payment_status, transaction_id
- notes, created_at, updated_at

### Subscriptions Table
- id, user_id, plan_name, start_date, expiry_date
- is_active, created_at, updated_at

### Notifications Table
- id, user_id, type, title, message
- is_read, created_at

---

## 💰 Subscription Plans

| Plan | Price | Features |
|------|-------|----------|
| **Free** | ₹0 | 5 Customers, Basic Dashboard |
| **Starter** | ₹499/mo | Unlimited Customers, Advanced Reports |
| **Professional** | ₹999/mo | + Payment Processing, API Access |
| **Enterprise** | ₹2999/mo | All + Dedicated Support |

---

## 🔧 Troubleshooting

### Database Connection Issues
```bash
# Check DATABASE_URL format
# Should be: postgresql://username:password@host:5432/dbname
```

### Static Files Not Loading
```bash
# Run with WhiteNoise enabled
python app.py
```

### Port Already in Use
```bash
# Use different port
python app.py --port 5001
```

### Login Not Working
- Clear browser cookies
- Check email/password credentials
- Verify database is running

---

## 📝 Notes

1. **Password Requirements**: Minimum 6 characters
2. **Mobile Format**: 10 digits, starts with 6-9
3. **Email Validation**: Standard email format
4. **Aadhaar**: Last 4 digits only stored
5. **Admin Access**: `/secure-admin-panel-login` (no navbar link)

---

## ✅ Deployment Checklist

- [ ] Repository pushed to GitHub
- [ ] All files committed and synced
- [ ] Render account created
- [ ] Web Service created on Render
- [ ] PostgreSQL database added
- [ ] Environment variables configured
- [ ] `SECRET_KEY` generated and set
- [ ] `DATABASE_URL` pointing to PostgreSQL
- [ ] Deployment triggered
- [ ] Application live at `https://your-app.onrender.com`
- [ ] Admin user created in production
- [ ] SSL certificate verified

---

## 🚀 Your Application is Ready!

Your **CyberCafe ERP** system is fully functional and ready for production deployment on Render. All features work as specified in your prompt.

**Next Steps:**
1. Go to [render.com](https://render.com)
2. Create Web Service from GitHub
3. Add PostgreSQL database
4. Set environment variables
5. Deploy!

For support or updates, check the repository at:
👉 `https://github.com/pintusingh8155vk-creator/csc-website`

---

**Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Last Updated**: May 31, 2026
