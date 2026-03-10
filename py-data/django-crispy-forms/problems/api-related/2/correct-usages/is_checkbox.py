from itertools import izip

from django import forms
from django import template
from django.conf import settings


@register.filter
def is_checkbox(field):
    return field.field.widget.__class__.__name__.lower() == "checkboxinput"
