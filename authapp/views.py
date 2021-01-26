from django.db import transaction
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from authapp.models import User

from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from basketapp.models import Basket
from authapp.forms import UserProfileEditForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'authapp/login.html', context)


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:profile'))
    else:
        form = UserProfileForm(instance=request.user)

    baskets = Basket.objects.filter(user=request.user)
    context = {
        'title': 'Профиль', 'form': form,
        'baskets': baskets,
    }
    return render(request, 'authapp/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = f'Подтверждение учетной записи {user.username}'

    message = f'Для подтверждения учетной записи {user.username} на портале \
{settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                print('сообщение подтверждения отправлено')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                print('ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('auth:login'))
        else:
            register_form = UserRegisterForm()
            content = {'title': title, 'register_form': register_form}
            return render(request, 'authapp/register.html', content)

    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'authapp/register.html', context)


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('main'))


@transaction.atomic
def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = UserProfileEditForm(request.POST, request.FILES,
                                        instance=request.user)
        profile_form = UserProfileEditForm(request.POST,
                                           instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = UserProfileEditForm(instance=request.user)
        profile_form = UserProfileEditForm(
            instance=request.user.shopuserprofile
        )

    content = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form
    }

    return render(request, 'authapp/edit.html', content)
