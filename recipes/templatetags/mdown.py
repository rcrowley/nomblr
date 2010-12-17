from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django import template

import markdown

register = template.Library()

@register.filter
@stringfilter
def mdown(value):
    return mark_safe(markdown.markdown(value))
