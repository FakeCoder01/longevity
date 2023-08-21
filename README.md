# Longevity Backend Intern Test Task

### Live API : <a href="https://longevityapi.pythonanywhere.com">https://longevityapi.pythonanywhere.com</a>


## Run the project:


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

#### Notes
** Make sure to run `python manage.py collectstatic` for static files generation  **


## API Reference

## Responses
| Response Code | Type     | Description                |
| :-------- | :------- | :------------------------- |
| **200 OK** | Success | Request was succesfull |
| **201 CREATED** | Success  | Request was fullfilled & user has been created |
| **204 NO_CONTENT** | Success | Request was deleted |
| **400 BAD_REQ** | Failed | Request was unsuccesfull (check params) |
| **403 FORBIDEN** | Failed | Auth unable (check Authorization Header) |
| **404 NOT FOUND** | Failed | User not found (check id/email) |
| **500 ERROR** | Failed | Server Error (check config/log) |



#### Login by password

```http
  POST /api/auth/login/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `email` | body `string` | **Required**. Your Email address |
| `password` | body `password` | **Required**. Your password |


#### Login by Email and OTP

-  First step : send the email and an OTP will be sent

```http
  POST /api/auth/login/email/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `email` | body `string` | **Required**. Your Email address |

- Second step : send the email and the otp from the email

```http
  POST /api/auth/login/verify/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `email` | body `string` | **Required**. The previous email |
| `otp` | body `string` | **Required**. OTP from the email |


#### Create a new user

```http
  POST /api/users/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization` | Headers `Bearer <access_token>` | **Required**. Your Access Token |
| `email` | body `string` | **Required**. Unique Email address |
| `password` | body `string` | **Required**. Password |
| `full_name` | body `string` |  Full  name |


#### Get all users

```http
  GET /api/users/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | Headers `Bearer <access_token>` | **Required**. Your Access Token |

#### Get one user

```http
  GET /api/users/${id}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization` | Headers `Bearer <access_token>` | **Required**. Your Access Token |
| `id`      | `string` | **Required**. Id of the user to fetch |


#### Update one user

```http
  PUT /api/users/${id}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization` | Headers `Bearer <access_token>` | **Required**. Your Access Token |
| `id`      | `string` | **Required**. Id of the user to update |
| `email` | body `string` | New unique Email address |
| `full_name` | body `string` | New full  name |


#### Delete one user

```http
  DELETE /api/users/${id}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization` | Headers `Bearer <access_token>` | **Required**. Your Access Token |
| `id`      | `string` | **Required**. Id of the user to delete |


### Get a new ACCESS_TOKEN

```http
  POST /api/auth/token/refresh/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization` | Headers `Bearer <access_token>` | **Required**. Your Access Token |
| `refresh`      | `string` | **Required**. Your refresh_token |


### Logout / Delete tokens

```http
  POST /api/auth/token/refresh/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization` | Headers `Bearer <access_token>` | **Required**. Your Access Token |
| `refresh`      | `string` | **Required**. Your refresh_token |

