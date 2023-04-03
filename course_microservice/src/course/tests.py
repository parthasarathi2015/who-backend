import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest import mock
from config import settings

client = APIClient()

@pytest.mark.django_db
class TestCourseListView:

    def test_course_list_view_with_authentication(self):
        url = reverse('course-list')
        client.credentials(HTTP_AUTHORIZATION=f'Token {settings.CUSTOM_TOKEN}')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_course_list_view_without_authentication(self):
        url = reverse('course-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestAuthenticateUserView:

    def test_authenticate_user_view_with_valid_token(self):
        url = reverse('authenticate-user')
        client.credentials(HTTP_AUTHORIZATION=f'Token {settings.CUSTOM_TOKEN}')
        response = client.get(url)
        assert response.data == True
        assert response.status_code == status.HTTP_200_OK

    def test_authenticate_user_view_with_invalid_token(self):
        url = reverse('authenticate-user')
        client.credentials(HTTP_AUTHORIZATION='Token abcdefghijklmnopqrstuvwxyz')
        response = client.get(url)
        assert response.data == False
        assert response.status_code == status.HTTP_200_OK

