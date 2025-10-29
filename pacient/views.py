from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import models

from pacient import models as pacient_models
from base import models as base_models

@login_required
def dashboard(request):
    pacient = pacient_models.Pacient.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(pacient=pacient)
    notifications = pacient_models.Notification.objects.filter(pacient=pacient)
    total_spent = base_models.Billing.objects.filter(pacient=pacient).aggregate(total_spent=models.Sum('total'))['total_spent']
    context = {
        'appointments': appointments,
        'notifications': notifications,
        'total_spent': total_spent,
    }

    return render(request, 'pacient/dashboard.html', context)

@login_required
def appointments(request):
    pacient = pacient_models.Pacient.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(pacient=pacient)

    context = {
        'appointments': appointments
    }

    return render(request, 'pacient/appointments.html', context)

@login_required
def appointment_detail(request, appointment_id):
    pacient = pacient_models.Pacient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id,pacient=pacient)
    medical_record = base_models.MedicalRecord.objects.filter(appointment=appointment)
    lab_tests = base_models.LabTest.objects.filter(appointment=appointment)
    prescriptions = base_models.Prescription.objects.filter(appointment=appointment)

    context = {
        'appointment': appointment,
        'medical_record': medical_record,
        'lab_tests': lab_tests,
        'prescriptions': prescriptions,
    }

    return render(request, 'pacient/appointment_detail.html', context)

@login_required
def cancel_appointment(request, appointment_id):
    pacient = pacient_models.Pacient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, pacient=pacient)
    appointment.status = 'Отменено'
    appointment.save()
    messages.success(request, 'Прием успешно отменен')

    return redirect('pacient:appointment_detail', appointment.appointment_id)

@login_required
def complete_appointment(request, appointment_id):
    pacient = pacient_models.Pacient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, pacient=pacient)
    appointment.status = "Выполнено"
    appointment.save()
    messages.success(request, 'Прием успешно выполнен')

    return redirect('pacient:appointment_detail', appointment.appointment_id)

@login_required
def activate_appointment(request, appointment_id):
    pacient = pacient_models.Pacient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, pacient=pacient)
    appointment.status = "Запланировано"
    appointment.save()
    messages.success(request, 'Прием успешно активирован')

    return redirect('pacient:appointment_detail', appointment.appointment_id)

@login_required
def payments(request):
    pacient = pacient_models.Pacient.objects.get(user=request.user)
    payments = base_models.Billing.objects.filter(appointment__pacient=pacient, status="Оплачено")
    context = {"payments": payments}
    return render(request, "pacient/payments.html", context)


@login_required
def notifications(request):
    pacient = pacient_models.Pacient.objects.get(user=request.user)
    notifications = pacient_models.Notification.objects.filter(pacient=pacient, seen=False)
    context = {"notifications": notifications}
    return render(request, "pacient/notifications.html", context)

@login_required
def mark_as_read_notifications(request, notification_id):
    pacient = pacient_models.Pacient.objects.get(user=request.user)
    notification = pacient_models.Notification.objects.get(id=notification_id, pacient=pacient)
    notification.seen = True
    notification.save()
    messages.success(request, 'Уведомление отмечено как прочитанное')
    return redirect('pacient:notifications')

@login_required
def profile(request):
    pacient = pacient_models.Pacient.objects.get(user=request.user)
    formatted_dob = pacient.dob.strftime("%d.%m.%Y")
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        image = request.FILES.get("image")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        blood_group = request.POST.get("blood_group")
        dob = request.POST.get("dob")

        pacient.full_name = full_name
        pacient.image = image
        pacient.mobile = mobile
        pacient.address = address
        pacient.gender = gender
        pacient.blood_group = blood_group
        pacient.dob = dob

        if image is not None:
            pacient.image = image

        pacient.save()
        messages.success(request, 'Профиль обновлен!')
        return redirect('pacient:profile')

    context={'pacient':pacient, 'formatted_dob':formatted_dob}
    return render(request, "pacient/profile.html", context)