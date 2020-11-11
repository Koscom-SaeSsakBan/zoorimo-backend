from django.db import models


class Users(models.Model):
    name = models.CharField(max_length=200)
    mail = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    USERNAME_FIELD = 'name'

