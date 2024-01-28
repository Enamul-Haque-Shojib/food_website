from django.shortcuts import render
from . import forms

from django.views.generic import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib import messages


class UserRegistrationView(FormView):
    template_name = 'registration.html'
    form_class = forms.UserRegistrationForm
    success_url = reverse_lazy('register')
    def form_valid(self, form):
        user = form.save()
        print(user)
        token = default_token_generator.make_token(user)
        # print("token: ",token)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        # print('uid: ', uid)
        confirm_link = f"http://127.0.0.1:8000/author/active/{uid}/{token}"
        email_subject = 'Confirm Your Email'
        email_body = render_to_string("confirm_email.html", {'confirm_link':confirm_link})
        email = EmailMultiAlternatives(email_subject, '', to=[user.email])
        email.attach_alternative(email_body, 'text/html')
        email.send()
            
        messages.warning(self.request, 'Check your email address')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Sign Up'
        return context 
            
    
    
def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')
    

class UserLoginView(LoginView):
    template_name = 'registration.html'


    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context

    

class UserLogoutView(LogoutView):
     def get_success_url(self):
        messages.success(self.request, 'Logged out successfully')
        return reverse_lazy('home')
     

class ProfileView(TemplateView):
    template_name = 'profile.html'
    

