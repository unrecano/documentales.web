"""
Django admin.
"""
from django.contrib import admin
from .models import Documentary, Report, Site

class DocumentaryAdmin(admin.ModelAdmin):
    """
    Custom admin view for documentary.
    """
    list_display = ["title", "year", "duration", "sites", "views"]
    search_fields = ["title", "description"]
    list_filter = ["year"]
    ordering = ["created"]

class SiteAdmin(admin.ModelAdmin):
    """
    Custom admin view for site.
    """
    list_display = ["name", "url", "visitors"]
    search_fields = ["name", "url"]
    list_filter = ["name"]
    ordering = ["created"]

class ReportAdmin(admin.ModelAdmin):
    """
    Custom admin view for report.
    """
    list_display = ["site", "comment"]
    search_fields = ["comment"]
    ordering = ["created"]

admin.site.register(Documentary, DocumentaryAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(Report, ReportAdmin)
