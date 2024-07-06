from phonenumber_field.phonenumber import to_python
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    """
    Validates that the input is a valid phone number.

    Args:
        value (str): The phone number to validate.

    Raises:
        ValidationError: If the phone number is not valid.
    """
    phone_number = to_python(value)
    if phone_number and not phone_number.is_valid():
        raise ValidationError(f"Invalid phone number: {value}")
