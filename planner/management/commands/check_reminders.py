from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from planner.models import Task, StudySession

class Command(BaseCommand):
    help = 'Check for upcoming reminders and send notifications'

    def handle(self, *args, **options):
        now = timezone.now()
        upcoming_time = now + timezone.timedelta(minutes=15)  # Check for reminders 15 minutes ahead

        # Check Tasks
        upcoming_tasks = Task.objects.filter(reminder__gte=now, reminder__lte=upcoming_time, completed=False)
        for task in upcoming_tasks:
            self.send_reminder_email(task.user.email, 'Task Reminder', f"Don't forget your task: {task.title}")

        # Check Study Sessions
        upcoming_sessions = StudySession.objects.filter(reminder__gte=now, reminder__lte=upcoming_time)
        for session in upcoming_sessions:
            self.send_reminder_email(session.user.email, 'Study Session Reminder', f"Your study session for {session.course.name} is starting soon!")

        self.stdout.write(self.style.SUCCESS('Successfully checked reminders'))

    def send_reminder_email(self, to_email, subject, message):
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            fail_silently=False,
        )