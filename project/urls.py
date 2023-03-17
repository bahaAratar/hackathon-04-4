from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# router.register('categories', CategoryModelViewset)
# router.register('projects', ProjectModelViewset)
router.register('categories', CategoryViewSet, basename='category')
router.register('projects', ProjectViewSet, basename='project')

urlpatterns = [
    path('projects/<int:project_id>/', ProjectDetailAPIView.as_view(), name='project-detail'),
    path('', include(router.urls)),
   
]