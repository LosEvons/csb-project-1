import secrets

#from django.contrib.auth.hashers import make_password, check_password
from django.db import models

from django.conf import settings


# Create your models here.

class Note(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=128)

    def set_token(self):
        new_token = secrets.token_hex(16)
        self.token = new_token # FLAW! Token stored as plaintext, cryptographic failure.
        # FIX: self.token = make_password(new_token)
        self.save()
        return new_token

    # FIX for cryptographic failure through plaintext token
    # def verify_token(self, other_token):
    #     return check_password(other_token, self.token)