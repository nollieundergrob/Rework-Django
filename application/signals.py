from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils.timezone import now
from .models import AttendanceRecord

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    AttendanceRecord.objects.create(
        user=user,
        timestamp=now(),
        ip_address=request.META.get('REMOTE_ADDR', 'Unknown'),
        user_agent=request.META.get('HTTP_USER_AGENT', 'Unknown'),
        request_method=request.method,
        request_url=request.build_absolute_uri(),
        headers={k: v for k, v in request.headers.items()},
    )
