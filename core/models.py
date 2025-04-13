from django.db import models
from django.utils import timezone

class VisitorLog(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(null=True, blank=True)
    referrer = models.URLField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    path = models.CharField(max_length=255)
    is_authenticated = models.BooleanField(default=False)
    country = models.CharField(max_length=100, null=True, blank=True)
    device_type = models.CharField(max_length=50, null=True, blank=True)
    browser = models.CharField(max_length=100, null=True, blank=True)
    os = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.ip_address} - {self.timestamp}"


""" class VisitorLog(models.Model):
    ip_address = models.GenericIPAddressField()  # Campo obbligatorio
    user_agent = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=2)  # Codice paese a 2 lettere
    visit_time = models.DateTimeField(auto_now_add=True) """

