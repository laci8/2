from django.contrib import admin

from django.contrib import admin
from .models import VisitorLog

@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'timestamp', 'path', 'country', 'device_type', 'browser')
    list_filter = ('is_authenticated', 'device_type', 'browser', 'os')
    search_fields = ('ip_address', 'user_agent')