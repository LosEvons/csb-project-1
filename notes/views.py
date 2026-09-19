import json

from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from notes.models import Note, Profile


# Create your views here.

@login_required
def inspect_note(request, note_id):
    note = get_object_or_404(Note, id=note_id) # FLAW! Ownership is not checked!
    # FIX: note = get_object_or_404(Note, id=note_id, owner=request.user)
    return render(request, "notes/inspect_note.html", {"note": note})

@login_required
def search(request):
    q = request.GET.get("q", "")
    results = []
    if q:
        with connection.cursor() as c:
            c.execute(
                f"SELECT id, title, content FROM notes_note WHERE title LIKE '%{q}%'" # FLAW! f-string allows for SQL injection through parameter!
            ) 
            # FIX:
            # c.execute(
            #     "SELECT id, title, content FROM notes_note WHERE title LIKE %s AND owner_id = %s",
            #     [f"%{q}%", request.user.id]
            # )
            results = c.fetchall()

    return render(request, "notes/search.html", {"results": results, "q": q})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("notes:search")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def profile(request):
    p, _ = Profile.objects.get_or_create(user=request.user, defaults={"token": ""})
    token = None
    if request.method == "POST":
        token = p.set_token()
    return render(request, "notes/profile.html",
                  {"has_token": bool(p.token), "new_token": token})

def notes_api(request):
    username, _, token = request.headers.get("Authorization", "").removeprefix("Token ").partition(":")
    p = get_object_or_404(Profile, user__username=username)
    if not p.verify_token(token):
        return JsonResponse({"error": "bad token"}, status=403)
    notes = Note.objects.filter(owner=p.user).values("id", "title", "content")
    return JsonResponse({"notes": list(notes)})

def create_note(request):
    if request.method == "POST":
        Note.objects.create(
            owner=request.user,
            title=request.POST.get("title", ""),
            content=request.POST.get("content", ""),
        )
        return redirect("notes:search")
    return render(request, "notes/create_note.html")