from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from note.forms import NoteForms
from note.models import Note


class NoteListView(ListView):
    """Класс контроллера списка заметок"""

    model = Note


class NoteDetailView(LoginRequiredMixin, DetailView):
    """Класс контроллера подробной информации о заметке"""

    model = Note


class NoteCreateView(LoginRequiredMixin, CreateView):
    """Класс контроллера создания новой заметки"""

    model = Note
    form_class = NoteForms


    def get_success_url(self) -> str:
        """Метод перенаправляет на страницу информации о созданной заметке"""
        return reverse_lazy("note:note_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form) -> Any:
        user = self.request.user
        form.instance.owner = user
        if not user.has_perm("note.can_unpublish_note"):
            raise PermissionDenied
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    """Класс контроллера создания новой заметки"""

    model = Note
    form_class = NoteForms
    permission_required = "catalog.change_note"

    def form_valid(self, form) -> Any:
        """Метод ограничивает права доступа для изменения заметки всех пользователей, кроме владельца"""
        user = self.request.user
        if user == form.instance.owner:
            change_note = Permission.objects.get(codename="change_note")
            user.user_permissions.add(change_note)
            return super().form_valid(form)
        raise PermissionDenied


    def get_success_url(self) -> str:
        """Метод перенаправляет на страницу информации о созданной заметке"""
        return reverse_lazy("note:note_detail", kwargs={"pk": self.object.pk})


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    """Класс контроллера удаления заметки"""

    model = Note
    success_url = reverse_lazy("note:home")
    permission_required = "note.delete_note"

    def post(self, request, *args, **kwargs):
        """Метод ограничивает права доступа для удаления товаров всех пользователей кроме владельца товара"""
        user = self.request.user
        obj = self.get_object()
        if user.email == obj.owner.email:
            delete_note = Permission.objects.get(codename="delete_note")
            user.user_permissions.add(delete_note)
            return super().post(request, *args, **kwargs)
        raise PermissionDenied
