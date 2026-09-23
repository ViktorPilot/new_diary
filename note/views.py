from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from note.forms import NoteForms
from note.models import Note


class OwnerNoteQuerysetMixin:
    """Ограничивает работу заметками текущего пользователя."""

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class NoteListView(LoginRequiredMixin, ListView):
    """Класс контроллера списка заметок"""

    model = Note

    def get_queryset(self):
        """Фильтрует записи пользователя по году, месяцу и поисковому запросу"""

        queryset = Note.objects.filter(owner=self.request.user)

        year = self.request.GET.get("year")
        month = self.request.GET.get("month")
        search = self.request.GET.get("search")

        if year:
            queryset = queryset.filter(date__year=year)

        if month:
            queryset = queryset.filter(date__month=month)

        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(text__icontains=search))

        return queryset.order_by("-date")

    def get_context_data(self, **kwargs):
        """Метод задает дефолтные значения года и месяца"""
        context = super().get_context_data(**kwargs)

        context["year"] = self.request.GET.get("year", "2026")
        context["month"] = self.request.GET.get("month", "")

        return context


class NoteDetailView(LoginRequiredMixin, OwnerNoteQuerysetMixin, DetailView):
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
        """Метод записывает в создаваемую заметку текущего пользователя"""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, OwnerNoteQuerysetMixin, UpdateView):
    """Класс контроллера обновления заметки"""

    model = Note
    form_class = NoteForms

    def get_success_url(self) -> str:
        """Метод перенаправляет на страницу информации об обновленной заметке"""
        return reverse_lazy("note:note_detail", kwargs={"pk": self.object.pk})


class NoteDeleteView(LoginRequiredMixin, OwnerNoteQuerysetMixin, DeleteView):
    """Класс контроллера удаления заметки"""

    model = Note
    success_url = reverse_lazy("note:home")
