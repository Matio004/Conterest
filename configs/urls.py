from django.urls import path
from .views import ConfigListView, ConfigDetailView, config_create

app_name = 'posts'

urlpatterns = [
    path('', ConfigListView.as_view(), name='posts'),
    path('post/<int:pk>/', ConfigDetailView.as_view(), name='post_detail'),
    path('create/', config_create, name='create'),
]