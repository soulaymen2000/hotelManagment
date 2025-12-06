from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def payment_form(request):
    """Payment form view"""
    # In a real application, you would fetch the booking from the database
    # For now, we'll just render the template
    return render(request, 'payments/payment_form.html')


@login_required
def payment_detail(request, payment_id):
    """Payment detail view"""
    # In a real application, you would fetch the payment from the database
    # For now, we'll just render the template
    return render(request, 'payments/payment_detail.html')