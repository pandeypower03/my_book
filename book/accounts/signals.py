from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

@receiver(user_logged_in)
def send_login_notification(sender, user, request, **kwargs):
    print(f"Signal received for user: {user.username}")  # Debug print
    print(f"User email: {user.email}")  # Debug print
    
    if user.email:
        subject = 'New Login Alert'
        message = f"""
        Hello {user.username},
        We detected a new login to your account at {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}.
        """
        
        try:
            print("Attempting to send email...")  # Debug print
            print(f"From email: {settings.EMAIL_HOST_USER}")  # Debug print
            print(f"To email: {user.email}")  # Debug print
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
            print("Email sent successfully!")  # Debug print
        except Exception as e:
            print(f"Failed to send email. Error: {str(e)}")  # Debug print