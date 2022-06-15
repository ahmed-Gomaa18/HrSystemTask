from django.db import models
from django.contrib.auth.models import User

from datetime import datetime
# Create your models here.

class Attendance(models.Model):

    employee = models.ForeignKey(User, null=True, blank=True, related_name="attendance", on_delete=models.CASCADE)
    total_overtime_hours = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    work_hours = models.FloatField(default=0)
    arrive = models.CharField(max_length=100, default="Arrive on time")
    leave = models.CharField(max_length=100, default="Leave on time")
    day = models.CharField(max_length=20, default=datetime.now().strftime('%A'))

    def __str__(self) -> str:
        return f"ID: {self.pk} Attendance Day {self.day} check-in:{self.check_in} & check-out:{self.check_out}"

    # Get work_hours
    def hours(self):
        # if employee check-in-again
        if self.check_out == None:
            return self.work_hours
        else:
            end = self.check_out.hour*60 + self.check_out.minute
            start = self.check_in.hour*60 + self.check_in.minute
            self.work_hours += round(float((end - start ) / 60), 1)
            return self.work_hours
    
    # Get total_overtime_hours
    def get_overtime(self):
        # if employee check-in-again
        if self.check_out == None:
            return self.work_hours
        elif str(self.day) in ['Friday', 'Saturday']:
            self.total_overtime_hours = round(self.work_hours, 1)
            return self.total_overtime_hours
        elif self.work_hours > 8:
            self.total_overtime_hours = round(float(self.work_hours - 8), 1)
            return self.total_overtime_hours


