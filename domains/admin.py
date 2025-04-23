from django.contrib import admin
from .models import Domain, DomainInquiry

# Register your models here.
admin.site.register(Domain)

@admin.register(DomainInquiry)
class DomainInquiryAdmin(admin.ModelAdmin):
    list_display = ('domain', 'email', 'phone_number', 'offer', 'created_at')
    search_fields = ('domain__name', 'email', 'phone_number')