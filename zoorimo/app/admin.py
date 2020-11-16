from django.contrib import admin
from django.contrib.admin import register, ModelAdmin

from zoorimo.app.models import User, Zoorimo, Stock, Quiz, Kospi


@register(User)
class UserAdmin(ModelAdmin):
    pass


@register(Zoorimo)
class ZoorimoAdmin(ModelAdmin):
    pass


@register(Stock)
class StockAdmin(ModelAdmin):
    pass


@register(Quiz)
class QuizAdmin(ModelAdmin):
    pass


@register(Kospi)
class KospiAdmin(ModelAdmin):
    pass
