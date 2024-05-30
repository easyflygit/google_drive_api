from django.contrib import admin
from .models import File


class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'data')


admin.site.register(File, FileAdmin)
