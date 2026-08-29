import os
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from notes.models import Note, Profile

call_command("migrate", "--noinput")

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@admin.com", "admin")

users = {}
u1, c1 = User.objects.get_or_create(username="steve")
if c1:
    u1.set_password("steve")
    u1.save()
users["steve"] = u1

u2, c2 = User.objects.get_or_create(username="molly")
if c2:
    u2.set_password("molly")
    u2.save()
users["molly"] = u2


if not Note.objects.exists():
    Note.objects.create(owner=u1, title="Steve's cooking", content="Steve likes cooking")
    Note.objects.create(owner=u1, title="Steve's banking", content="1234")
    Note.objects.create(owner=u2, title="Molly's painting", content="Molly hates painting")

p, _ = Profile.objects.get_or_create(user=u2, defaults={"token": ""})
token = p.set_token()
