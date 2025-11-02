from django.urls import path
from dnevnik.views import HomeView, DiaryListView, DiaryDetailView, DiaryCreateView, DiaryDeleteView, DiarySearchView

app_name = 'dnevnik'

urlpatterns = [
    path('', DiaryListView.as_view(), name='list'),
    path('home/', HomeView.as_view(), name='home'),
    path('create/', DiaryCreateView.as_view(), name='diary_create'),
    path('detail/<int:pk>/', DiaryDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', DiaryDeleteView.as_view(), name='delete'),
    path('search/', DiarySearchView.as_view(), name='search'),
]