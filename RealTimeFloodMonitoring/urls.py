from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('flood_monitor/', include('flood_monitor.urls')),
    path('api/', include(router.urls))
]
