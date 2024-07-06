import pytest
from person.models import Role


@pytest.mark.django_db
class TestRoleModel:
    def test_role_creation(self, roles):
        """
        Test that the admin role can be created and exists.
        """
        admin_role = roles["admin"]
        assert admin_role.name == "admin"

    def test_role_str_method(self, roles):
        """
        Test the string representation of the Role model.
        """
        guest_role = roles["guest"]
        assert str(guest_role) == "guest"

    def test_role_name_unique(self, roles):
        """
        Test that Role names must be unique.
        """
        # Check that a unique constraint exception is raised
        with pytest.raises(Exception):
            # This should fail due to the unique constraint as admin already exists
            Role.objects.create(name="admin")
