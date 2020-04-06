from django.db import models


# Create your models here.

class ConfirmedData(models.Model):
    timestamp = models.DateTimeField()
    country = models.CharField(max_length=100)
    count = models.IntegerField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.country} - {self.count}'

    class Meta:
        indexes = [
            models.Index(fields=['created_at'])
        ]


class DeadData(models.Model):
    timestamp = models.DateTimeField()
    country = models.CharField(max_length=100)
    count = models.IntegerField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.country} - {self.count}'

    class Meta:
        indexes = [
            models.Index(fields=['created_at'])
        ]


class RecoveredData(models.Model):
    timestamp = models.DateTimeField()
    country = models.CharField(max_length=100)
    count = models.IntegerField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.country} - {self.count}'

    class Meta:
        indexes = [
            models.Index(fields=['created_at'])
        ]
