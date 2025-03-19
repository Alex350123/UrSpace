from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import OperatorToken

class OperatorTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        print("OperatorTokenAuthentication debug1: Authorization Header:", auth_header)  # print header for debug
        if not auth_header or not auth_header.startswith('Token '):
            return None

        token_key = auth_header.split(' ')[1]
        try:
            token = OperatorToken.objects.get(key=token_key)
            print("Authenticated token:", token_key)
            print("Authenticated operator:", token.operator)
        except OperatorToken.DoesNotExist:
            print("Invalid token")
            raise AuthenticationFailed('Invalid token')

        operator = token.operator
        operator.is_authenticated = True
        print("CustomerTokenAuthentication debug2: Authenticated operator:", token.operator)
        return (operator, token)