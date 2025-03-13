from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from customers.models import Customer

class RegisterCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['firstname', 'lastname', 'email', 'password', 'phone', 'DOB',]
        extra_kwargs = {'password': {'write_only': True},
                        'lastname': {'required': True},
                        'firstname': {'required': True},
                        'email': {'required': True},
                        'DOB': {'required': True},
                        'phone': {'required': True},
                        }


class LoadCustomerSerializer(serializers.ModelSerializer):
    firstname = serializers.SerializerMethodField()
    lastname = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['Customerid', 'firstname', 'lastname', 'email', 'DOB', 'phone', ]

    def get_firstname(self, obj):
        return obj.get_decrypted_firstname()

    def get_lastname(self, obj):
        return obj.get_decrypted_lastname()

    def get_phone(self, obj):
        return obj.get_decrypted_phone()
