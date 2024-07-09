from datetime import date

import factory
from django.db import migrations

from person.factories import PersonFactory, RoleFactory


def create_roles_and_persons(apps, schema_editor):
    """
    Data migration script that will create admin & guest roles, and a person each for each role
    """

    admin_role = RoleFactory(name="admin")
    guest_role = RoleFactory(name="guest")

    PersonFactory(username="jaychhatrala-admin",
                  email="jay@example.com",
                  password="securepassword123",
                  first_name="Jay",
                  last_name="Chhatrala",
                  date_of_birth=date(1990, 1, 1),
                  role=admin_role)

    PersonFactory(username="jaychhatrala-guest",
                  email="jay@example.com",
                  password="securepassword123",
                  first_name="Jay",
                  last_name="Chhatrala",
                  date_of_birth=date(1990, 1, 1),
                  role=guest_role)

    # Can use if we want to search using vector search with a dummy db
    # PersonFactory.create_batch(50, role=factory.Iterator([admin_role, guest_role]))


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0001_initial'),
        ('vectordb', '0002_vector_created_at_vector_updated_at_and_more'),
    ]

    operations = [
        migrations.RunPython(create_roles_and_persons),
    ]
