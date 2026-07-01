from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.conf import settings
from pacient.models import Pacient
from doctor.models import Doctor
from base.models import Service, Appointment, Billing
from pacient.models import Notification as PacientNotification
from pacient.models import Notification


def index_view(request):
    services = Service.objects.all()
    context = {"services": services}
    return render(request, 'base/index.html', context)

def service_detail_view(request, service_id):
    service = Service.objects.get(id=service_id)
    context = {"service": service}
    return render(request, 'base/service_detail.html', context)

@login_required
def book_appointment(request, service_id, doctor_id):
    service = Service.objects.get(id=service_id)
    doctor = Doctor.objects.get(id=doctor_id)
    pacient = Pacient.objects.get(user=request.user)


    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        adress = request.POST.get('adress')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        issues = request.POST.get('issues')
        symptoms = request.POST.get('symptoms')

        pacient.full_name = full_name
        pacient.email = email
        pacient.mobile = mobile
        pacient.adress = adress
        pacient.gender = gender
        pacient.dob = dob
        pacient.save()

        appointment = Appointment.objects.create(
            pacient = pacient,
            doctor = doctor,
            service = service,
            issues = issues,
            symptoms = symptoms,
            appointment_date = doctor.next_appointment_date
        )

        billing = Billing()
        billing.appointment = appointment
        billing.pacient = pacient
        billing.sub_total = appointment.service.cost
        billing.tax = appointment.service.cost * 13/100
        billing.total = billing.sub_total + billing.tax
        billing.status = 'Не оплачено'
        billing.save()

        return redirect('base:checkout', billing.billing_id)


    context = {'service': service, 'doctor': doctor, 'pacient': pacient}
    return render(request, 'base/book_appointment.html', context)

@login_required
def checkout_view(request, billing_id):
    billing = Billing.objects.get(billing_id=billing_id)
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    context = {'billing': billing, "stripe_public_key": stripe_public_key}
    return render(request, 'base/checkout.html', context)

@csrf_exempt
def stripe_payment(request, billing_id):
    billing = Billing.objects.get(billing_id=billing_id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email=billing.pacient.email,
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "Оплата" + billing.pacient.full_name,
                    },
                    "unit_amount": int(billing.total * 100),
                },
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse("base:stripe_payment_verify", args=[billing.billing_id])
        )
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(
            reverse("base:stripe_payment_verify", args=[billing.billing_id])
        ),
    )
    return JsonResponse({"sessionId": checkout_session.id})

@login_required
def stripe_payment_verify(request, billing_id):
    billing = Billing.objects.get(billing_id=billing_id)
    session_id = request.GET.get('session_id')

    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    payment_status = session.payment_status

    if payment_status == 'paid':
        if billing.status == 'Не оплачено':
            billing.status = 'Оплачено'
            billing.save()
            billing.appointment.status = 'Выполнено'
            billing.appointment.save()

            Notification.objects.create(
                doctor=billing.appointment.doctor,
                appointment=billing.appointment,
                category="Новая запись",
            )

            PacientNotification.objects.create(
                pacient=billing.appointment.pacient,
                appointment=billing.appointment,
                category='Запись создана'
            )
        # даже если уже "Оплачено", всё равно редиректим
        return redirect(f'/payment_status/{billing.billing_id}/?payment_status=paid')

    return redirect(f'/payment_status/{billing.billing_id}/?payment_status=failed')

@login_required
def payment_status_view(request, billing_id):
    billing = Billing.objects.get(billing_id=billing_id)
    payment_status = request.GET.get('payment_status')
    context = {'billing': billing, 'payment_status': payment_status}
    return render(request, 'base/payment_status.html', context)
