from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import OperatorToken

class OperatorTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            print("Authorization header is missing.")
            return None

        # Clean up the header to remove potential quotes and extra whitespace
        auth_header = auth_header.strip().strip('"')
        print("OperatorTokenAuthentication, Authorization Header:", auth_header)  # print header for debug
        if not auth_header or not auth_header.startswith('Token '):
            print("it does not start with Token")
            return None

        token_key = auth_header.split(' ')[1].strip()
        try:
            token = OperatorToken.objects.get(key=token_key)
            print("Authenticated token:", token_key)
            print("Authenticated operator:", token.employee)
        except OperatorToken.DoesNotExist:
            print("No such token found in database:", token_key)
            raise AuthenticationFailed('invalid operator token')
        except Exception as e:
            print("Failed when seeking for token:", str(e))
            raise AuthenticationFailed('Failed when seeking for token')


        operator = token.employee
        operator.is_authenticated = True

        return (operator, token)