import re

from django.core.exceptions import ValidationError


def validate_positive(value):
    if value < 0:
        raise ValidationError(f"{value} should be positive")


def validate_phone(value):
    matched = re.match(r"[+]?[0-9|-]*", value)
    if value[matched.start():matched.end()] != value:
        raise ValidationError("Invalid phone number")


def validate_discount(value):
    if value <= 0:
        raise ValidationError("Discount cant be lower than zero")
    if value > 100:
        raise ValidationError("Discount cant be greater than 100")
