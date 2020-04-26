from django.db import models


class BaseClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ConfirmedData(BaseClass):
    timestamp = models.DateTimeField()
    country = models.CharField(max_length=100)
    count = models.IntegerField(default=0.0)

    def __str__(self):
        return f'{self.country} - {self.count}'

    class Meta:
        indexes = [
            models.Index(fields=['timestamp'])
        ]


class DeadData(BaseClass):
    timestamp = models.DateTimeField()
    country = models.CharField(max_length=100)
    count = models.IntegerField(default=0.0)

    def __str__(self):
        return f'{self.country} - {self.count}'

    class Meta:
        indexes = [
            models.Index(fields=['timestamp'])
        ]


class RecoveredData(BaseClass):
    timestamp = models.DateTimeField()
    country = models.CharField(max_length=100)
    count = models.IntegerField(default=0.0)

    def __str__(self):
        return f'{self.country} - {self.count}'

    class Meta:
        indexes = [
            models.Index(fields=['timestamp'])
        ]


class CovidData(BaseClass):
    timestamp = models.DateTimeField()
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    ibge_id = models.CharField(max_length=50)
    new_deaths = models.IntegerField(default=None, null=True, blank=True)
    deaths = models.IntegerField(default=None, null=True, blank=True)
    new_cases = models.IntegerField(default=None, null=True, blank=True)
    total_cases = models.IntegerField(default=None, null=True, blank=True)
    new_recovered = models.IntegerField(default=None, null=True, blank=True)
    recovered = models.IntegerField(default=None, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['timestamp'])
        ]


class ImportsUpdate(BaseClass):
    endpoint = models.CharField(max_length=1024)
    columns = models.CharField(max_length=1200)
    rows_count = models.IntegerField(default=None, null=True, blank=True)
    cols_count = models.IntegerField(default=None, null=True, blank=True)
    total_import_time = models.FloatField(default=None, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['created_at'])
        ]
