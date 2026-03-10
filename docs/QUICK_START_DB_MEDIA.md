# 🚀 Quick Start: MySQL & Media Files

## TL;DR - Fast Setup Guide

### Prerequisites
- ✅ MySQL Server installed
- ✅ mysqlclient Python package installed (already done)

---

## 🗄️ MySQL Setup (5 Steps)

### 1. Create Database
```bash
mysql -u root -p
```
```sql
CREATE DATABASE matrimonial_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 2. Create .env File
```bash
cd d:\Matrimonial_Site\backend
copy .env.example .env
```

### 3. Edit .env (Add Your MySQL Password)
```env
DB_NAME=matrimonial_db
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD_HERE
DB_HOST=localhost
DB_PORT=3306
```

### 4. Run Migrations
```bash
.\venv\Scripts\python.exe manage.py makemigrations
.\venv\Scripts\python.exe manage.py migrate
```

### 5. Create Superuser
```bash
.\venv\Scripts\python.exe manage.py createsuperuser
```

**Done! MySQL is configured.** ✅

---

## 📸 Media Files Setup (Already Done!)

✅ **MEDIA_URL** = `/media/`  
✅ **MEDIA_ROOT** = `d:\Matrimonial_Site\backend\media`  
✅ **Directories Created:**
   - `media/profile_photos/`
   - `media/documents/`

---

## 🧪 Test Configuration

### Test MySQL Connection:
```bash
.\venv\Scripts\python.exe manage.py check --database default
```

### Test Media Files:
```bash
dir media
dir media\profile_photos
dir media\documents
```

---

## 📋 Current Configuration

| Setting | Value |
|---------|-------|
| **Database** | MySQL (django.db.backends.mysql) |
| **DB Name** | matrimonial_db |
| **DB User** | root (default) |
| **DB Host** | localhost |
| **DB Port** | 3306 |
| **Media URL** | /media/ |
| **Media Root** | backend/media |

---

## 🆘 Troubleshooting

### "Can't connect to MySQL server"
**Fix:** Start MySQL service
```powershell
Start-Service -Name MySQL80
```

### "Access denied for user 'root'"
**Fix:** Check password in `.env` file

### "Unknown database"
**Fix:** Create database (see step 1 above)

---

## 📚 Full Documentation

- **MySQL Guide**: `MYSQL_CONFIGURATION.md`
- **Media Files Guide**: `MEDIA_FILES_CONFIGURATION.md`
- **Complete Summary**: `DATABASE_MEDIA_SUMMARY.md`

---

## ✅ Status: Ready to Use!

All configurations are complete. Just follow the 5 steps above to activate MySQL!
