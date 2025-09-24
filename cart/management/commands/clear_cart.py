from django.core.management.base import BaseCommand
from django.utils import timezone
from cart.models import CartItem
import datetime
import os

class Command(BaseCommand):
    help = 'Remove cart items older than specific minutes'

    def handle(self, *args, **kwargs):
        # Set time threshold (example: 5 minutes old)
        time_threshold = timezone.now() - datetime.timedelta(minutes=5)

        old_items = CartItem.objects.filter(created_at__lt=time_threshold)
        count = old_items.count()
        old_items.delete()

        # ✅ Write log to file
        log_file = os.path.join("cart_cleanup.log")
        with open(log_file, "a") as f:
            f.write(f"[{timezone.now()}] Deleted {count} old cart items\n")

        # Also show in console
        self.stdout.write(self.style.SUCCESS(f"✅ Deleted {count} old cart items"))
