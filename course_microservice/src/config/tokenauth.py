from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                _, token = auth_header.split()
                if token:
                    token_obj = Token.objects.get(key=token)
                    request.user = token_obj.user
                else:
                    request.user = None
            except (ValueError, Token.DoesNotExist, AuthenticationFailed):
                request.user = None

        response = self.get_response(request)
        return response

