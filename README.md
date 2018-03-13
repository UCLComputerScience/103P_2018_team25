# IXN Matching Application
Applied Software Development application by team 25. The purpose of the project is to match students and their interests to potential client projects.

## Prerequisites
```
Django 1.11.10
MySQL Server
mysqlclient 1.3.12 (Python module)
requests (Python module)
```

## MySQL Database Setup
```
NAME: matching_db
USER: matching_db_user (grant all privileges)
PASSWORD: matching_db_password
HOST: 
PORT: 
```

## Development Setup
1. Clone this repository with: `git clone git@github.com:UCLComputerScience/103P_2018_team25.git`
2. Install prerequisites
3. Enter the Django project with: `cd ixn`
4. Run the Django server with: `python3 manage.py runserver`
5. Load the site at: http://localhost:8000
6. Add `/matchingsystem` to the URL to enter the matching system pages
7. Create a superuser to access admin page at `/admin`
