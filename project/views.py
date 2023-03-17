from rest_framework.permissions import IsAuthenticated , IsAuthenticatedOrReadOnly, AllowAny
from rest_framework import viewsets , generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import *

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectDetailSerializer
    queryset = Project.objects.all()
    lookup_url_kwarg = 'project_id'


class AddCandidateAPIView(generics.CreateAPIView):
    serializer_class = AddCandidateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs.get('project_id'))
        user = self.request.user

        # Проверяем, что пользователь не является создателем проекта
        if user == project.owner:
            return Response({'статус': 'ошибка', 'сообщение': 'Вы не можете подать заявку на свой собственный проект.'})

        # Проверяем, что пользователь еще не является кандидатом на проекте
        if user in project.candidates.all():
            return Response({"статус":"ошибка","сообщение":"Вы уже подали заявку на участие в этом проекте."})

        # Проверяем, что пользователь не является исполнителем проекта
        if user == project.executor:
            return Response({'статус': 'ошибка', 'сообщение': 'Вы не можете подать заявку на проект, над которым уже работаете.'})

        # Добавляем пользователя в список кандидатов проекта
        project.candidates.add(user)

        return Response({'статус': 'успешно', 'сообщение': 'Ваша заявка успешно отправлена'})

class ChooseExecutorAPIView(generics.UpdateAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    lookup_url_kwarg = 'project_id'

    def patch(self, request, *args, **kwargs):
        project = self.get_object()
        owner = project.owner
        if owner != request.user:
            return Response({'сообщение': 'У вас нет разрешения на выполнение этого действия.'}, status=status.HTTP_403_FORBIDDEN)

        executor_id = request.data.get('executor_id')
        if not executor_id:
            return Response({'Требуетя': 'executor_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            executor = User.objects.get(id=executor_id)
        except User.DoesNotExist:
            return Response({'сообщение': 'Такого исполнителя не существует.'}, status=status.HTTP_400_BAD_REQUEST)

        if not project.candidates.filter(id=executor_id).exists():
            return Response({'сообщение': 'Исполнитель не является кандидатом на этот проект.'}, status=status.HTTP_400_BAD_REQUEST)

        project.executor = executor
        project.is_available = False
        project.is_accepted = True
        project.save()

        serializer = self.get_serializer(project)
        return Response(serializer.data)


