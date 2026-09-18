from typing import Any

from django import forms

from note.models import Note


class NoteForms(forms.ModelForm):

    class Meta:
        model = Note
        fields = ["title", "text", "mood", "energy", "image"]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.fields["mood"].widget = forms.Select(
            choices=[
                ("😊", "😊"),
                ("🙂", "🙂"),
                ("😐", "😐"),
                ("😔", "😔"),
                ("😡", "😡"),
            ]
        )

        self.fields["energy"].widget = forms.NumberInput(
            attrs={
                "min": 1,
                "max": 10,
            }
        )

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": "form-control",
            })