from django.urls import path

from frontend.views import Home

app_name = 'frontend'

urlpatterns = [
    path('', Home.as_view(), name='home'),
]
