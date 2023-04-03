from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import AnonymousUser        
# from django.contrib.auth import authenticate

from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import BaseAuthentication
from django.utils.translation import gettext_lazy as _
import requests
from config import settings


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, str):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth   

class CustomTokenAuthentication(BaseAuthentication):
    keyword = ['Token','bearer']
    def authenticate(self, request, token=None):
        
        auth = get_authorization_header(request).split()           

        if not auth or auth[0].lower() not in [k.lower().encode() for k in self.keyword]:
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)
        url = settings.AUTH_END_POINT+'token/verify/'

        resp = requests.post(url,data=({'token':token}))
        if resp.status_code == 200:
            user = ServerUser()
            return user, None
        else:
            return None, None


    def get_user(self, user_id):
        # Since there is no User model, always return AnonymousUser
        return AnonymousUser()


from django.contrib.auth.models import AnonymousUser

class ServerUser(AnonymousUser):

    @property
    def is_authenticated(self):
        # Always return True. This is a way to tell if
        # the user has been authenticated in permissions
        return True
