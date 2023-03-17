from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('orders', OrderViewSet, basename='order')
router.register('ratings', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
]