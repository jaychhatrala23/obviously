import pytest
from person.models import Role


@pytest.fixture
def roles():
    """
    Fixture to create 'admin' and 'guest' roles before running any tests.
    """
    # As we have a data migration which is loaded on running the server or starting tests
    # we are fetching the roles here, otherwise create those roles to be used in tests
    admin_role = Role.objects.get(name="admin")
    guest_role = Role.objects.get(name="guest")
    return {"admin": admin_role, "guest": guest_role}
