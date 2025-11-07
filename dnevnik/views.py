from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import DiaryEntry
from .forms import DiaryEntryForm, CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy

class HomeView(TemplateView):
    template_name = 'dnevnik/home.html'

class DiaryListView(LoginRequiredMixin, ListView):
    model = DiaryEntry
    template_name = 'dnevnik/list.html'
    context_object_name = 'diaries'
    paginate_by = 9

    def get_queryset(self):
        queryset = DiaryEntry.objects.filter(
            author=self.request.user
        ).order_by('-created_at')

        # ОТЛАДКА
        print("=" * 50)
        print(f"🔍 Пользователь: {self.request.user}")
        print(f"🔍 Аутентифицирован: {self.request.user.is_authenticated}")
        print(f"🔍 Найдено записей: {queryset.count()}")
        for diary in queryset:
            print(f"📝 {diary.id}: {diary.title} - {diary.created_at}")
        print("=" * 50)

        return queryset

class DiaryDetailView(LoginRequiredMixin, DetailView):
    model = DiaryEntry
    template_name = 'dnevnik/diary_detail.html'
    context_object_name = 'diary'

    def get_queryset(self):
        return DiaryEntry.objects.filter(author=self.request.user)

class DiaryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = DiaryEntry
    fields = ['title', 'content']
    template_name = 'dnevnik/forms.html'
    success_message = "Запись успешно создана!"

    def form_valid(self, form):
        print("🎯 form_valid вызван")
        form.instance.author = self.request.user
        response = super().form_valid(form)
        print(f"✅ Запись создана: {self.object.id} - {self.object.title}")
        return response

    def form_invalid(self, form):
        print("❌ Форма невалидна:", form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новая запись'
        return context

    def get_success_url(self):
        return reverse_lazy('dnevnik:list')

class DiaryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DiaryEntry
    fields = ['title', 'content']
    template_name = 'dnevnik/forms.html'
    success_message = "Запись успешно обновлена!"

    def get_queryset(self):
        return DiaryEntry.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать запись'
        return context

    def get_success_url(self):
        return reverse_lazy('dnevnik:list')

class DiaryDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = DiaryEntry
    template_name = 'dnevnik/delete.html'
    success_message = 'Запись успешно удалена!'

    def get_queryset(self):
        return DiaryEntry.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('dnevnik:list')

class DiarySearchView(LoginRequiredMixin, ListView):
    model = DiaryEntry
    template_name = 'dnevnik/search.html'
    context_object_name = 'diaries'
    paginate_by = 10

    def get_queryset(self):
        queryset = DiaryEntry.objects.filter(author=self.request.user)
        query = self.request.GET.get('q')

        if query:
            search_title = self.request.GET.get('search_title') == 'on'
            search_content = self.request.GET.get('search_content') == 'on'

            if not search_title and not search_content:
                search_title = search_content = True

            conditions = Q()
            if search_title:
                conditions |= Q(title__icontains=query)
            if search_content:
                conditions |= Q(content__icontains=query)

            queryset = queryset.filter(conditions)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['search_title'] = self.request.GET.get('search_title', 'on')
        context['search_content'] = self.request.GET.get('search_content', 'on')
        return context
