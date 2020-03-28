from django.urls import path

from frontend.views import Home, Simulation

app_name = 'frontend'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('simulation', Simulation.as_view(), name='simulation')
]
