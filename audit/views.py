from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def audit_log(request):
    """Audit log view"""
    # In a real application, you would fetch the audit logs from the database
    # For now, we'll just render the template
    return render(request, 'audit/audit_log.html')