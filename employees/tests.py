from django.test import TestCase
from django.utils import timezone
from .models import Operator, OperatorToken

class OperatorModelTest(TestCase):
    def setUp(self):
        self.operator = Operator.objects.create(
            firstname="John",
            lastname="Doe",
            email="johndoe@example.com",
            phone="1234567890",
            password="securepassword123"
        )
        self.operator.save()

    def test_encryption_and_password(self):
        # 测试加密和密码验证功能
        operator = Operator.objects.get(email="johndoe@example.com")
        # 验证数据是否被加密
        self.assertNotEqual(operator.firstname, "John")
        self.assertNotEqual(operator.lastname, "Doe")
        self.assertNotEqual(operator.phone, "1234567890")
        # 验证数据解密
        self.assertEqual(operator.get_decrypted_firstname(), "John")
        self.assertEqual(operator.get_decrypted_lastname(), "Doe")
        self.assertEqual(operator.get_decrypted_phone(), "1234567890")
        # 验证密码校验
        self.assertTrue(operator.check_password("securepassword123"))

    def test_str_method(self):
        # 测试 __str__ 方法返回正确的解密姓名
        self.assertEqual(self.operator.__str__(), "John Doe")

class OperatorTokenModelTest(TestCase):
    def setUp(self):
        self.operator = Operator.objects.create(
            firstname="Alice",
            lastname="Wonderland",
            email="alice@example.com",
            phone="0987654321",
            password="wonderland123"
        )
        self.token = OperatorToken(operator=self.operator)
        self.token.save()

    def test_token_creation(self):
        # 测试 Token 自动创建和保存
        # 验证 Token 是否被正确创建
        self.assertTrue(self.token.key)
        self.assertIsInstance(self.token.key, str)
        self.assertGreater(len(self.token.key), 0)

    def test_token_str(self):
        # 测试 Token 的 __str__ 方法
        self.assertEqual(self.token.__str__(), self.token.key)

