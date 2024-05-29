from django.contrib import admin
from .models import File


class FileAdmin(admin.ModelAdmin):
    fields = ['__all__']


admin.site.register(File, FileAdmin)
