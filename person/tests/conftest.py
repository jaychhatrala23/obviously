import pytest
from django.contrib.auth import get_user_model

from person.models import Role

User = get_user_model()


@pytest.fixture
def roles():
    """
    Fixture to get 'admin' and 'guest' roles before running any tests.
    """
    # As we have a data migration which is loaded on running the server or starting tests
    # we are fetching the roles here, otherwise create those roles to be used in tests
    admin_role = Role.objects.get(name="admin")
    guest_role = Role.objects.get(name="guest")
    return {"admin": admin_role, "guest": guest_role}


@pytest.fixture
def admin_user():
    """
    Fixture to return admin user
    """
    return User.objects.get(
        username="jaychhatrala-admin"
    )


@pytest.fixture
def guest_user():
    """
    Fixture to return admin user
    """
    return User.objects.get(
        username="jaychhatrala-guest"
    )

