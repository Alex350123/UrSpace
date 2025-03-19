from django.contrib import admin
from .models import Customer, CustomerToken


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ( 'password','firstname','lastname','phone')
    readonly_fields = ('DOB',)

@admin.register(CustomerToken)
class CustomerTokenAdmin(admin.ModelAdmin):
    list_display = ("customer", "key", "created")
