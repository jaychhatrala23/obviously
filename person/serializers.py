from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class PersonSerializer(serializers.ModelSerializer):
    """
    Serializer to handle CRUD operations with PersonViewSet
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'role', 'age', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def to_representation(self, instance):
        """
        Modify the output to hide sensitive data.
        """
        ret = super().to_representation(instance)
        ret.pop('password', None)  # Ensure password is not sent back to the client
        return ret


class PersonSearchSerializer(serializers.ModelSerializer):
    """
    Serializer to handle search operations with PersonViewSet Search api
    """
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'role', 'age']
