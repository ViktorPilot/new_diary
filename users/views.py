from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView

from config.settings import EMAIL_HOST_USER
from users.forms import CustomCreationForm, UserAuthenticationForm
from users.models import CustomUser


class RegisterView(CreateView):
    """Класс контроллера создания нового пользователя"""

    model = CustomUser
    form_class = CustomCreationForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form: Any) -> Any:
        """Метод, отправляющий приветственное письмо пользователю после успешной регистрации"""
        user = form.save()
        subject = "Приветствие от new_diary!"
        message = "Вы успешно зарегистрировались в приложении new_diary!"
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


class UserDeleteView(LoginRequiredMixin, DeleteView):
    """Удаляет аккаунт текущего пользователя."""

    model = CustomUser
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("users:login")

    def get_object(self, queryset=None):
        """Возвращает только аккаунт текущего пользователя."""
        return self.request.user
