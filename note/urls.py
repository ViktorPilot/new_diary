from django.urls import path

from note import views
from note.apps import NoteConfig

app_name = NoteConfig.name

urlpatterns = [
    path("home/", views.NoteListView.as_view(), name="home"),
    path("note_detail/<int:pk>/", views.NoteDetailView.as_view(), name="note_detail"),
    path("add_note/", views.NoteCreateView.as_view(), name="add_note"),
    path("update_note/<int:pk>/", views.NoteUpdateView.as_view(), name="update_note"),
    path("delete_note/<int:pk>/", views.NoteDeleteView.as_view(), name="delete_note"),
]
