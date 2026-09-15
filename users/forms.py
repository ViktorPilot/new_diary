from typing import Any

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import CustomUser


class StyleMixin:
    """Миксин создающий экземпляр класса для стилизации web-страницы"""

    def __init__(self, *args: Any, **kwargs: dict) -> None:
        """Метод задает стиль web-страниц"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != "phone_number":
                self.fields[field].widget.attrs.update({"class": "form-control"})
            else:
                self.fields[field].widget.attrs.update({"class": "form-control", "placeholder": "X-XXX-XXX-XX-XX"})


class CustomCreationForm(StyleMixin, UserCreationForm):
    """Класс формы для создания нового пользователя"""

    class Meta(UserCreationForm.Meta):
        """Класс метаданных для формы создания нового пользователя"""

        model = CustomUser
        fields = ("email", "password1", "password2")


class UserAuthenticationForm(StyleMixin, AuthenticationForm):
    """Класс формы для аутентификации пользователя"""

    class Meta(UserCreationForm.Meta):
        """Класс метаданных для формы аутентификации пользователя"""

        model = CustomUser
        fields = ("email", "password")


class UserModelForm(StyleMixin, forms.ModelForm):
    """Класс формы для обновления информации о пользователе"""

    class Meta:
        """Класс метаданных для формы обновления информации о пользователе"""

        model = CustomUser
        fields = ("email", "avatar", "phone_number", "country")
