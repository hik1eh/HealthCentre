from django.db import models
from django.utils import timezone
from authuser.models import User

NOTIFICATION_CHOICES = (
    ("Новая запись", "Новая запись"),
    ("Отмена записи", "Отмена записи")

)

class Doctor(models.Model):
    user = models.OneToOneField(User, max_length=100, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='doctor/images/', null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    year_of_exp = models.CharField(max_length=100, null=True, blank=True)
    next_appointment_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'Doctor {self.full_name}'

class Notification(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    appointment = models.ForeignKey("base.Appointment", on_delete=models.CASCADE, null=True, blank=True, related_name='doctor_appoinment_notifications')
    category = models.CharField(max_length=100, choices=NOTIFICATION_CHOICES)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Doctor {self.full_name} - Уведомление'



