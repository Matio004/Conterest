from django.urls import path
from .views import ConfigDetailView, config_create, config_list

app_name = 'posts'

urlpatterns = [
    path('', config_list, name='posts'),
    path('post/<int:id>/<slug:slug>/', ConfigDetailView.as_view(), name='post_detail'),
    path('create/', config_create, name='create'),
]