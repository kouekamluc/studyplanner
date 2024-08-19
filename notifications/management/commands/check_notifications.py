from django.core.management.base import BaseCommand
from notifications.tasks import check_and_create_notifications

class Command(BaseCommand):
    help = 'Manually run the notification check and creation process'

    def handle(self, *args, **options):
        self.stdout.write("Starting notification check...")
        check_and_create_notifications()
        self.stdout.write(self.style.SUCCESS("Notification check completed successfully"))