from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import TemplateView
from payments import get_payment_model, RedirectNeeded
from plans.models import Order


def payment_details(request, payment_id):
    payment = get_object_or_404(get_payment_model(), id=payment_id)
    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))
    return TemplateResponse(request, 'plans_payments/payment.html',
                            {'form': form, 'payment': payment})


def create_payment(request, data):
    order = get_object_or_404(Order, data[order].pk)
    Payment = get_payment_model()
    payment = Payment.objects.create(
        variant=data['variant'],
        order=order,
        description=data['description'],
        total=Decimal(data['total']),
        tax=Decimal(23),
        currency=order.currency,
        delivery=Decimal(0),
        billing_first_name=data['billing_first_name'],
        billing_last_name=data['billing_last_name'],
        billing_address_1=data['billing_address_1'],
        billing_address_2=data['billing_address_2'],
        billing_city=data['billing_city'],
        billing_postcode=data['billing_postcode'],
        billing_country_code=data['billing_country_code'],
        billing_country_area=data['billing_country_area'],
        customer_ip_address=data["customer_ip_address"]
    )
    return redirect(reverse('payment_details', kwargs={'payment_id': payment.id}))
