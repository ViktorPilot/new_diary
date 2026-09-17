from django.db import models

from users.models import CustomUser


class Note(models.Model):
    """Класс заметки"""
    title = models.CharField(max_length=200, verbose_name="название заметки", )
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="note")
    date = models.DateField(auto_now_add=True, verbose_name="дата создания записи")
    text = models.TextField(verbose_name="текст заметки",)
    mood = models.CharField(max_length=20, verbose_name="настроение",)
    energy = models.PositiveSmallIntegerField(verbose_name="энергия",)
    image = models.ImageField(upload_to="note/image/", blank=True, null=True, verbose_name="картинка",)

    def __str__(self) -> str:
        """Магический метод, возвращающий название заметки"""
        return f"{self.title}"

    class Meta:
        """Класс метаданных для заметки"""

        verbose_name = "заметка"
        verbose_name_plural = "заметки"
        ordering = ["id"]
        db_table = "note"
        permissions = [
            ("can_unpublish_note", "Can unpublish note"),
        ]