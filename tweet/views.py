from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic import UpdateView, CreateView, FormView, TemplateView, DetailView
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
import tweepy
from .forms import *
from .models import Home
from bs4 import BeautifulSoup
import cloudinary
from cloudinary.uploader import upload
import tempfile
from django.conf import settings
from django.core.files import File
from django.test import TestCase
import storages
from time import sleep
import requests
import os
import asyncio
from django.utils.decorators import classonlymethod


# first page will be display on site
class Index(DetailView):
    model = Home
    template_name = 'index.html'

    # get objects from model
    def get_object(self):
        home = Home.objects.first()
        return home


# successfully page
class Done(TemplateView):
    template_name = 'done.html'


def tweepy_authenticate(consumer_key, consumer_secret, access_token, access_token_secret):
    global api
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)


# the class which is working for sending tweet on twitter
class Tweety(FormView):
    form_class = TweetForm
    template_name = 'tweet.html'
    success_url = reverse_lazy('tweet:done')

    # get the information from form in our template
    def form_valid(self, form):
        cloudinary.config(
            cloud_name="aminsaberi",
            api_key="127435522261298",
            api_secret="VtYO5terAwp8Q_Y2LEZ1WQLqnF4"
        )
        try:
            # Authenticate The user in the twitter api
            user = self.request.user
            tweepy_authenticate(user.consumer_key, user.consumer_secret, user.access_token, user.access_token_secret)
            # getting information from form
            tweet = form.cleaned_data.get('tweet')
            photo = form.cleaned_data.get('tweet_photo')
            clean_text = BeautifulSoup(tweet, "lxml").text
            # the functions of sending tweet
            if photo:
                tweet_photo = cloudinary.uploader.upload(photo, public_id=clean_text)
                media = tweet_photo['url']
                print(media)
                filename = clean_text
                request = requests.get(media, stream=True)
                if request.status_code == 200:
                    with open(filename, 'wb') as image:
                        for chunk in request:
                            image.write(chunk)
                    api.update_with_media(filename, status=clean_text)
                    os.remove(filename)
                else:
                    print("Unable to download image")
            else:
                api.update_status(status=clean_text)
        # handle the error if we get it from tweepy
        except tweepy.TweepError as e:
            t = loader.get_template('tweepy_error.html')
            c = {'e': e}
            return HttpResponse(t.render(c, self.request))
        return super(Tweety, self).form_valid(form)


# the class which is working for retweeting on twitter
class Retweet(FormView):
    form_class = RetweetForm
    template_name = 'retweet.html'
    success_url = reverse_lazy('tweet:done')

    # get the information from form in our template
    def form_valid(self, form):
        try:
            # Authenticate The user in the twitter api
            user = self.request.user
            tweepy_authenticate(user.consumer_key, user.consumer_secret, user.access_token, user.access_token_secret)
            # getting information from form
            query = form.cleaned_data.get('query')
            count = form.cleaned_data.get('count')
            time = form.cleaned_data.get('sleep_time')
            lang = form.cleaned_data.get('lang')
            # cleaning our getting information by using bs4
            clean_text = BeautifulSoup(query, "lxml").text
            clean_count = BeautifulSoup(count, 'lxml').text
            sleep_time = BeautifulSoup(time, 'lxml').text
            clean_lang = BeautifulSoup(lang, 'lxml').text
            # the functions of auto retweet
            for tweet in tweepy.Cursor(api.search, q=(clean_text) + " -filter:mentions", count=clean_count,
                                       lang=clean_lang).items(
                int(clean_count)):
                tweet.retweet()
                id = tweet._json['id']
                api.create_favorite(id)
                sleep(int(sleep_time))
        # handle the error if we get it from tweepy
        except tweepy.TweepError as e:
            t = loader.get_template('tweepy_error.html')
            c = {'e': e}
            return HttpResponse(t.render(c, self.request))
        return super(Retweet, self).form_valid(form)


class Mention(FormView):
    template_name = 'mention.html'
    form_class = MentionForm
    success_url = reverse_lazy('tweet:done')

    def form_valid(self, form):
        try:
            # Authenticate The user in the twitter api
            user = self.request.user
            tweepy_authenticate(user.consumer_key, user.consumer_secret, user.access_token, user.access_token_secret)
            # getting information from form
            query = form.cleaned_data.get('query')
            count = form.cleaned_data.get('count')
            time = form.cleaned_data.get('sleep_time')
            text = form.cleaned_data.get('mention')
            lang = form.cleaned_data.get('lang')
            # cleaning our getting information by using bs4
            clean_count = BeautifulSoup(count, 'lxml').text
            sleep_time = BeautifulSoup(time, 'lxml').text
            mention = BeautifulSoup(text, 'lxml').text
            clean_query = BeautifulSoup(query, "lxml").text
            clean_lang = BeautifulSoup(lang, 'lxml').text
            # the functions of auto mention
            for tweet in tweepy.Cursor(api.search, q=(clean_query) + "-filter:restricted", count=int(clean_count),
                                       lang=clean_lang).items(
                int(clean_count)):
                id = tweet._json['id']
                api.update_status(mention, in_reply_to_status_id=id, auto_populate_reply_metadata=True)
                sleep(int(sleep_time))
        # handle the error if we get it from tweepy
        except tweepy.TweepError as e:
            t = loader.get_template('tweepy_error.html')
            c = {'e': e}
            return HttpResponse(t.render(c, self.request))

        return super(Mention, self).form_valid(form)
