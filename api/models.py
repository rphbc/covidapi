from django.db import models


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ConfirmedData(models.Model):
    timestamp = models.DateTimeField()
    country = models.CharField(max_length=100)
    count = models.IntegerField(default=0.0)

    def __str__(self):
        return f'{self.country} - {self.count}'


class DeadData(models.Model):
    timestamp = models.DateTimeField()
    country = models.CharField(max_length=100)
    count = models.IntegerField(default=0.0)

    def __str__(self):
        return f'{self.country} - {self.count}'


class RecoveredData(models.Model):
    timestamp = models.DateTimeField()
    country = models.CharField(max_length=100)
    count = models.IntegerField(default=0.0)

    def __str__(self):
        return f'{self.country} - {self.count}'
