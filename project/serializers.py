from rest_framework import serializers
from .models import *
# from rest_framework import serializers
# from .models import Category, Project

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = '__all__'

# class ProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         exclude = ('owner',)

#     def create(self, validated_data):
#         validated_data['owner'] = self.context['request'].user
#         return super().create(validated_data)



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    executor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Project
        exclude = ('candidates',)

class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

