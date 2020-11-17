from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='이메일',
        null=False
    )
    name = models.CharField(
        verbose_name='이름',
        max_length=255,
        null=False,
        blank=False
    )


class Zoorimo(models.Model):
    # id
    user = models.ForeignKey(
        verbose_name='소유자',
        to=User,
        on_delete=models.CASCADE,
        null=False,
        related_name='zoorimo_user'
    )
    size = models.IntegerField(
        verbose_name='크기',
        null=False
    )
    status = models.IntegerField(
        verbose_name='상태',
        null=False
    )


class Stock(models.Model):
    user = models.ForeignKey(
        verbose_name='소유자',
        to=User,
        on_delete=models.CASCADE,
        null=False,
        related_name='stock_user'
    )
    stock_name = models.CharField(
        verbose_name='이름',
        max_length=255,
        null=False,
        blank=False
    )
    average_price = models.IntegerField(
        verbose_name='평단가',
        null=False
    )
    stock_count = models.IntegerField(
        verbose_name='보유수',
        null=False
    )


class Quiz(models.Model):
    question = models.CharField(
        verbose_name='문제',
        max_length=255,
        null=False,
        blank=False
    )
    answer = models.CharField(
        verbose_name='답변',
        max_length=255,
        null=False,
        blank=False
    )
    solution = models.CharField(
        verbose_name='해설',
        max_length=255,
        null=False,
        blank=False
    )


class Kospi(models.Model):
    name = models.CharField(
        verbose_name='이름',
        max_length=255,
        null=False,
        blank=False
    )
    code = models.CharField(
        verbose_name='코드',
        max_length=255,
        null=False,
        blank=False
    )
