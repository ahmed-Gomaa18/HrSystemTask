
# HR Management system Task

The goal of this task is tracking the employee's attendance.


## The Database used

The main database I used is ***PostgresQL*** but to the test I used is ***Sqlite3***
Can use PostgresQL by first uncomment then filling in these database settings in settings.py 
and make comment to sqlite3 configuration  

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'Enter your database name',
        'USER': 'Enter your user',
        'PASSWORD': 'Enter your password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

Then run the following set of commands

```bash
python manage.py makemigrations

python manage.py migrate

python manage.py runserver
```

Then open admin page by `http://127.0.0.1:8000/admin/` username:admin & password:admin
And create two objects ***admin & employee*** in Group Model and after create employee 
you can division users to admins and employees by groups attrpute in user object  

>OR use Default sqlite3


## The Database used

```bash
$ pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py runserver
```


## Configurations needed to run the code.

>Run the following set of commands to install all packages

```bash
pip install -r requirements.txt
```


## How to run the code

>Run the following set of commands

```bash
python manage.py makemigrations

python manage.py migrate

python manage.py runserver
```


## Summary 

```
I completed this task by Web framework Django, Django rest framework and signals behind As expected, the outputs of this program will be API.
 I used Postman to test all urls and functions alot of error cases However the project worked fine.
```


## Main Functions

1. register()
    - create users

2. login()
    - login user and create Token
        - Not: Token put in header like Key:Authorization value:Token 7c906c7bd73a1eec8..... 

3. logout()
    - remove Token

4. get_user()
    - get object user & user role by Token 

5. Check_in()
    - add check-in and create attendance record

6. check_out()
    - add check-out, worke_hours, total_over_time

7. Check_in_again()
    - add another check-in on the same attendance record

8. Check_out_again()
    - add another check-out on the same attendance record

9. list_attendance()
    - get all complete attendance for specific employee

10. list_attendance_all()
    - get all complete attendance with all employees But this function for admain only  

