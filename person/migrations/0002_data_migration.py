from django.db import migrations


def create_roles_and_persons(apps, schema_editor):
    """
    Data migration script that will create admin & guest roles, and a person each for each role
    """
    Role = apps.get_model('person', 'Role')
    admin_role = Role.objects.create(name='admin')
    guest_role = Role.objects.create(name='guest')

    Person = apps.get_model('person', 'Person')
    Person.objects.create_user(
        username="jaychhatrala-admin",
        email="jay@example.com",
        password="securepassword123",
        first_name="Jay",
        last_name="Chhatrala",
        phone="+14155552671",
        date_of_birth="1990-01-01",
        role=admin_role,
    )
    Person.objects.create_user(
        username="jaychhatrala-guest",
        email="jay@example.com",
        password="securepassword123",
        first_name="Jay",
        last_name="Chhatrala",
        phone="+14155552671",
        date_of_birth="1990-01-01",
        role=guest_role,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_roles_and_persons),
    ]
