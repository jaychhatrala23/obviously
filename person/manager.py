from datetime import datetime

from django.contrib.auth.models import UserManager


class PersonManager(UserManager):
    """
    Custom manager for the Person model.

    This manager overrides the default create_user method to ensure that
    the date_of_birth field is correctly handled as a date object, even if
    it's provided as a string, and raise ValueError if password is None.
    """

    def create_user(self, username, email, password=None, **extra_fields):
        if not password:
            raise ValueError("Password must be set")
        if "date_of_birth" in extra_fields:
            date_of_birth = extra_fields["date_of_birth"]
            if isinstance(date_of_birth, str):
                extra_fields["date_of_birth"] = datetime.strptime(
                    date_of_birth, "%Y-%m-%d"
                ).date()
        return super().create_user(username, email, password, **extra_fields)
