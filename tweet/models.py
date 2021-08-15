import datetime
import time
from django.utils import timezone

from django.db import models


class Home(models.Model):
    photo = models.ImageField(upload_to='bg/')
    title = models.CharField(max_length=25)
    avatar = models.ImageField(upload_to='avatar/')
    name = models.CharField(max_length=20)
    date = models.DateTimeField(default=timezone.now())
    description = models.TextField(max_length=500)
    twitter = models.URLField(max_length=200)


# Create your models here.
class Tweet(models.Model):
    tweet = models.TextField(max_length=280)
    tweet_photo = models.ImageField(blank=True, upload_to='')


class Retweet(models.Model):
    query = models.CharField(max_length=400, blank=False)
    count = models.CharField(max_length=5, default=1)
    sleep = models.CharField(max_length=5, default=1)


class Mention(models.Model):
    query = models.CharField(max_length=400, blank=False)
    count = models.CharField(max_length=5, default=1)
    sleep = models.CharField(max_length=5, default=1)
    mention = models.TextField(max_length=280)
