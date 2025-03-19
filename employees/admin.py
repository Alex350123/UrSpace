from django.contrib import admin
from .models import Operator, OperatorToken
# Register your models here.
@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ( 'email','firstname','lastname','firstname')

@admin.register(OperatorToken)
class OperatorTokenAdmin(admin.ModelAdmin):
    list_display = ("operator", "key", "created")
