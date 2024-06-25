from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from .utils import otp_code_generator


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)

    profile_photo = models.ImageField(upload_to='profile_photos/')
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.email


class OTP(models.Model):
    otp_key = models.UUIDField(default=uuid.uuid4)
    otp_code = models.IntegerField(default=otp_code_generator)
    otp_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    otp_attempt = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.created_at)
