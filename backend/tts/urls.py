from django.urls import path, include
from rest_framework import routers

from tts.views import AudioViewSet, ProjectViewSet

router = routers.DefaultRouter()
router.register('audio', AudioViewSet)
router.register('project', ProjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
]