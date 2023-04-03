# permissions.py

import requests
from rest_framework.permissions import BasePermission
from config import settings


class AuthTokenPermission(BasePermission):
    def has_permission(self, request, view):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return False
        else:
            return True
