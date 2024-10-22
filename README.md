# Theatre API Service

The Theatre API Service is designed to facilitate ticket reservations and management for theatre performances. 
The project provides a comprehensive backend system using Django, 
offering RESTful API endpoints to handle various operations related to theatre management

## Run service on your machine

### 1. Clone repository
```bash
git clone https://github.com/Maksym-Turenko/Theatre-API-Service.git
```
### 2. Create .vevn

```bash
python -m venv .venv
```

### 3. Activate .venv

#### Windows
```bash
.\.venv\Scripts\activate
```
#### Unix
```bash
source venv/bin/activate
```

### 4. Install requirements.txt 

```bash
pip insatll -r requirements.txt
```

### 5. Do migrations

```bash
python manage.py migrate
```

### 6. Pull docker image from Docker hub

```bash
docker pull varicella/theatre-api-service
```

### 7. Start your docker image 

```bash
docker-compose up --build
```

### 8. Enter this URL to connect to API service

http://localhost:8000/api/v1


## Project structure

```plaintext
Project
 └── config
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    ├── __init__.py
    theatre
    ├── admin.py
    ├── apps.py
    ├── custom_mixins.py
    ├── models.py
    ├── permissions.py
    ├── serializers.py
    ├── urls.py
    ├── views.py
    ├── __init__.py
    └── management
        ├── __init__.py
        └── commands
            ├── wait_for_db.py
            ├── __init__.py
        tests
        ├── test_admin.py
        ├── test_models.py
        ├── test_serializers.py
        ├── test_views.py
        ├── __init__.py
    user_config
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── tests.py
    ├── urls.py
    ├── views.py
    ├── __init__.py
```

## Features
- JWT Authentication
- Admin panel `/admin/`
- Swagger documentation
- Managing performance and tickets
- Creating orders and tickets
- Creating plays

## Hint
### To see all endpoints enter this URL: http://localhost:8000/api/doc/swagger/
