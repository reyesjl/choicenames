from django.db import models

class Domain(models.Model):
    name = models.CharField(max_length=255, unique=True)
    ask_price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_price = models.DecimalField(max_digits=10, decimal_places=2)
    initial_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    lock_state = models.CharField(max_length=50, null=True, blank=True)
    privacy = models.BooleanField(default=False)
    status = models.CharField(max_length=100, null=True, blank=True)
    hosting_plan = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
