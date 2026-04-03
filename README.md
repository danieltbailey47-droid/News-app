# News App

## Description

A Django-based news platform where users can register as Readers, Journalists, or Editors, create and approve articles, subscribe to journalists or publishers, and access a RESTful API for approved articles.

---

## Features

* User registration and login with roles (Reader, Journalist, Editor)
* Automatic login after successful registration
* Form validation with user-friendly error messages (e.g., duplicate email)
* Journalists can create articles and assign publishers or submit independently
* Editors can approve or decline articles for publishers they are associated with
* Independent articles are automatically approved
* Readers can view articles and subscribe to journalists or publishers
* Publishers can be created and associated with journalists and editors
* REST API to fetch approved articles
* Email notifications for approved articles
* Responsive UI with a card-based layout

---

## Requirements

### Software

* Python 3.11+
* pip
* Git
* Docker (optional, for containerized setup)

### Python Libraries

All required libraries are listed in `requirements.txt`.

---

## Installation Guide (Local Setup)

### 1. Clone the Repository

```
git clone <repo-url>
cd news_app
```

### 2. Create and Activate a Virtual Environment

```
python3 -m venv venv
```

**Mac / Linux**

```
source venv/bin/activate
```

**Windows**

```
venv\Scripts\activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

## Environment Setup

This project uses environment variables for configuration.

### 1. Create a `.env` file

```
cp .env.example .env
```

### 2. Update values if needed

```
DATABASE_NAME=news_db
DATABASE_USER=newsuser
DATABASE_PASSWORD=newsapp123
DATABASE_HOST=localhost
DEBUG=True
```

---

## Database Setup (Local Only)

### 1. Open MySQL/MariaDB

```
mysql -u root -p
```

### 2. Create Database

```
CREATE DATABASE news_db;
```

### 3. Create User

```
CREATE USER 'newsuser'@'localhost' IDENTIFIED BY 'yourpassword';
```

### 4. Grant Permissions

```
GRANT ALL PRIVILEGES ON news_db.* TO 'newsuser'@'localhost';
FLUSH PRIVILEGES;
```

---

## Apply Migrations

```
python manage.py migrate
```

---

## Create Superuser

```
python manage.py createsuperuser
```

---

## Run the Application

```
python manage.py runserver
```

Open in browser:

```
http://127.0.0.1:8000/
```

---

## Running with Docker

### 1. Build and start containers

```
docker-compose up --build
```

### 2. Apply migrations (in a new terminal)

```
docker-compose exec web python manage.py migrate
```

### 3. Access the application

```
http://localhost:8000
```

### 4. Stop containers

```
docker-compose down
```

---

## Running Tests

```
python manage.py test
```

---

## Project Structure

```
news_app/
├── news/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│   └── tests.py
├── docs/
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .env.example
```

---

## Technologies Used

### Backend

* Django
* Django REST Framework

### Database

* MariaDB / MySQL

### Frontend

* HTML
* CSS

---

## Notes

* Users must include an email address during registration to receive notifications.
* Editors approve articles before publication unless the article is independent.
* Publishers manage associations with journalists and editors.
* Environment variables are required for configuration and should not be hardcoded.
* Sensitive data (e.g., passwords) should not be committed to version control.

---
