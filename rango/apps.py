from django.apps import AppConfig

from rango import admin


class RangoConfig(AppConfig):
    name = 'rango'

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')
    name='rango'


