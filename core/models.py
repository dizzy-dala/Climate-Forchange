from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    receive_alerts = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class PDFResource(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='pdfs/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class WeatherAlert(models.Model):
    ALERT_TYPES = [
        ('flood', 'Flood Warning'),
        ('rain', 'Heavy Rainfall'),
        ('drought', 'Drought Alert'),
        ('wind', 'Strong Wind Alert'),
        ('heat', 'Heat Wave Alert'),
    ]
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_alert_type_display()} - {self.title}'


class AuditLog(models.Model):
    LEVELS = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ]

    level = models.CharField(max_length=10, choices=LEVELS, default='info')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=255)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.level}] {self.action} @ {self.created_at.isoformat()}'


class WeatherRequestLog(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=150, blank=True)
    ip = models.CharField(max_length=50, blank=True)
    result_summary = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.city} by {self.user or "anonymous"} @ {self.created_at.isoformat()}'
