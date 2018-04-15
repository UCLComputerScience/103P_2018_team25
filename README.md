# IXN Matching Application
Applied Software Development application by team 25. The purpose of the project is to match students and their interests to potential client projects. This file describes the setup required for a local development server, and should not be used to deploy to a server.

## Development Setup
1. Clone this repository with: `git clone git@github.com:UCLComputerScience/103P_2018_team25.git`
2. Install prerequisites
3. Follow the MySQL database setup
4. Follow the environment variables setup
5. Make the relevant migrations with: `python3 manage.py makemigrations`
6. Apply the relevant migrations with: `python3 manage.py migrate`
7. Collect static files with : `python3 manage.py collectstatic`
8. Run the Django server with: `python3 manage.py runserver`
9. Load the site at: `127.0.0.1:8000`
10. Create a superuser to access admin page at `127.0.0.1:8000/admin`

## Prerequisites
```
Django 1.11.10
MySQL Server
mysqlclient 1.3.12 (Python module)
requests (Python module)
python-decouple (Python module)
django-tables2 (Python module)
tablib 0.11.4 (Python module)
```

## MySQL Database Setup
```
NAME: matching_db (create an empty database)
USER: matching_db_user (create this user and grant all privileges)
PASSWORD: matching_db_password
```

## Environment Variables
These variables will need to be placed in a .env file in the local repository
```
DEBUG=True
SECRET_KEY=(Generate a Django secret key)
DATABASE_NAME=matching_db
DATABASE_USER=matching_db_user
DATABASE_PASSWORD=matching_db_password
DATABASE_HOST=localhost
DATABASE_PORT=0
ALLOWED_HOSTS=.127.0.0.1
SECURE_SSL_REDIRECT=False
CSRF_COOKIE_SECURE=False
SESSION_COOKIE_SECURE=False
X_FRAME_OPTIONS=DENY
SECURE_BROWSER_XSS_FILTER=False
UCL_API_CLIENT_ID=(Sign up to UCL API for these)
UCL_API_CLIENT_SECRET=(Sign up to UCL API for these)
```
