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
    project_id = serializers.IntegerField()

    def validate(self, data):
        project_id = data['project_id']
        project = Project.objects.filter(pk=project_id, is_available=True, is_accepted=False).first()
        if not project:
            raise serializers.ValidationError('Invalid project ID or project is not available for application.')
        if self.context['request'].user == project.owner:
            raise serializers.ValidationError('You cannot apply to your own project.')
        if self.context['request'].user in project.candidates.all():
            raise serializers.ValidationError('You have already applied to this project.')
        if self.context['request'].user == project.executor:
            raise serializers.ValidationError('You cannot apply to a project you are already working on.')
        return data

class ExecutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProjectCandidateSerializer(serializers.ModelSerializer):
    candidates = ExecutorSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'candidates']

