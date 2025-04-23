from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from .models import Domain, DomainInquiry

def index(request):
    """
    Index of all domains.
    """
    filter_letter = request.GET.get('filter', None)
    if filter_letter == 'all' or not filter_letter:
        domains = Domain.objects.all()
        filter_letter = 'all'  # Ensure 'all' is passed to the template for highlighting
    elif filter_letter.isalpha() and len(filter_letter) == 1:
        domains = Domain.objects.filter(name__istartswith=filter_letter)
    else:
        domains = Domain.objects.all()

    context = {
        'domains': domains,
        'active_filter': filter_letter,
    }

    return render(request, 'domains.index.html', context)

def show(request, id):
    """
    Show one domain.
    """
    domain = Domain.objects.get(id=id)
    context = {
        'domain': domain,
    }

    return render(request, 'domains.show.html', context)

def create(request):
    """
    Create a new domain.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        domain = Domain(name=name, description=description)
        domain.save()
        return redirect('index')

    return render(request, 'domains.create.html')

def update(request, id):
    """
    Update a domain.
    """
    domain = Domain.objects.get(id=id)

    if request.method == 'POST':
        domain.name = request.POST.get('name')
        domain.description = request.POST.get('description')
        domain.save()
        return redirect('index')

    context = {
        'domain': domain,
    }

    return render(request, 'domains.update.html', context)

def delete(request, id):
    """
    Delete a domain.
    """
    domain = Domain.objects.get(id=id)
    domain.delete()
    return redirect('index')

def submit_inquiry(request, domain_id):
    if request.method == 'POST':
        honeypot = request.POST.get('honeypot', '')
        if honeypot:  # If honeypot is filled, reject the submission
            return HttpResponseBadRequest("Invalid submission.")
        
        domain = get_object_or_404(Domain, id=domain_id)
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        offer = request.POST.get('offer')

        DomainInquiry.objects.create(
            domain=domain,
            email=email,
            phone_number=phone_number,
            offer=offer
        )
        messages.success(request, "Your inquiry has been submitted successfully.")
        return redirect('domains:show', id=domain_id)

