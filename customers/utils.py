from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from customers.models import CustomerToken


class CustomerTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        print("CustomerTokenAuthentication debug1: Authorization Header:", auth_header)  # print header for debug
        if not auth_header or not auth_header.startswith('Token '):
            return None

        token_key = auth_header.split(' ')[1]
        try:
            token = CustomerToken.objects.get(key=token_key)
            print("Authenticated token:", token_key)
            print("Authenticated customer:", token.customer)
        except CustomerToken.DoesNotExist:
            print("Invalid token")
            raise AuthenticationFailed('Invalid token')

        customer = token.customer
        customer.is_authenticated = True
        print("CustomerTokenAuthentication debug2: Authenticated customer:", token.customer)
        return (customer, token)