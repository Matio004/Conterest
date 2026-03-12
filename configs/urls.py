from django.urls import path
from .views import ConfigListView, ConfigDetailView

app_name = 'posts'

urlpatterns = [
    path('', ConfigListView.as_view(), name='posts'),
    path('post/<str:user>/<int:year>/<int:month>/<int:day>/<slug:slug>/', ConfigDetailView.as_view(), name='post_detail'),
]