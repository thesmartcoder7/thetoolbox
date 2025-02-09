from django.urls import path
from repo_analyzer.views import analyze_repository
urlpatterns = [
    path('analyze/', analyze_repository, name='analyze-api'),
]