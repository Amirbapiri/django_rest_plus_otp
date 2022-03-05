from re import match

from django.core.exceptions import ValidationError


def phone_validator(value):
    pattern_str = "^09\d{9}$"
    if not bool(match(pattern=pattern_str, string=value)):
        raise ValidationError(message="Phone number is not valid.")
