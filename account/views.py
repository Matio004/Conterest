from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from configs.models import Config
from .models import Profile
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm

# Create your views here.
@login_required
def dashboard(request):
    object_list = Config.objects.filter(user=request.user)

    paginator = Paginator(object_list, 20)
    page = request.GET.get('page')
    try:
        configs = paginator.page(page)
    except PageNotAnInteger:
        configs = paginator.page(1)
    except EmptyPage:
        configs = paginator.page(paginator.num_pages)
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard',
                   'page': page,
                   'configs': configs,})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)  # tworzenie nowego uzytkownika; nie zapisywanie w bazie danych
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # zapisywanie
            new_user.save()
            # utworzenie profilu
            profile = Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Uaktualnienie profilu zakończyło się sukcesem.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Wystąpił błąd podczas uaktualniania profilu')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})