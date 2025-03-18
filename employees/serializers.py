from rest_framework import serializers
from .models import Operator

class OperatorRegisterSerializer(serializers.ModelSerializer):
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

class LoadOperatorSerializer(serializers.ModelSerializer):
    firstname = serializers.SerializerMethodField()
    lastname = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    class Meta:
        model = Operator
        fields = ['Operatorid', 'firstname', 'lastname', 'email', 'DOB', 'phone', ]

    def get_firstname(self, obj):
        return obj.get_decrypted_firstname()

    def get_lastname(self, obj):
        return obj.get_decrypted_lastname()

    def get_phone(self, obj):
        return obj.get_decrypted_phone()