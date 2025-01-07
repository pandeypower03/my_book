import socket
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

def send_login_notification(user, request):
    if user.receive_login_notifications and user.email:
        # Get client IP
        client_ip = request.META.get('REMOTE_ADDR', 'Unknown')
        
        # Get user agent (browser/device info)
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown Device')
        
        subject = 'Login Notification'
        message = f"""
        Hello {user.username},

        A new login has been detected on your account:
        
        Time: {timezone.now()}
        IP Address: {client_ip}
        Device: {user_agent}
        
        If this wasn't you, please change your password immediately.
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            # Log the error or handle it as needed
            print(f"Email notification failed: {e}")