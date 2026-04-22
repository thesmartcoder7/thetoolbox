from rest_framework import serializers
from .models import Repository, AnalysisResult, OverallScore

class AnalysisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisResult
        fields = ['category', 'score', 'details']

class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ['id', 'owner', 'name', 'url']