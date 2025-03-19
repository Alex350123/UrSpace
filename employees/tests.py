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

        operator = Operator.objects.get(email="johndoe@example.com")

        self.assertNotEqual(operator.firstname, "John")
        self.assertNotEqual(operator.lastname, "Doe")
        self.assertNotEqual(operator.phone, "1234567890")

        self.assertEqual(operator.get_decrypted_firstname(), "John")
        self.assertEqual(operator.get_decrypted_lastname(), "Doe")
        self.assertEqual(operator.get_decrypted_phone(), "1234567890")

        self.assertTrue(operator.check_password("securepassword123"))

    def test_str_method(self):

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

        self.assertTrue(self.token.key)
        self.assertIsInstance(self.token.key, str)
        self.assertGreater(len(self.token.key), 0)

    def test_token_str(self):
        self.assertEqual(self.token.__str__(), self.token.key)

