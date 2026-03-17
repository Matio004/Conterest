from django.urls import path
from .views import config_detail, config_create, config_list

app_name = 'posts'

urlpatterns = [
    path('', config_list, name='posts'),
    path('<slug:user>/<slug:config>/', config_detail, name='post_detail'),
    path('create/', config_create, name='create'),
]