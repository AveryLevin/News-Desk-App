from django.contrib import admin

from .models import Source, UserProfile, Tag

# Register your models here.
admin.site.register(Source)
admin.site.register(UserProfile)
admin.site.register(Tag)