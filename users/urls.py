from django.urls import path
from . import views
from .views import RegisterView, CustomLoginView, CustomLogoutView
from django.contrib.auth import views as auth_views
from users.forms import EmailAuthenticationForm

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(
        form_class=EmailAuthenticationForm,
        template_name='registration/login.html'
    ), name='login'),
]
