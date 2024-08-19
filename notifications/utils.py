
from django.utils import timezone
from .models import Notification

from django.db.models import Count, F, Q
from django.db.models.functions import TruncDate
from planner.models import Task, StudySession

def create_task_due_notification(task):
    Notification.objects.create(
        user=task.user,
        notification_type='task_due',
        title=f"Task Due: {task.title}",
        message=f"Your task '{task.title}' is due soon.",
        content_object=task
    )

def create_session_reminder_notification(session):
    Notification.objects.create(
        user=session.user,
        notification_type='session_reminder',
        title=f"Upcoming Study Session: {session.course.name}",
        message=f"You have a study session for '{session.course.name}' starting soon.",
        content_object=session
    )

def create_progress_update_notification(user, course, progress):
    Notification.objects.create(
        user=user,
        notification_type='progress_update',
        title=f"Progress Update: {course.name}",
        message=f"You've completed {progress}% of '{course.name}'. Keep up the good work!",
        content_object=course
    )


def create_streak_notification(user, streak_days):
    # Check if a streak notification for this milestone has already been created
    existing_notification = Notification.objects.filter(
        user=user,
        notification_type='streak',
        message__contains=f"{streak_days}-day study streak"
    ).exists()

    if not existing_notification:
        Notification.objects.create(
            user=user,
            notification_type='streak',
            title="Study Streak!",
            message=f"Congratulations! You've maintained a {streak_days}-day study streak. Keep it up!"
        )

def create_custom_notification(user, title, message):
    Notification.objects.create(
        user=user,
        notification_type='custom',
        title=title,
        message=message
    )
    
    

def calculate_streak(user_id):
    # Get all study sessions for the user, ordered by date
    sessions = StudySession.objects.filter(user_id=user_id).annotate(
        date=TruncDate('start_time')
    ).values('date').distinct().order_by('-date')

    # Calculate the streak
    streak = 0
    last_date = None
    for session in sessions:
        if last_date is None:
            streak = 1
        elif (last_date - session['date']).days == 1:
            streak += 1
        else:
            break
        last_date = session['date']

    return streak
