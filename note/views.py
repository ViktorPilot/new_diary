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


class NoteDetailView(LoginRequiredMixin, DetailView):
    """Класс контроллера подробной информации о заметке"""

    model = Note

    def get_object(self, queryset=None):
        """Метод запрещает доступ к заметкам других пользователей"""
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise Http404("Object not found")
        return obj


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


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    """Класс контроллера обновления заметки"""

    model = Note
    form_class = NoteForms
    permission_required = "note.change_note"

    def form_valid(self, form) -> Any:
        """Метод ограничивает права доступа для изменения чужих заметок"""
        user = self.request.user
        if user == form.instance.owner:
            change_note = Permission.objects.get(codename="change_note")
            user.user_permissions.add(change_note)
            return super().form_valid(form)
        raise PermissionDenied

    def get_success_url(self) -> str:
        """Метод перенаправляет на страницу информации об обновленной заметке"""
        return reverse_lazy("note:note_detail", kwargs={"pk": self.object.pk})


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    """Класс контроллера удаления заметки"""

    model = Note
    success_url = reverse_lazy("note:home")
    permission_required = "note.delete_note"

    def post(self, request, *args, **kwargs):
        """Метод ограничивает права доступа для удаления чужих заметок"""
        user = self.request.user
        obj = self.get_object()
        if user.email == obj.owner.email:
            delete_note = Permission.objects.get(codename="delete_note")
            user.user_permissions.add(delete_note)
            return super().post(request, *args, **kwargs)
        raise PermissionDenied
