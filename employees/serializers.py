from rest_framework import serializers
from .models import Operator

class EmployeeRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = ['firstname', 'lastname', 'email','password','phone','password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'phone': {'required': True},
            'firstname': {'required': True},
            'lastname': {'required': True},
        }

