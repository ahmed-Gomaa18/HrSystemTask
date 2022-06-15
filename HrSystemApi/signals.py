from django.db.models.signals import post_save
from .models import Attendance
from django.dispatch import receiver

@receiver(post_save, sender=Attendance)
def post_save_attendance(sender, instance, created, **kwargs):
    # Check This attendance 
    if created == False:
        # Calculate work_hours
        instance.hours()
        # Calculate total_overtime_hours
        instance.get_overtime()
        print("Hello....")
        # Disconnect
        post_save.disconnect(post_save_attendance, sender=sender)
        # Save attendance
        instance.save()
        # Connect again
        post_save.connect(post_save_attendance, sender=sender)


