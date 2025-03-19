from django.contrib import admin
from .models import Customer, CustomerToken
from django.utils.translation import gettext_lazy as _

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ( 'password','firstname','lastname','phone')
    readonly_fields = ('DOB',)

@admin.register(CustomerToken)
class CustomerTokenAdmin(admin.ModelAdmin):
    list_display = ("customer", "key", "created")


admin.site.site_header = _("UrSpace Manager")
admin.site.site_title = _("UrSpace Manager")
admin.site.index_title = _("Welcome to UrSpace Management System")
