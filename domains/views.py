from django.shortcuts import redirect, render
from .models import Domain

def index(request):
    """
    Index of all domains.
    """
    domains = Domain.objects.all()
    context = {
        'domains': domains,
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

