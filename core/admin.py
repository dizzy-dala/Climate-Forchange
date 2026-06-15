from django.contrib import admin

from .models import NewsArticle, PDFResource, UserProfile, WeatherAlert

from .models import AuditLog, WeatherRequestLog


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'receive_alerts', 'created_at']
    search_fields = ['user__username', 'phone', 'city']


@admin.register(PDFResource)
class PDFResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'active', 'uploaded_at']
    search_fields = ['title', 'description']
    list_filter = ['active']


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at', 'active']
    list_filter = ['active']
    search_fields = ['title', 'content']


@admin.register(WeatherAlert)
class WeatherAlertAdmin(admin.ModelAdmin):
    list_display = ['title', 'alert_type', 'severity', 'active', 'created_at', 'expires_at']
    list_filter = ['alert_type', 'severity', 'active']
    search_fields = ['title', 'message']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['level', 'action', 'user', 'created_at']
    list_filter = ['level']
    search_fields = ['action', 'details', 'user__username']


@admin.register(WeatherRequestLog)
class WeatherRequestLogAdmin(admin.ModelAdmin):
    list_display = ['city', 'user', 'ip', 'result_summary', 'created_at']
    search_fields = ['city', 'user__username', 'ip']
