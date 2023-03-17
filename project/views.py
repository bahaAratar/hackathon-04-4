from rest_framework.permissions import IsAuthenticated , IsAuthenticatedOrReadOnly, AllowAny
from rest_framework import viewsets , generics
from .serializers import *
from .models import *
# from rest_framework import viewsets
# from rest_framework import generics
# from .models import Category, Project
# from .serializers import CategorySerializer, ProjectSerializer
# from rest_framework.viewsets import ModelViewSet


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectDetailSerializer
    queryset = Project.objects.all()
    lookup_url_kwarg = 'project_id'
