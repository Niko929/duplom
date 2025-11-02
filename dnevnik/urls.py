from django.urls import path
from dnevnik.views import HomeView, DiaryListView, DiaryDetailView, DiaryCreateView, DiaryDeleteView, DiarySearchView, \
    DiaryUpdateView

app_name = 'dnevnik'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    # Главная страница - список записей
    path('', DiaryListView.as_view(), name='list'),
    # Создание новой записи
    path('create/', DiaryCreateView.as_view(), name='diary_create'),
    # Поиск по записям
    path('search/', DiarySearchView.as_view(), name='search'),
    # Детальный просмотр записи
    path('<int:pk>/', DiaryDetailView.as_view(), name='detail'),
    # Редактирование записи
    path('<int:pk>/update/', DiaryUpdateView.as_view(), name='update'),
    # Удаление записи
    path('<int:pk>/delete/', DiaryDeleteView.as_view(), name='delete'),
]