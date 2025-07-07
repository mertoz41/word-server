from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=0)



class Language(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=2, unique=True, default='en')
    def __str__(self):
        return f"{self.name} ({self.code})"
    

class Word(models.Model):
    text = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, default='exp')
    definition = models.TextField()
    user = models.ForeignKey('api.User', on_delete=models.CASCADE, related_name="words")
    language = models.ForeignKey('api.Language', on_delete=models.CASCADE, related_name="words")
    created_at = models.DateTimeField(auto_now_add=True)
    sentences = models.JSONField(blank=True, null=True)
    translations = models.JSONField(blank=True, null=True)


    def __str__(self):
        return self.text