from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password
from django.db import models
from Users.models import User
import secrets

def get_expired():
    now = timezone.now()
    expire = now + timedelta(days=1)
    return expire

def generar_token():
    token = ''
    for i in range(9):
        token = token + str(secrets.randbelow(9))
    code_hash = make_password(token)
    return token, code_hash

class PasswordReset(models.Model):
    class Meta:
        db_table = 'password_reset'
        ordering = ['-created_at']
        verbose_name = 'Token reset password'
        verbose_name_plural = 'Tokens reset password'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset')
    code_hash = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(default=get_expired)
    used = models.BooleanField(default=False)
    request_ip = models.GenericIPAddressField(null=True, blank=True)
    consumed_at = models.DateTimeField(null=True, blank=True)
    attempts = models.IntegerField(default=0)

    def __str__(self):
        return self.user.first_name