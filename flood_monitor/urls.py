from django.urls import path
from flood_monitor.views.rest import FloodMonitorDataViewset
from flood_monitor.views.views import FloodMonitorView
from RealTimeFloodMonitoring.urls import router

app_name = 'flood_monitor'

router.register(r'flood_monitor', FloodMonitorDataViewset, basename='api_flood_monitor')


urlpatterns = [
    path('', FloodMonitorView.as_view(), name='flood_monitor'),
]
