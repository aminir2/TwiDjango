from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from .forms import SignupForm, ProfileForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .models import User
from django.core.mail import EmailMessage
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


# register View
class Register(CreateView):
    form_class = SignupForm
    template_name = 'register.html'

    # get the information form form
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        # sending email verification
        mail_subject = 'Activate your blog account.'
        message = render_to_string('emailConfirmation.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return render(self.request, 'ConfirmEmail.html', {'user': user})


# checking for user has verified his/her account or not
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/register_done.html')
    else:
        return render(request, 'registration/invalid_link.html')


# login view
class Login(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            return reverse_lazy("account:profile")
        else:
            return reverse_lazy('account:login')


class MainProfile(LoginRequiredMixin, TemplateView):
    template_name = 'registration/home.html'


# the view that user can change some of his/her information
class UserProfile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy("account:profile")

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(UserProfile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs
