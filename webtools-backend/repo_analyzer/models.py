from django.db import models

class Repository(models.Model):
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    url = models.URLField()
    last_analyzed = models.DateTimeField(auto_now=True)

class AnalysisResult(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    score = models.FloatField()
    details = models.JSONField()

class OverallScore(models.Model):
    repository = models.OneToOneField(Repository, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f"{self.repository.owner}/{self.repository.name}: {self.score:.2f}"