from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import DiaryEntry
from .forms import DiaryEntryForm, CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, DetailView,
    UpdateView, DeleteView
)

class HomeView(TemplateView):
    template_name = 'dnevnik/home.html'


class DiaryListView(LoginRequiredMixin, ListView):
    model = DiaryEntry
    template_name = 'dnevnik/list.html'
    context_object_name = 'diaries'
    paginate_by = 9

    def get_queryset(self):
        return DiaryEntry.objects.filter(
            author=self.request.user
        ).order_by('-created_at')


class DiaryDetailView(LoginRequiredMixin, DetailView):
    model = DiaryEntry
    template_name = 'dnevnik/diary_detail.html'
    context_object_name = 'diary'

    def get_queryset(self):
        # Пользователь может просматривать только свои записи
        return DiaryEntry.objects.filter(author=self.request.user)


class DiaryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = DiaryEntry
    fields = ['title', 'content']
    template_name = 'dnevnik/forms.html'
    success_url = reverse_lazy('dnevnik:list')
    success_message = "Запись успешно создана!"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новая запись'
        return context

    def get_success_url(self):
        return reverse_lazy('list')



class DiaryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DiaryEntry
    fields = ['title', 'content']
    template_name = 'dnevnik/diary_update.html'
    success_message = "Запись успешно обновлена!"

    def get_queryset(self):
        return DiaryEntry.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать запись'
        return context

    def get_success_url(self):
        return reverse_lazy('diary-detail', kwargs={'pk': self.object.pk})


class DiaryDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = DiaryEntry
    template_name = 'dnevnik/delete.html'
    success_message = 'Запись успешно удалена!'
    success_url = reverse_lazy('dnevnik:list')

    def get_queryset(self):
        return DiaryEntry.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('list')


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'

    def form_valid(self, form):
        try:
            user = form.save()
            login(self.request, user)
            print(f"✅ Пользователь создан: {user.email}")  # Для отладки
            return redirect('dnevnik:list')
        except Exception as e:
            print(f"❌ Ошибка: {e}")  # Для отладки
            return self.form_invalid(form)

    def form_invalid(self, form):
        print("❌ Форма невалидна:", form.errors)  # Для отладки
        return super().form_invalid(form)


class DiarySearchView(ListView):
    model = DiaryEntry
    template_name = 'dnevnik/search.html'
    context_object_name = 'diaries'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            # Получаем параметры фильтров
            search_title = self.request.GET.get('search_title') == 'on'
            search_content = self.request.GET.get('search_content') == 'on'

            # Если не выбраны конкретные поля, ищем везде
            if not search_title and not search_content:
                search_title = search_content = True

            # Создаем условия для поиска
            conditions = Q()
            if search_title:
                conditions |= Q(title__icontains=query)
            if search_content:
                conditions |= Q(content__icontains=query)

            queryset = queryset.filter(conditions)

        # Фильтруем только записи текущего пользователя
        return queryset.filter(author=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['search_title'] = self.request.GET.get('search_title', 'on')
        context['search_content'] = self.request.GET.get('search_content', 'on')
        return context