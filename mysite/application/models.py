from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from django.conf import settings

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    status = models.CharField(max_length = 140)
    biography = models.TextField()
    birth_date = models.DateField(default=date.today)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    def __str__(self):
        return self.email

class notes(models.Model):
    date = models.DateTimeField()
    title = models.CharField(max_length = 255)
    text = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    def __unicode__(self):
        return self.title

    