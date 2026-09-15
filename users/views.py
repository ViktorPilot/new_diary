from typing import Any

from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import CustomCreationForm, UserAuthenticationForm, UserModelForm
from users.models import CustomUser


class RegisterView(CreateView):
    """Класс контроллера создания нового пользователя"""

    model = CustomUser
    form_class = CustomCreationForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form: Any) -> Any:
        """Метод, отправляющий приветственное письмо пользователю после успешной регистрации"""
        user = form.save()
        subject = "Приветствие от MyMarketplace!"
        message = "Вы успешно зарегистрировались на сайте MyMarketplace!"
        send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[
                user.email,
            ],
        )
        return super().form_valid(form)


class CustomLoginView(LoginView):
    """Класс контроллера входа пользователя в аккаунт"""

    model = CustomUser
    form_class = UserAuthenticationForm
    template_name = "users/login.html"


class UserUpdateView(UpdateView):
    """Класс контроллера выхода пользователя из аккаунта"""

    model = CustomUser
    form_class = UserModelForm
    success_url = reverse_lazy("catalog:home")
    template_name = "users/update_form.html"
