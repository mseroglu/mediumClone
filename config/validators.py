from django import forms


def max_length_10_validator(value):
    if len(value) > 10:
        raise forms.ValidationError(message="Max 10 characters!")