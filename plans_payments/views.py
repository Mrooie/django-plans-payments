from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import TemplateView
from payments import get_payment_model, RedirectNeeded
from plans.models import Order, BillingInfo


def payment_details(request, payment_id):
    payment = get_object_or_404(get_payment_model(), id=payment_id)
    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))
    return TemplateResponse(request, 'plans_payments/payment.html',
                            {'form': form, 'payment': payment})


def create_payment(request, payment_variant, order_id):
    order = get_object_or_404(Order, pk=order_id)
    billing = BillingInfo.objects.get(user=request.user)
    Payment = get_payment_model()
    payment = Payment.objects.create(
        variant=payment_variant,
        order=order,
        description='Zamówienie: %s' % order.name,
        total=Decimal(order.total()),
        tax=Decimal(order.tax_total()),
        currency=order.currency,
        delivery=Decimal(0),
        billing_first_name=order.user.first_name,
        billing_last_name=order.user.last_name,
        billing_address_1=billing.street,
        billing_address_2="-",
        billing_city=billing.city,
        billing_postcode=billing.zipcode,
        billing_country_code=billing.country,
        billing_country_area="-",
        customer_ip_address=request.META.get("REMOTE_ADDR"))
    return redirect(reverse('payment_details', kwargs={'payment_id': payment.id}))
    return redirect(reverse('payment_details', kwargs={'payment_id': payment.id}))
