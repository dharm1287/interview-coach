from django.db import models
from django.contrib.auth.models import User

class InterviewSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=200)
    level = models.CharField(max_length=50, default='Mid')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} ({self.level}) - {self.created_at:%Y-%m-%d %H:%M}"

class Question(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE)
    text = models.TextField()
    difficulty = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:60]

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    transcript = models.TextField(blank=True, null=True)
    audio = models.FileField(upload_to='answers/', blank=True, null=True)
    feedback = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to Q#{self.question.id} @ {self.created_at:%Y-%m-%d %H:%M}"

#### FILE: core/forms.py
