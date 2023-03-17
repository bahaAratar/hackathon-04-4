from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    executor = serializers.PrimaryKeyRelatedField(read_only=True)
    chosen_candidate = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Project
        exclude = ('candidates',)

class ProjectDetailSerializer(serializers.ModelSerializer):
    chosen_candidate = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    class Meta:
        model = Project
        fields = '__all__'


class AddCandidateSerializer(serializers.Serializer):
    project_id = serializers.IntegerField(required=True)


class ExecutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProjectCandidateSerializer(serializers.ModelSerializer):
    candidates = ExecutorSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'candidates']

