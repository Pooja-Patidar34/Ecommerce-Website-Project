from background_task import background
from django.utils import timezone
from datetime import timedelta
from .models import CartItem

@background(schedule=60)  # run every 60 seconds
def clear_old_cart_items():
    expiry_time = timezone.now() - timedelta(seconds=5)
    deleted_count, _ = CartItem.objects.filter(created_at__lt=expiry_time).delete()
    print(f"🗑️ Deleted {deleted_count} old cart items")