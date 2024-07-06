from datetime import date
from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from person.manager import PersonManager


# Create your models here.


class Role(models.Model):
    """
    Role model to represent different roles within the application.

    Attributes:
    name (str): The name of the role. Unique identifier for the role.
    """

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Person(AbstractUser):
    """
    Custom user model that extends the AbstractUser model to include additional fields.

    Attributes:
    phone (PhoneNumberField): The phone number of the person.
    date_of_birth (DateField): The date of birth of the person.
    role (ForeignKey): Foreign key to the Role model, representing the person's role.
    """

    phone = PhoneNumberField(blank=True, region="GB")
    date_of_birth = models.DateField(
        null=True, blank=True, help_text="Please use the following format : YYYY-MM-DD"
    )
    role = models.ForeignKey(Role, on_delete=models.RESTRICT, null=True, blank=True)

    objects = PersonManager()

    def __str__(self):
        return self.get_full_name()

    @property
    def age(self) -> Optional[int]:
        """
        Calculate the age of the person from the date of birth.

        Returns:
        Optional[int]: The age of the person, or None if `date_of_birth` is not set.
        """
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            if today.month < self.date_of_birth.month or (
                today.month == self.date_of_birth.month
                and today.day < self.date_of_birth.day
            ):
                age -= 1
            return age
        return None
