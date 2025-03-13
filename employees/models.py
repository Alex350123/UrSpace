from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
import binascii
import os
# Create your models here.
cipher =  Fernet(settings.FERNET_KEY.encode())

class Operator(models.Model):
    Operatorid = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique = True)
    phone = models.CharField(max_length=15)
    password = models.CharField(blank= False, max_length=100)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)

        self.firstname = cipher.encrypt(self.firstname.encode('utf-8').decode('utf-8'))
        self.lastname = cipher.encrypt(self.lastname.encode('utf-8').decode('utf-8'))
        self.phone = cipher.encrypt(self.phone.encode('utf-8').decode('utf-8'))
        super(Operator, self).save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def get_decrypted_firstname(self):
        return cipher.decrypt(self.firstname.encode('utf-8').decode('utf-8'))

    def get_decrypted_lastname(self):
        return cipher.decrypt(self.lastname.encode('utf-8').decode('utf-8'))

    def get_decrypted_phone(self):
        return cipher.decrypt(self.phone.encode('utf-8').decode('utf-8'))

    def __str__(self):
        return f"{self.get_decrypted_firstname()} {self.get_decrypted_lastname()}"

class OperatorToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    operator = models.OneToOneField(Operator, related_name="auth_token", on_delete=models.CASCADE)
    created =models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = binascii.hexlify(os.urandom(20)).decode('utf-8')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.key