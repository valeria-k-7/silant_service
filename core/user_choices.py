from django import forms
from django_filters import ModelChoiceFilter


def get_user_display_name(user):
    return user.get_full_name() or user.username


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return get_user_display_name(obj)


class UserChoiceFilter(ModelChoiceFilter):
    field_class = UserChoiceField
