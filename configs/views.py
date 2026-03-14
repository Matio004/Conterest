from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView

from .models import Config
from .forms import ConfigForm


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


@login_required
def config_create(request):
    if request.method == 'POST':
        form = ConfigForm(request.POST, request.FILES)

        if form.is_valid():
            cd = form.cleaned_data
            try:
                new_item = form.save(commit=False)

                new_item.user = request.user
                new_item.save()
                return redirect(new_item.get_absolute_url())
            except IntegrityError:
                form.add_error('title', 'Title must be unique among your configs.')
    else:
        form = ConfigForm()
    return render(request,
                  'configs/create.html',
                  {
                      'form': form
                  })
