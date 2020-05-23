from django.contrib import admin
from .models import Documentary, Tag

class TagAdmin(admin.ModelAdmin):
    search_fields = ["value"]
    ordering = ["value"]

class DocumentaryAdmin(admin.ModelAdmin):
    list_display = ["title", "url", "year", "duration"]
    search_fields = ["title", "description"]
    list_filter = ["year"]
    ordering = ['created']

admin.site.register(Documentary, DocumentaryAdmin)
admin.site.register(Tag, TagAdmin)