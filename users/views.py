import random
from typing import Any

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView

from catalog.services import send_email
from shop import settings

from users.forms import RegisterForm, ResetPasswordForm, ProfileUpdateForm
from users.models import User


class RegisterView(CreateView):
    '''
    Класс для регистрации пользователей
    Класс для регистрации пользователей
    '''
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form) -> HttpResponse:
        if form.is_valid():
            self.object = form.save()
            self.object.is_active = False
            self.object.save()

            token = default_token_generator.make_token(self.object)
            uid = urlsafe_base64_encode(force_bytes(self.object.pk))
            active_url = reverse_lazy('users:email_confirm', kwargs={'uidb64': uid, 'token': token})

            send_mail(
                'Подтверждение e-mail адресса',
                f'Перейдите по ссылке, чтобы подтвердить e-mail адресс: http://127.0.0.1:8000/{active_url}',
                settings.EMAIL_HOST_USER,
                [self.object.email],
                fail_silently=False
            )

            return redirect('users:sent_email')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


class UserConfirmEmailView(View):
    '''
    Класс для проверки подтверждения пользователя по email
    '''

    def get(self, request, uidb64, token) -> HttpResponse:
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except:
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            group = Group.objects.get(name='seller')
            user.groups.add(group)
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_failed_confirmed')


class EmailConfirmSentView(TemplateView):
    '''
    Класс для отображения страницы с оповещением об отправленом
    письме
    '''
    template_name = 'users/sent_email.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подтверждение email'

        return context


class EmailConfirmedView(TemplateView):
    '''
    Класс для отображения страницы с оповещением об
    подтвержденом e-mail адресе
    '''
    template_name = 'users/email_confirmed.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Email подтвержден'

        return context


class EmailFailedConfirmView(TemplateView):
    '''
    Класс для отображения страницы с оповещением об
    неподтвержденом e-mail адресе
    '''
    template_name = 'users/failed_email_confirm.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ошибка подтверждения email'

        return context


class PasswordResetSentView(TemplateView):
    '''
    Класс для отображения страницы с оповещением об успешной
    отправки нового пароля на почту
    '''
    template_name = 'users/sent_password.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пароль отправлен'

        return context


def get_new_password(request) -> HttpResponse:
    '''
    Генерация нового пароля с последующей отправкой на почту
    пользователя
    '''
    form = ResetPasswordForm()
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=request.POST.get('email'))
            password = ''.join([str(random.randint(0, 10)) for _ in range(10)])
            user.set_password(password)
            user.save()

            send_email(
                user.email,
                'Новый пароль!',
                f'Сгенирированный пароль для входа в систему: {password}',
            )
            return redirect('users:sent_password')

    return render(request, 'users/password_reset.html', {'form': form, 'title': 'Восстановление пароля'})


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    '''
    Класс для редактирования профиля пользователя
    '''
    model = User
    form_class = ProfileUpdateForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None) -> User:
        return self.request.user

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = f'Профиль {self.request.user.email}'
        return context
