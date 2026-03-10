# MySQL Database Configuration Guide

## Overview
The Django backend has been configured to use MySQL as the primary database. This guide will help you set up and configure MySQL for the Matrimonial Website.

---

## 📋 Database Settings in `settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'matrimonial_db'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

### Configuration Fields:
- **ENGINE**: `django.db.backends.mysql` - MySQL database adapter
- **NAME**: `matrimonial_db` - Database name (default)
- **USER**: `root` - MySQL username (default)
- **PASSWORD**: Empty string (default, set your password)
- **HOST**: `localhost` - Database server address
- **PORT**: `3306` - MySQL default port

---

## 🚀 Setup Instructions

### Step 1: Install MySQL Server
If you don't have MySQL installed:

**Windows:**
1. Download MySQL Installer from: https://dev.mysql.com/downloads/installer/
2. Run the installer and select "MySQL Server"
3. Set a root password during installation
4. Complete the installation

**Linux:**
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

**macOS:**
```bash
brew install mysql
brew services start mysql
```

---

### Step 2: Create the Database

1. **Login to MySQL:**
```bash
mysql -u root -p
```
Enter your MySQL root password when prompted.

2. **Create the database:**
```sql
CREATE DATABASE matrimonial_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. **Create a dedicated user (recommended for production):**
```sql
CREATE USER 'matrimonial_user'@'localhost' IDENTIFIED BY 'your_strong_password';
GRANT ALL PRIVILEGES ON matrimonial_db.* TO 'matrimonial_user'@'localhost';
FLUSH PRIVILEGES;
```

4. **Verify database creation:**
```sql
SHOW DATABASES;
USE matrimonial_db;
```

5. **Exit MySQL:**
```sql
EXIT;
```

---

### Step 3: Configure Environment Variables

1. **Create `.env` file** (copy from `.env.example`):
```bash
cd d:\Matrimonial_Site\backend
copy .env.example .env
```

2. **Edit `.env` file** with your MySQL credentials:
```env
DB_NAME=matrimonial_db
DB_USER=matrimonial_user
DB_PASSWORD=your_strong_password
DB_HOST=localhost
DB_PORT=3306
```

---

### Step 4: Install Python MySQL Client
Already installed! (`mysqlclient==2.2.7`)

If you need to reinstall:
```bash
.\venv\Scripts\pip.exe install mysqlclient
```

---

### Step 5: Run Django Migrations

1. **Make migrations:**
```bash
cd d:\Matrimonial_Site\backend
.\venv\Scripts\python.exe manage.py makemigrations
```

2. **Apply migrations:**
```bash
.\venv\Scripts\python.exe manage.py migrate
```

3. **Create superuser:**
```bash
.\venv\Scripts\python.exe manage.py createsuperuser
```

---

## 🔧 Troubleshooting

### Error: "Can't connect to MySQL server"
**Solution:**
1. Check if MySQL service is running
2. Verify HOST and PORT are correct
3. Ensure firewall allows connection to port 3306

**Windows - Check MySQL service:**
```powershell
Get-Service -Name MySQL*
```

**Start MySQL service:**
```powershell
Start-Service -Name MySQL80
```

### Error: "Access denied for user"
**Solution:**
1. Verify username and password in `.env`
2. Check user has proper privileges:
```sql
SHOW GRANTS FOR 'matrimonial_user'@'localhost';
```

### Error: "Unknown database"
**Solution:**
Create the database if it doesn't exist:
```sql
CREATE DATABASE matrimonial_db;
```

### Error: "No module named 'MySQLdb'"
**Solution:**
Install mysqlclient:
```bash
.\venv\Scripts\pip.exe install mysqlclient
```

---

## 📊 Database Schema

After running migrations, the following tables will be created:

### Core Django Tables:
- `auth_user` - User accounts
- `auth_group` - User groups
- `auth_permission` - Permissions
- `django_admin_log` - Admin actions log
- `django_content_type` - Content types
- `django_session` - User sessions

### Custom App Tables:
- `users_userprofile` - Extended user profiles
  - user_id (Foreign Key to auth_user)
  - phone_number
  - date_of_birth
  - gender
  - bio
  - created_at
  - updated_at

---

## 🔒 Security Best Practices

### 1. Use Environment Variables
Never hardcode credentials in `settings.py`. Always use environment variables:
```python
'PASSWORD': os.environ.get('DB_PASSWORD', ''),
```

### 2. Strong Passwords
Use strong passwords for MySQL users:
- Minimum 12 characters
- Mix of uppercase, lowercase, numbers, symbols

### 3. Dedicated Database User
Don't use `root` in production. Create a dedicated user with limited privileges.

### 4. Backup Regular
Set up automated database backups:
```bash
mysqldump -u root -p matrimonial_db > backup.sql
```

### 5. Enable SSL (Production)
For production, enable SSL connections:
```python
'OPTIONS': {
    'ssl': {
        'ca': '/path/to/ca-cert.pem',
    }
}
```

---

## 🔄 Switching Back to SQLite (Development)

If you want to use SQLite for development:

1. **Comment out MySQL configuration in `settings.py`:**
```python
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         ...
#     }
# }
```

2. **Uncomment SQLite configuration:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

## 📈 Database Management

### View All Tables
```sql
USE matrimonial_db;
SHOW TABLES;
```

### View Table Structure
```sql
DESCRIBE users_userprofile;
```

### View Data
```sql
SELECT * FROM auth_user;
SELECT * FROM users_userprofile;
```

### Database Size
```sql
SELECT 
    table_schema AS 'Database',
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)'
FROM information_schema.tables 
WHERE table_schema = 'matrimonial_db'
GROUP BY table_schema;
```

---

## ✅ Verification Checklist

- [ ] MySQL server is installed and running
- [ ] Database `matrimonial_db` is created
- [ ] Database user has proper privileges
- [ ] `.env` file is configured with correct credentials
- [ ] `mysqlclient` package is installed
- [ ] Migrations run successfully
- [ ] Django can connect to MySQL
- [ ] Superuser is created
- [ ] Admin panel is accessible

---

## 🎯 Quick Commands Reference

```bash
# Check MySQL version
mysql --version

# Login to MySQL
mysql -u root -p

# Create database
mysql -u root -p -e "CREATE DATABASE matrimonial_db;"

# Run migrations
.\venv\Scripts\python.exe manage.py migrate

# Create superuser
.\venv\Scripts\python.exe manage.py createsuperuser

# Start Django server
.\venv\Scripts\python.exe manage.py runserver
```

---

## 📞 Support

For MySQL-specific issues:
- MySQL Documentation: https://dev.mysql.com/doc/
- Django MySQL Notes: https://docs.djangoproject.com/en/4.2/ref/databases/#mysql-notes

For Django database configuration:
- Django Databases: https://docs.djangoproject.com/en/4.2/ref/databases/
