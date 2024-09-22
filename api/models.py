from django.db import models
from django.contrib.auth.models import User


class Announcement(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="announcements")

    def __str__(self):
        return self.title   
    
class Subject(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    date = models.DateField()
    subject_code = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="subject_code")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student")
    status = models.BooleanField()

    def __str__(self):
        return f"{self.student.username} - {self.date}"
    
class Results(models.Model):
    date = models.DateField(auto_now_add=True)
    subject_code = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="result_subject_code")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="result_student")
    score = models.IntegerField()
    max_score = models.IntegerField()
    status = models.BooleanField()

    def __str__(self):
        return f"{self.student.username} - {self.date}"
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            existing_result = Results.objects.filter(student=self.student, subject_code=self.subject_code).first()
            if existing_result:
                existing_result.score = self.score
                existing_result.max_score = self.max_score
                existing_result.status = self.status
                existing_result.save()
                return
        super().save(*args, **kwargs)