from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatar/', null=True,
                               default='https://www.pphfoundation.ca/wp-content/uploads/2018/05/default-avatar.png')
    consumer_key = models.CharField(max_length=60)
    consumer_secret = models.CharField(max_length=60)
    access_token = models.CharField(max_length=60)
    access_token_secret = models.CharField(max_length=60)
