from django.urls import path
from notes import views

app_name = 'notes'

urlpatterns = [
    path("<int:note_id>/", views.inspect_note, name="inspect_note"),
    path("search/", views.search, name="search"),
    path("profile/", views.profile, name="profile"),
    path("api/notes/", views.notes_api, name="notes_api"),
    path("new/", views.create_note, name="create_note"),
]