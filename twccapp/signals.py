# signals.py (for automatic sending when newsletter is published)
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Newsletter, Subscriber
from .utils import send_newsletter_email
from django.core.mail import EmailMessage

@receiver(post_save, sender=Newsletter)
def handle_newsletter_publishing(sender, instance, created, **kwargs):
    if instance.is_published and instance.send_to_subscribers:
        subscribers = Subscriber.objects.filter(is_active=True)
        for subscriber in subscribers:
            try:
                send_newsletter_email(subscriber, instance)
            except Exception as e:
                print(f"Failed to send newsletter to {subscriber.email}: {str(e)}")
        # Reset flag after sending
        Newsletter.objects.filter(pk=instance.pk).update(send_to_subscribers=False)