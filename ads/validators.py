from django.core.exceptions import ValidationError


def IsPublishedMustBeFalse(value: bool):
    message = f"You cannot create advertisement with 'is_published' = True"

    if value:
        raise ValidationError(message)
