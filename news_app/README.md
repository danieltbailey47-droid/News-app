News App


## Description:
    A Django-based news platform where users can register as Readers, Journalists, or Editors, create and approve articles, subscribe to journalists or publishers, and access a RESTful API for approved articles.

## Features:
    - User registration and login with roles (Reader, Journalist, Editor)
    - Journalists can create articles and assign publishers
    - Editors can approve or decline articles
    - Readers can view articles and subscribe to journalists or publishers
    - REST API to fetch approved articles for third-party clients
    - Email notifications for approved articles
    - Responsive UI with a card-based layout

## Requirements
### Software
- Python 3.11+ (tested)
- pip
- MariaDB or MySQL
- Git

### Python Libraries
- Django 4.2+
- Django REST Framework
- mysqlclient
- requests

## Installation Guide:

### Step 1 — Clone the Repository:

    git clone <repo-url>
    cd news_app

### Step 2 — Create a Virtual Environment:

    python3 -m venv myenv

    Activate the environment:

    Mac / Linux

    source myenv/bin/activate

    Windows

    myenv\Scripts\activate

### Step 3 — Install Dependencies:

    If a requirements file exists:

    pip install -r requirements.txt

    If installing manually:

    pip install django

    pip install djangorestframework

    pip install mysqlclient

### Step 4 — Open the SQL Client:

    mysql -u root -p

    Enter your MySQL/MariaDB root password.

### Step 5 — Create the Database:

    Inside the SQL client run:

    CREATE DATABASE news_app_db;

### Step 6 — Create a Database User:

    CREATE USER 'news_user'@'localhost' IDENTIFIED BY 'yourpassword';

### Step 7 — Grant Database Permissions:

    GRANT ALL PRIVILEGES ON news_app_db.* TO 'news_user'@'localhost';
    FLUSH PRIVILEGES;

    Exit the SQL client:
    EXIT;

## Configure Django Database:

    Open:

    news_app/settings.py

    Update the database configuration:

    DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'news_app_db',
    'USER': 'news_user',
    'PASSWORD': 'yourpassword',
    'HOST': 'localhost',
    'PORT': '3306',
    }
    }

## Apply Database Migrations
    python manage.py migrate

## Create an Admin User:
    python manage.py createsuperuser

    Follow the prompts to create the administrator account.

## Running the Application:

    Start the development server:

    python manage.py runserver

    Open a browser and navigate to:

    http://127.0.0.1:8000/

## Running Unit Tests

    Run the project tests with:

    python3 manage.py test

## Project File Structure:
    news_app/
    ├── news/
    │   ├── migrations/
    │   ├── templates/
    │   │   ├── articles/
    │   │   │   ├── article_list.html
    │   │   │   ├── create_article.html
    │   │   │   ├── approve_articles.html
    │   │   │   ├── edit_article.html
    │   │   │   └── subscribed_articles.html
    │   │   ├── registration/
    │   │   │   ├── login.html
    │   │   │   ├── signup.html
    │   │   │   └── dashboard.html
    │   │   └── base.html
    │   │
    │   ├── static/
    │   │   └── css/style.css
    │   │
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── serializers.py
    │   └── tests.py
    │
    ├── manage.py
    ├── requirements.txt
    └── README.md

## Technologies Used:

    Backend:

        Django
        Django REST Framework

    Database:

        MariaDB / MySQL

    Frontend:

        HTML
        CSS

## Notes:

    Users must include an email address during registration to receive article notifications.
    Editors must approve articles before they appear publicly.
    Readers can subscribe to journalists or publishers to receive updates.
