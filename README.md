# Longevity Backend Intern Test Task

##Run the project:


1. Install python dependencies

```
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory and paste the following:

```
# Email Config
export EMAIL_HOST = YOUR_EMAIL_HOSTNAME
export EMAIL_HOST_USER = YOUR_EMAIL_USERNAME
export EMAIL_HOST_PASSWORD = YOUR_EMAIL_PASSWORD

# DB Config
export DATABASE_NAME = YOUR_DB_NAME
export DATABASE_USER = YOUR_DB_USERNAME
export DATABASE_PASSWORD = YOUR_DB_PASSWORD
export DATABASE_HOST = 	YOUR_DB_HOST

# Redis Sever URL
export REDIS_SEVER_URL = YOUR_REDIS_OR_RABBITMQ_SERVER

# Django SECRET_KEY
export SECRET_KEY = GENERATE_A_DJANGO_SECRET_KEY

``` 

3. Run the migrations:

```
python manage.py makemigrations
```

4. Migrate the changes to the DB:

```
python manage.py migrate
```

5. Create a superuser for the project
```
python manage.py createsuperuser
```

6. Start the celery:

```
celery -A longevity worker --loglevel=info
```

7. Start the django server [use ngnix/gunicorn for production]

```
python manage.py runserver
```
