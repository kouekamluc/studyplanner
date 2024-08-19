from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone







class File(models.Model):
    file = models.FileField(upload_to='uploads/')
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey('Task', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    time_zone = models.CharField(max_length=50, default='UTC')
    preferred_study_time = models.TimeField(null=True, blank=True)
    daily_study_goal = models.DurationField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return self.name
class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    difficulty_level = models.IntegerField(choices=[(1, 'Easy'), (2, 'Medium'), (3, 'Hard')], default=2)
    color = models.CharField(max_length=7, default='#007bff')  # Hex color code
    files = models.ManyToManyField(File, related_name='courses', blank=True)


    def __str__(self):
        return self.name

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    estimated_time = models.DurationField()
    priority = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=2)
    completed = models.BooleanField(default=False)
    tags = models.CharField(max_length=200, blank=True)  # Comma-separated tags
    reminder = models.DateTimeField(null=True, blank=True)
    files = models.ManyToManyField(File, related_name='tasks', blank=True)
    def __str__(self):
        return self.title

class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='study_sessions')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    actual_duration = models.DurationField(null=True, blank=True)
    productivity_rating = models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Excellent')], null=True)
    notes = models.TextField(blank=True)
    reminder = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.course.name} - {self.start_time.date()}"

class LearningStyle(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    visual_score = models.IntegerField(default=0)
    auditory_score = models.IntegerField(default=0)
    reading_writing_score = models.IntegerField(default=0)
    kinesthetic_score = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.user.username}'s Learning Style"
    
    

class PomodoroSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='pomodoro_sessions')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Pomodoro for {self.task.title} - {self.start_time.date()}"