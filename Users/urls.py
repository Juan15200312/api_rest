from rest_framework.routers import DefaultRouter
from .views import UserModelViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('', viewset=UserModelViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),

]