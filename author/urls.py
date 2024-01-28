
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views




urlpatterns = [
    
    path('register/', views.UserRegistrationView.as_view(), name = 'register'),
    path('login/', views.UserLoginView.as_view(), name = 'login'),
    path('logout/', views.UserLogoutView.as_view(), name = 'logout'),
    path('active/<uid64>/<token>', views.activate, name = 'activate'),
    path('profile/', views.ProfileView.as_view(), name = 'profile'),

    path('passwordreset/', auth_views.PasswordResetView.as_view(template_name="password_reset_form.html"), name = 'password_reset'),
    path('passwordresetdone/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name = 'password_reset_done'),
    path('passwordresetconfirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name = 'password_reset_confirm'),
    path('passwordresetcomplete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name = 'password_reset_complete'),
]