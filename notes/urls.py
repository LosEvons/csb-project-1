from django.urls import path
from notes import views

app_name = 'notes'

urlpatterns = [
    path("<int:note_id>/", views.inspect_note, name="inspect_note"),
    path("search/", views.search, name="search"),
]