from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from dnevnik.forms import CustomUserCreationForm


class RegisterView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('dnevnik:list')
    success_message = 'Регистрация прошла успешно!'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


# Вход с использованием auth_views.LoginView
class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    success_message = 'Добро пожаловать!'

    def get_success_url(self):
        return reverse_lazy('dnevnik:list')


# Выход с использованием auth_views.LogoutView
class CustomLogoutView(LogoutView):
    def get(self, request):
        # Для GET запроса показываем страницу подтверждения
        return render(request, 'registration/logout_confirm.html')

    def post(self, request):
        # Для POST запроса выполняем выход
        logout(request)
        return redirect('home')


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'

    def form_valid(self, form):
        # Сохраняем пользователя
        user = form.save()

        # Явно указываем бэкенд аутентификации
        from django.contrib.auth.backends import ModelBackend
        backend = 'django.contrib.auth.backends.ModelBackend'  # или ваш кастомный бэкенд

        login(self.request, user, backend=backend)
        return redirect('diary:list')