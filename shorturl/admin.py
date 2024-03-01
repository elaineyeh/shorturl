from django.contrib import admin

from .models import Url


class UrlAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'code')


admin.site.register(Url, UrlAdmin)