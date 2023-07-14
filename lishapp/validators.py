from django.core.exceptions import ValidationError
class CustomUniqueValidationError(ValidationError):
    def __init__(self, message='This field must be unique.'):
        super().__init__(message)
