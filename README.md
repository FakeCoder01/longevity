create an Account Model in django that allows CRUD using REST framework where the email is the unique identifier and password should be stored securely by hashing it using a Django hashing algorithm (e.g., Argon). The login can be done by using the email and password or email and email otp. The otp should have an expiration time of 15 minutes and use celery to send the email otp. The login should be using JWT authentication. Write the serializers, views, models and everything.


The endpoints should look like this:

/api/users/
POST : email, password (Creates a new user)
GET : returns all users

/api/users/<user_id>/
PUT : update the user
GET : get the user data
DELETE : delete the user


LOGINS:
/api/login/
POST : email and password, performs the login

/api/login/email/
POST : emails the user the otp for login

/api/login/verify/
POST : matches the otp and performs the login