from shortuuid.django_fields import ShortUUIDField
from django.db import models
from doctor.models import Doctor
from pacient.models import Pacient
from decimal import Decimal

class Service(models.Model):
    image = models.FileField(upload_to='images/', null=True, blank=True)
    name = models.CharField(max_length=120, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    cost = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    available = models.ManyToManyField(Doctor, blank=True)

    def __str__(self):
        return f'{self.name} - {self.cost}'

class Appointment(models.Model):
    STATUS_CHOICES = (
    ("Запланировано", "Запланировано"),
    ("Выполнено", "Выполнено"),
    ("Рассматривается", "Рассматривается"),
    ("Отменено", "Отменено")
    )

    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='service_appointment')

    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='doctor_appointment')

    pacient = models.ForeignKey(Pacient, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='pacient_appointment')

    appointment_date = models.DateField(null=True, blank=True)
    issues = models.TextField(null=True, blank=True)
    symptoms = models.TextField(null=True, blank=True)
    appointment_id = ShortUUIDField(length=6, max_length=24, unique=True, alphabet='0123456789')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Запланировано')

    def __str__(self):
        return f'{self.pacient.full_name} - {self.doctor.full_name}'

class MedicalRecord(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField(null=True, blank=True)
    treatment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Медицинская запись для {self.appointment.pacient.full_name}'

class LabTest(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    test_name = models.CharField(max_length=200, null=True, blank=True)
    test_result = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.test_name

class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medication = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Предписание {self.appointment.pacient.full_name}'

class Billing(models.Model):
    pacient = models.ForeignKey(
        Pacient,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pacient_billing",
    )
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="appointment_billing",
    )
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(
        max_length=100,
        choices=(("Оплачено", "Оплачено"), ("Не оплачено", "Не оплачено")),
        default="Не оплачено",
    )
    billing_id = ShortUUIDField(
        length=6, max_length=10, unique=True, alphabet="0123456789"
    )
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Счет No {self.id} для {self.appointment.pacient.full_name}, сумма: {self.total}"



