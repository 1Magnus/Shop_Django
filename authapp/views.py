from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForms, ShopUsersEditForm, ShopUser


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

    context = {'login_form': login_form, 'next': next_param}
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForms(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                print('сообщение отправлено')
            else:
                print('сообщение не отправлено')
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


def verify(request, email, activation_key):
    user = ShopUser.objects.filter(email=email).first()
    if user:
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
        return render(request, 'authapp/verify.html')
    return HttpResponseRedirect(reverse('index'))


def send_verify_mail(user):
    subject = 'Verify your account'
    link = reverse("auth:verify", args=[user.email, user.activation_key])
    message = f'{settings.DOMAIN}{link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
