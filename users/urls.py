from django.urls import path
from . import views
from .views import RegisterView, CustomLoginView, CustomLogoutView
from django.contrib.auth import views as auth_views
from users.forms import EmailAuthenticationForm

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='registration/logged_out.html'
    ), name='logout'),
    # Регистрация
    path('signup/', auth_views.SignUpView.as_view(), name='signup'),
]
