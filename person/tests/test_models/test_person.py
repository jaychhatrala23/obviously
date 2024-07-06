import datetime

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from freezegun import freeze_time

from person.models import Role

User = get_user_model()


@pytest.mark.django_db
class TestPersonModel:
    @pytest.fixture(autouse=True)
    def setup_method(self, roles):
        """
        Set up the common data for Person model tests using the roles fixture.
        """
        self.role_admin = roles["admin"]
        self.role_guest = roles["guest"]

    def test_person_creation(self):
        """
        Test that a Person can be created with the correct attributes.
        """
        user = User.objects.create_user(
            username="jaychhatrala",
            email="jay@example.com",
            password="securepassword123",
            first_name="Jay",
            last_name="Chhatrala",
            phone="+14155552671",
            date_of_birth="1990-01-01",
            role=self.role_admin,
        )
        assert user.username == "jaychhatrala"
        assert user.email == "jay@example.com"
        assert user.first_name == "Jay"
        assert user.last_name == "Chhatrala"
        assert user.phone == "+14155552671"
        assert user.date_of_birth == datetime.date(1990, 1, 1)
        assert user.role == self.role_admin
        assert user.check_password("securepassword123") is True

    @freeze_time("2024-01-01")
    def test_person_age_computation(self):
        """
        Test that the age property is computed correctly.
        """
        user = User.objects.create_user(
            username="janedoe",
            email="jane@example.com",
            password="securepassword123",
            first_name="Jane",
            last_name="Doe",
            phone="+14155552672",
            date_of_birth="1990-01-01",
            role=self.role_guest,
        )
        assert user.age == 34  # Age is computed as 2024 - 1990

    def test_person_invalid_date_of_birth(self):
        """
        Test that the `age` property returns None if `date_of_birth` is not set.
        """
        user = User.objects.create_user(
            username="alexdoe",
            email="alex@example.com",
            password="securepassword123",
            first_name="Alex",
            last_name="Doe",
            phone="+14155552673",
            date_of_birth=None,  # No date of birth provided
            role=self.role_admin,
        )
        assert user.age is None

    def test_person_str_method(self):
        """
        Test the string representation of the Person model.
        """
        user = User.objects.create_user(
            username="jaychhatrala",
            email="jay@example.com",
            password="securepassword123",
            first_name="Jay",
            last_name="Chhatrala",
            phone="+14155552671",
            date_of_birth="1990-01-01",
            role=self.role_admin,
        )
        assert str(user) == "Jay Chhatrala"

    def test_person_missing_username(self):
        """
        Test that creating a Person without a username raises a ValueError.
        """
        with pytest.raises(ValueError):
            User.objects.create_user(
                username="",
                email="missingusername@example.com",
                password="securepassword123",
                first_name="Jay",
                last_name="Chhatrala",
                phone="+14155552671",
                date_of_birth="1990-01-01",
                role=self.role_admin,
            )

    def test_person_missing_password(self):
        """
        Test that creating a Person without a password raises a ValueError.
        """
        with pytest.raises(ValueError):
            User.objects.create_user(
                username="jaychhatrala",
                email="jay@example.com",
                password=None,  # Missing password
                first_name="Jay",
                last_name="Chhatrala",
                phone="+14155552671",
                date_of_birth="1990-01-01",
                role=self.role_admin,
            )

    def test_role_deletion_protected(self):
        """
        Test that deleting a Role with associated Person objects raises an error.
        """
        User.objects.create_user(
            username="jaychhatrala",
            email="jay@example.com",
            password="securepassword123",
            first_name="Jay",
            last_name="Chhatrala",
            phone="+14155552671",
            date_of_birth="1990-01-01",
            role=self.role_admin,
        )
        # Attempt to delete the role
        with pytest.raises(IntegrityError):
            self.role_admin.delete()

        # Ensure the role still exists
        assert Role.objects.filter(id=self.role_admin.id).exists()

    def test_role_deletion_without_person(self):
        """
        Test that deleting a Role without associated Person objects succeeds.
        """
        test_role = Role.objects.create(name="test")

        test_role.delete()

        # Ensure the role no longer exists
        assert not Role.objects.filter(id=test_role.id).exists()

    def test_invalid_phone_number(self):
        with pytest.raises(ValidationError):
            User.objects.create_user(
                username="jaychhatrala",
                email="jay@example.com",
                password="securepassword123",
                first_name="Jay",
                last_name="Chhatrala",
                phone="+invalid1223",   # Invalid Number
                date_of_birth="1990-01-01",
                role=self.role_admin,
            )
