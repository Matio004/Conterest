from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Config


# Create your views here.
class ConfigListView(ListView):
    queryset = Config.published.all()
    context_object_name = 'configs'
    template_name = 'configs/list.html'
    paginate_by = 20


class ConfigDetailView(DetailView):
    model = Config
    context_object_name = 'config'
    template_name = 'configs/details.html'