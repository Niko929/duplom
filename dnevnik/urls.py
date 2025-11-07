from django.urls import path
from dnevnik.views import HomeView, DiaryListView, DiaryDetailView, DiaryCreateView, DiaryDeleteView, DiarySearchView, \
    DiaryUpdateView

app_name = 'dnevnik'

urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('', DiaryListView.as_view(), name='list'),
    path('create/', DiaryCreateView.as_view(), name='diary_create'),
    path('detail/<int:pk>/', DiaryDetailView.as_view(), name='diary_detail'),
    path('edit/<int:pk>/', DiaryUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', DiaryDeleteView.as_view(), name='delete'),
    path('search/', DiarySearchView.as_view(), name='search'),
]