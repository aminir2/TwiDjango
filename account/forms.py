from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django.core.exceptions import ValidationError


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'type': 'password', 'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("User Name already exists")
        return username

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)
        if not user.is_superuser:
            self.fields['username'].disabled = True
            self.fields['email'].disabled = True

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'consumer_key', 'consumer_secret', 'access_token',
                  'access_token_secret', 'avatar']
