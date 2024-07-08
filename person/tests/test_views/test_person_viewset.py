import pytest
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status

from rest_framework.test import APIClient


@pytest.mark.django_db
class TestPersonAPI:
    url = '/persons/'

    @pytest.fixture(autouse=True)
    def setup_method(self, roles, admin_user, guest_user):
        """
        Setup common test data and configurations before each test method.
        Creates 'admin' and 'guest' roles only once per test case run.
        """
        self.admin_role = roles["admin"]
        self.guest_role = roles["guest"]
        self.admin_user = admin_user
        self.guest_user = guest_user
        self.api_client = APIClient()

    def test_admin_access(self):
        """
        Test that users with 'admin' role can access the person listing endpoint.
        """
        self.api_client.force_authenticate(user=self.admin_user)
        response = self.api_client.get(self.url)
        assert response.status_code == 200

    def test_guest_access(self):
        """
        Test that users with 'guest' role cannot access the person listing endpoint.
        """
        self.api_client.force_authenticate(user=self.guest_user)
        response = self.api_client.get(self.url)
        assert response.status_code == 403

    def test_create_person(self):
        """
        Test creation of a new person via the API by an admin user.
        """
        self.api_client.force_authenticate(user=self.admin_user)
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newsecurepassword',
            'first_name': 'New',
            'last_name': 'User',
            'phone': "+14155552671",
            'date_of_birth': "1990-01-01",
            'role': self.admin_user.role.id
        }
        response = self.api_client.post(self.url, data, format='json')
        print(response.json())
        assert response.status_code == 201

    def test_update_person(self):
        """
        Test updating an existing person's details via the API by an admin user.
        """
        self.api_client.force_authenticate(user=self.admin_user)
        new_email = 'updated@example.com'
        response = self.api_client.patch(f"{self.url}{self.guest_user.id}/", {'email': new_email}, format='json')
        assert response.status_code == 200
        self.guest_user.refresh_from_db()
        assert self.guest_user.email == new_email

    def test_delete_person(self):
        """
        Test the deletion of an existing person via the API by an admin user.
        """
        self.api_client.force_authenticate(user=self.admin_user)
        response = self.api_client.delete(f"{self.url}{self.guest_user.id}/")
        assert response.status_code == 204


@pytest.mark.django_db
class TestPersonSearchAPI:
    url = reverse('person-search')

    @pytest.fixture(autouse=True)
    def setup(self, roles, admin_user, guest_user):
        """
        Fixture to set up roles ('admin' and 'guest') and create test users before each test method runs.
        """
        self.admin_role = roles['admin']
        self.guest_role = roles['guest']
        self.admin_user = admin_user
        self.guest_user = guest_user
        self.api_client = APIClient()

    def test_search_by_first_name(self):
        """
        Test filtering by first_name for an authenticated admin user.
        """
        self.api_client.force_authenticate(user=self.admin_user)
        response = self.api_client.get(self.url, {'first_name': 'Jay'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2  # Expecting both admin and guest users

    def test_search_by_last_name(self):
        """
        Test filtering by last_name for an authenticated admin user.
        """
        self.api_client.force_authenticate(user=self.admin_user)
        response = self.api_client.get(self.url, {'last_name': 'Chhatrala'})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2  # Expecting both admin and guest users

    @freeze_time("2024-01-01")
    def test_search_by_age(self):
        """
        Test filtering by age for an authenticated admin user.
        """
        self.api_client.force_authenticate(user=self.admin_user)
        response = self.api_client.get(self.url, {'age': 34})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2  # Expecting both admin and guest users

    def test_guest_access(self):
        """
        Test that a guest user can access the search endpoint.
        """
        self.api_client.force_authenticate(user=self.guest_user)
        response = self.api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK

    def test_unauthenticated_access(self):
        """
        Test that an unauthenticated user cannot access the search endpoint.
        """
        url = reverse('person-search')
        response = self.api_client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
