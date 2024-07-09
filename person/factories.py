import factory
from django.contrib.auth import get_user_model
from person.models import Role

User = get_user_model()


class RoleFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Role instances.
    """
    class Meta:
        model = Role

    name = factory.Iterator(['admin', 'guest'])


class PersonFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Person instances.
    """
    class Meta:
        model = User

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    date_of_birth = factory.Faker('date_of_birth', minimum_age=18, maximum_age=65)
    phone = factory.Faker('phone_number')
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')
    role = factory.SubFactory(RoleFactory)

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.set_password(extracted)
        else:
            self.set_password('defaultpassword')
