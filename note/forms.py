from typing import Any

from django import forms

from note.models import Note


class NoteForms(forms.ModelForm):
    """Класс формы для модели заметок"""

    class Meta:
        """Класс метаданных для формы модели заметок"""

        model = Note


    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Переопределение метода с добавлением пользовательского стиля"""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "rows": "3"})
