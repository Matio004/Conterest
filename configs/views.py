from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Config
from .forms import ConfigForm


# Create your views here.
def config_detail(request, user, config):
    config = get_object_or_404(Config.published, user__username=user, slug=config)
    return render(request,
                  'configs/details.html',
                  {'config': config,})



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

def config_list(request):
    posts = Config.published.all()
    paginator = Paginator(posts, 20)

    page = request.GET.get('page')
    posts_only = request.GET.get('posts_only')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        if posts_only:
            return HttpResponse('')
        posts = paginator.page(paginator.num_pages)
    if posts_only:
        return render(request,
                      'configs/config_list.html',
                      {'configs': posts})
    return render(request,
                  'configs/list.html',
                  {'configs': posts})