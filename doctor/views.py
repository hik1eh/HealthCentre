from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

from base import models as base_models
from doctor import models as doctor_models


@login_required
def dashboard(request):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(doctor=doctor)
    notifications = doctor_models.Notification.objects.filter(doctor=doctor)

    context = {
        'appointments': appointments,
        'notifications': notifications,
    }

    return render(request, 'doctor/dashboard.html', context)

@login_required
def appointments(request):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(doctor=doctor)

    context = {
        'appointments': appointments
    }

    return render(request, 'doctor/appointments.html', context)

@login_required
def appointment_detail(request, appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id,doctor=doctor)
    medical_record = base_models.MedicalRecord.objects.filter(appointment=appointment)
    lab_tests = base_models.LabTest.objects.filter(appointment=appointment)
    prescriptions = base_models.Prescription.objects.filter(appointment=appointment)

    context = {
        'appointment': appointment,
        'medical_record': medical_record,
        'lab_tests': lab_tests,
        'prescriptions': prescriptions,
    }

    return render(request, 'doctor/appointment_detail.html', context)

@login_required
def cancel_appointment(request, appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    appointment.status = 'Отменено'
    appointment.save()
    messages.success(request, 'Прием успешно отменен')

    return redirect('doctor:appointment_detail', appointment.appointment_id)

@login_required
def complete_appointment(request, appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    appointment.status = "Выполнено"
    appointment.save()
    messages.success(request, 'Прием успешно выполнен')

    return redirect('doctor:appointment_detail', appointment.appointment_id)

@login_required
def activate_appointment(request, appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    appointment.status = "Запланировано"
    appointment.save()
    messages.success(request, 'Прием успешно активирован')

    return redirect('doctor:appointment_detail', appointment.appointment_id)

@login_required
def add_medical_record(request, appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor = doctor)

    if request.method == 'POST':
        diagnosis = request.POST.get('diagnosis')
        treatment = request.POST.get('treatment')
        base_models.MedicalRecord.objects.create(
            appointment=appointment, diagnosis=diagnosis, treatment=treatment
        )

        messages.success(request, 'Медицинская запись успешно добавлена!')
        return redirect('doctor:appointment_detail', appointment.appointment_id)

@login_required
def edit_medical_record(request, appointment_id, medical_record_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id)
    medical_record = base_models.MedicalRecord.objects.get(id=medical_record_id, appointment=appointment)

    if request.method == 'POST':
        diagnosis = request.POST.get('diagnosis')
        treatment = request.POST.get('treatment')
        medical_record.diagnosis = diagnosis
        medical_record.treatment = treatment
        medical_record.save()

        messages.success(request, 'Запись успешно обновлена!')
        return redirect('doctor:appointment_detail', appointment.appointment_id)

@login_required
def add_lab_test(request, appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor = doctor)
    if request.method == 'POST':
        test_name = request.POST.get('test_name')
        description = request.POST.get('description')
        result = request.POST.get('result')
        base_models.LabTest.objects.create(
            appointment=appointment, test_name=test_name, description=description, result=result
        )
        messages.success(request, 'Лабораторный тест добавлен!')
        return redirect('doctor:appointment_detail', appointment.appointment_id)

@login_required
def edit_lab_test(request, appointment_id, lab_test_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id)
    lab_test = base_models.LabTest.objects.get(id=lab_test_id, appointment=appointment)

    if request.method == 'POST':
        test_name = request.POST.get('test_name')
        description = request.POST.get('description')
        result = request.POST.get('result')
        lab_test.test_name = test_name
        lab_test.description = description
        lab_test.result = result
        lab_test.save()
        messages.success(request, 'Лабораторный тест успешно обновлен!')
        return redirect('doctor:appointment_detail', appointment.appointment_id)


@login_required
def add_prescription(request, appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, doctor=doctor
    )
    if request.method == "POST":
        medications = request.POST.get("medications")
        base_models.Prescription.objects.create(
            appointment=appointment, medication=medications
        )
    messages.success(request, "Предписание врача успешно добавлено")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def edit_prescription(request, appointment_id, prescription_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, doctor=doctor
    )
    prescription = base_models.Prescription.objects.get(
        id=prescription_id, appointment=appointment
    )
    if request.method == "POST":
        medications = request.POST.get("medications")
        prescription.medication = medications
        prescription.save()
    messages.success(request, "Предписание врача успешно обновлено")
    return redirect("doctor:appointment_detail", appointment.appointment_id)


@login_required
def payments(request):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    payments = base_models.Billing.objects.filter(appointment__doctor=doctor, status="Оплачено")
    context = {"payments": payments}
    return render(request, "doctor/payments.html", context)


@login_required
def notifications(request):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    notifications = doctor_models.Notification.objects.filter(doctor=doctor, seen=False)
    context = {"notifications": notifications}
    return render(request, "doctor/notifications.html", context)

@login_required
def mark_as_read_notifications(request, notification_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    notification = doctor_models.Notification.objects.get(id=notification_id, doctor=doctor)
    notification.seen = True
    notification.save()
    messages.success(request, 'Уведомление отмечено как прочитанное')
    return redirect('doctor:notifications')

@login_required
def profile(request):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    formatted_next_appointment_date = doctor.next_appointment_date.strftime("%d.%m.%Y")
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        image = request.FILES.get("image")
        phone = request.POST.get("phone")
        city = request.POST.get("city")
        bio = request.POST.get("bio")
        specialization = request.POST.get("specialization")
        qualification = request.POST.get("qualification")
        year_of_exp = request.POST.get("year_of_exp")
        next_appointment_date = request.POST.get("next_available_appointment_date")

        doctor.full_name = full_name
        doctor.image = image
        doctor.phone = phone
        doctor.city = city
        doctor.bio = bio
        doctor.specialization = specialization
        doctor.qualification = qualification
        doctor.year_of_exp = year_of_exp
        doctor.next_appointment_date = next_appointment_date

        if image != None:
            doctor.image = image

        doctor.save()
        messages.success(request, 'Профиль обновлен!')
        return redirect('doctor:profile')

    context={'doctor':doctor, 'formatted_next_appointment_date':formatted_next_appointment_date}
    return render(request, "doctor/profile.html", context)

