

from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, F, Q
from django.contrib.auth.models import User
from planner.models import Task, StudySession, Course
from .models import Notification
from .utils import (
    create_task_due_notification,
    create_session_reminder_notification,
    create_progress_update_notification,
    create_streak_notification,
    calculate_streak
)

@shared_task
def check_and_create_notifications():
    now = timezone.now()
    
    # Task due notifications
    upcoming_tasks = Task.objects.filter(
        due_date__range=(now, now + timedelta(days=1)),
        completed=False
    ).select_related('user')
    
    for task in upcoming_tasks:
        create_task_due_notification(task)
    
    # Study session reminders
    upcoming_sessions = StudySession.objects.filter(
        start_time__range=(now, now + timedelta(hours=1))
    ).select_related('user', 'course')
    
    for session in upcoming_sessions:
        create_session_reminder_notification(session)
    
    # Progress updates (weekly updates)
    if now.weekday() == 6:  # Sunday
        courses = Course.objects.annotate(
            total_tasks=Count('tasks'),
            completed_tasks=Count('tasks', filter=F('tasks__completed')==True)
        ).select_related('user')
        
        for course in courses:
            progress = (course.completed_tasks / course.total_tasks) * 100 if course.total_tasks > 0 else 0
            create_progress_update_notification(course.user, course, progress)
    
    # Streak notifications
    users = User.objects.annotate(streak=calculate_streak(F('id')))
    for user in users:
        if user.streak > 0 and user.streak % 7 == 0:  # Notify on every 7-day milestone
            create_streak_notification(user, user.streak)

def calculate_streak(user_id):
    # This is a placeholder function. You need to implement the actual streak calculation logic.
    # It should return a database expression that calculates the streak for a given user.
    return 7



@shared_task
def cleanup_old_notifications():
    thirty_days_ago = timezone.now() - timedelta(days=30)
    Notification.objects.filter(created_at__lt=thirty_days_ago, read=True).delete()

