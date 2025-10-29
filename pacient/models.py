from django.db import models
from authuser.models import User
from django.utils import timezone

NOTIFICATION_CHOICES = (
    ("Запись создана", "Запись создана"),
    ("Запись отменена", "Запись отменена"),
)


class Pacient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='images', null=True, blank=True)
    full_name = models.CharField(max_length=120,null=True, blank=True)
    email = models.CharField(max_length=120, null=True, blank=True)
    mobile = models.CharField(max_length=120,null=True, blank=True)
    address = models.CharField(max_length=120,null=True, blank=True)
    gender = models.CharField(max_length=120,null=True, blank=True)
    blood_group = models.CharField(max_length=120,null=True, blank=True)
    dob = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name

class Notification(models.Model):
    pacient = models.ForeignKey(Pacient, on_delete=models.SET_NULL, null=True, blank=True)
    appointment = models.ForeignKey("base.Appointment", on_delete=models.CASCADE, null=True, blank=True, related_name='pacient_appointment_notifications')
    category = models.CharField(max_length=100, choices=NOTIFICATION_CHOICES)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Doctor {self.pacient.full_name} - Уведомление'



