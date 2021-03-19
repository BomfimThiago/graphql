from django.contrib import admin
from apps.cards.models import Card


class CardAdmin(admin.ModelAdmin):
    list_display = ('deck', 'question', 'bucket')


admin.site.register(Card, CardAdmin)