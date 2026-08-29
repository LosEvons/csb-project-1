from django.contrib.auth.decorators import login_required
from django.db import connection
from django.shortcuts import render, get_object_or_404

from notes.models import Note


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
