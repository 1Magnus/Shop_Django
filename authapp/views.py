from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForms, ShopUsersEditForm


def login(request):
    login_form = ShopUserLoginForm(data=request.POST)
    next_param = request.GET.get('next', '')
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(reverse(request.POST['next']))
            return HttpResponseRedirect(reverse('index'))

    context = {'login_form': login_form, 'next':next_param}
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForms(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForms()

    content = {'register_form': register_form}

    return render(request, 'authapp/register.html', content)


def edit(request):
    if request.method == 'POST':
        edit_form = ShopUsersEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUsersEditForm(instance=request.user)

    content = {'edit_form': edit_form}

    return render(request, 'authapp/edit.html', content)

