from django.contrib import admin

from .models import Image, TempUrl


admin.site.register(Image)
admin.site.register(TempUrl)
