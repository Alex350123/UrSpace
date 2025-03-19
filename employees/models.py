from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
import binascii
import os

cipher = Fernet(settings.FERNET_KEY.encode())


class Operator(models.Model):
    Operatorid = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # 保持 email 唯一，不能加密
    phone = models.CharField(max_length=15)
    password = models.CharField(blank=False, max_length=100)

    def save(self, *args, **kwargs):
        """ 在保存到数据库之前进行加密 """
        if not self.pk:  # 仅在创建新用户时加密
            self.password = make_password(self.password)

        if not self.firstname.startswith("gAAAAA"):  # 避免重复加密
            self.firstname = cipher.encrypt(self.firstname.encode('utf-8')).decode()
        if not self.lastname.startswith("gAAAAA"):
            self.lastname = cipher.encrypt(self.lastname.encode('utf-8')).decode()
        if not self.phone.startswith("gAAAAA"):
            self.phone = cipher.encrypt(self.phone.encode('utf-8')).decode()

        super(Operator, self).save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def get_decrypted_firstname(self):
        """ 处理解密异常，防止程序崩溃 """
        try:
            return cipher.decrypt(self.firstname.encode()).decode('utf-8')
        except Exception:
            return "Decryption Failed"

    def get_decrypted_lastname(self):
        try:
            return cipher.decrypt(self.lastname.encode()).decode('utf-8')
        except Exception:
            return "Decryption Failed"

    def get_decrypted_phone(self):
        try:
            return cipher.decrypt(self.phone.encode()).decode('utf-8')
        except Exception:
            return "Decryption Failed"

    def __str__(self):
        return f"{self.get_decrypted_firstname()} {self.get_decrypted_lastname()}"


class OperatorToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    operator = models.OneToOneField(Operator, related_name="auth_token", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = binascii.hexlify(os.urandom(20)).decode('utf-8')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.key
