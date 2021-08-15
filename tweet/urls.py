from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "tweet"
urlpatterns = [
    path('account/tweet', Tweety.as_view(), name='tweet'),
    path('done/', Done.as_view(), name='done'),
    path('', Index.as_view(), name='home'),
    path('account/retweet', Retweet.as_view(), name='retweet'),
    path('account/mention', Mention.as_view(), name='mention'),
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
