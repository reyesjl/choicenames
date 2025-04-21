from django.shortcuts import redirect, render
from django.db.models import Q
from .models import Domain

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

