from django.contrib import admin
from .models import Documentary, Tag, Url

class TagAdmin(admin.ModelAdmin):
    search_fields = ["value"]
    ordering = ["value"]

class DocumentaryAdmin(admin.ModelAdmin):
    list_display = ["title", "year", "duration"]
    search_fields = ["title", "description"]
    list_filter = ["year"]
    ordering = ['created']

class UrlAdmin(admin.ModelAdmin):
    list_display = ["site", "url", "visitors"]
    search_fields = ["site", "url"]
    list_filter = ["site"]
    ordering = ["created"]

admin.site.register(Documentary, DocumentaryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Url, UrlAdmin)