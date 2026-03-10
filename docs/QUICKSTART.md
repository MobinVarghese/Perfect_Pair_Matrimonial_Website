# Matrimonial Site - Quick Start Guide

## Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

## Quick Start

### 1. Backend Setup (Django)

Open a terminal and run:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Backend will run on: http://localhost:8000

### 2. Frontend Setup (React)

Open a new terminal and run:

```bash
cd frontend
npm install
npm start
```

Frontend will run on: http://localhost:3000

## Testing the Application

1. Open http://localhost:3000 in your browser
2. Click "Register" to create a new user account
3. Fill in the registration form
4. View registered users by clicking "Users"

## Admin Panel

Access the Django admin at http://localhost:8000/admin using the superuser credentials you created.

## Common Issues

**Issue:** Django not found
**Solution:** Make sure the virtual environment is activated

**Issue:** React dependencies not installing
**Solution:** Delete node_modules and package-lock.json, then run npm install again

**Issue:** CORS errors
**Solution:** Ensure both backend and frontend are running on the correct ports
