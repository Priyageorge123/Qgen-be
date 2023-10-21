from django.db import models
from django.utils import timezone

# Create your models here.


class Question(models.Model):
    class Levels(models.TextChoices):
        Application = 'Application'
        Evaluation = 'Evaluation'
        Synthesis = 'Synthesis'
        Knowledge = 'Knowledge'
        Comprehenssion = 'Comprehension'
        Analysis = 'Analysis'
    id = models.AutoField(primary_key=True)
    question_text = models.CharField(max_length=1000)
    level = models.CharField(max_length=100, choices=Levels.choices)
    module = models.CharField(max_length=1000)
    mark = models.IntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text
