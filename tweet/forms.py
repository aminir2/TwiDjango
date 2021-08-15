from django import forms
from .models import Tweet, Retweet, Mention

LANGUAGE_CHOICES = [('en', 'English'),
                    ('fa', 'Persian'),
                    ('de', 'Deutsch'),
                    ('ar', 'Arabic')
                    ]


class TweetForm(forms.ModelForm):
    tweet = forms.CharField(max_length=280, required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))
    tweet_photo = forms.ImageField(required=False)

    class Meta:
        model = Tweet
        fields = ['tweet', 'tweet_photo']


class RetweetForm(forms.ModelForm):
    query = forms.CharField(max_length=400, min_length=3,
                            widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    count = forms.CharField(max_length=5, min_length=1,
                            widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    sleep_time = forms.CharField(max_length=5, min_length=1,
                                 widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    lang = forms.CharField(max_length=5, min_length=1,
                           widget=forms.Select(choices=LANGUAGE_CHOICES))

    class Meta:
        model = Retweet
        fields = ['query', 'count', 'sleep_time']


class MentionForm(forms.ModelForm):
    query = forms.CharField(max_length=400, min_length=3,
                            widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    mention = forms.CharField(max_length=280, min_length=2,
                              widget=forms.Textarea(attrs={'type': 'text', 'class': 'form-control'}))
    count = forms.CharField(max_length=5, min_length=1,
                            widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    sleep_time = forms.CharField(max_length=5, min_length=1,
                                 widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    lang = forms.CharField(max_length=5, min_length=1,
                           widget=forms.Select(choices=LANGUAGE_CHOICES))

    class Meta:
        model = Mention
        fields = ['query', 'mention', 'query', 'sleep_time', 'lang']
