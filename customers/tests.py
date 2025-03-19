from django.test import TestCase
from .models import Customer, CustomerToken
from django.utils import timezone

class CustomerModelTest(TestCase):
    def test_create_customer_and_encrypt_data(self):

        customer = Customer(
            firstname="John",
            lastname="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            DOB=timezone.now().date(),
            password="testpassword123"
        )
        customer.save()


        saved_customer = Customer.objects.get(email="john.doe@example.com")
        self.assertTrue(saved_customer.check_password("testpassword123"))
        self.assertNotEqual(saved_customer.firstname, "John")  # 加密后的数据应不同
        self.assertNotEqual(saved_customer.lastname, "Doe")
        self.assertNotEqual(saved_customer.phone, "1234567890")
        self.assertEqual(saved_customer.get_decrypted_firstname(), "John")
        self.assertEqual(saved_customer.get_decrypted_lastname(), "Doe")
        self.assertEqual(saved_customer.get_decrypted_phone(), "1234567890")

    def test_decryption_and_str_method(self):

        customer = Customer(
            firstname="Jane",
            lastname="Smith",
            email="jane.smith@example.com",
            phone="0987654321",
            DOB=timezone.now().date(),
            password="mypassword456"
        )
        customer.save()
        saved_customer = Customer.objects.get(email="jane.smith@example.com")
        self.assertEqual(saved_customer.__str__(), "Jane Smith")

class CustomerTokenModelTest(TestCase):
    def test_token_creation(self):

        customer = Customer(
            firstname="Alice",
            lastname="Wonderland",
            email="alice@example.com",
            phone="1112223333",
            DOB=timezone.now().date(),
            password="alicepassword"
        )
        customer.save()
        token = CustomerToken(customer=customer)
        token.save()


        saved_token = CustomerToken.objects.get(customer=customer)
        self.assertEqual(saved_token.customer, customer)
        self.assertTrue(saved_token.key)
        self.assertIsInstance(saved_token.key, str)
        self.assertGreater(len(saved_token.key), 0)

