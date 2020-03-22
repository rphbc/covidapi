from django.contrib import admin

# Register your models here.
from api.models import ConfirmedData, DeadData, RecoveredData

admin.site.register(ConfirmedData)
admin.site.register(DeadData)
admin.site.register(RecoveredData)
