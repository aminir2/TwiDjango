## Project Summary

This Website trying to make easy managing twitter bot for their managers,It's a demo version of this site which can
tweet ,auto retweet and also auto mention but many feature will be added in future upadtes:)

![alt text](https://wallpaperaccess.com/full/1459045.jpg "Logo")

---

## Running this project

To get this project up and running you should start by having Python installed on your computer. It's advised you create
a virtual environment to store your projects dependencies separately. You can install virtualenv with

```
pip install virtualenv
```

Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) or windows terminal,
run the following command in the base directory of this project

```
virtualenv env
```

That will create a new folder `env` in your project directory. Next activate it with this command on mac/linux:

```
source env/bin/active
```

Then install the project dependencies with

```
pip install -r requirements.txt
```

Then collect the static of the project

```
python manage.py collectstatic
```

Then if You want to use send email function too you should set your email in .env-sample

```
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'sample'
EMAIL_HOST_PASSWORD = 'sample'
EMAIL_PORT = 587
SECRET_KEY = 'sample'
```

Then you should run this command in your commandline

```
pyhton manage.py makemigrations
python migrate
```

After All of this you want a superuser so run this command

```
python manage.py createsuperuser
```

Now you can run the project with this command

```
python manage.py runserver
```








