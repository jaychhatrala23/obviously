import pytest
from person.models import Role


@pytest.fixture
def roles():
    """
    Fixture to create 'admin' and 'guest' roles before running any tests.
    """
    # Create admin and guest roles
    admin_role = Role.objects.create(name="admin")
    guest_role = Role.objects.create(name="guest")
    return {"admin": admin_role, "guest": guest_role}
