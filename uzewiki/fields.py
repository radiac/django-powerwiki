"""
Model and form fields
"""
import re

from django import forms
from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _


slug_msg = (
    "Enter a valid wiki 'slug' consisting of letters, numbers, underscores or"
    " hyphens, using forward slashes to separate sub-pages"
)
class WikiSlugWidget(forms.SlugField):
    default_error_messages = {
        'invalid': _(slug_msg),
    }
    default_validators = [validators.RegexValidator(
        re.compile(r'^[-\w]+(/[-\w]+)*$'),
        slug_msg, 'invalid',
    )]

class WikiSlugField(models.SlugField):
    def formfield(self, **kwargs):
        defaults = {'form_class': WikiSlugWidget}
        defaults.update(kwargs)
        return super(WikiSlugField, self).formfield(**defaults)

#
# South migrations
#
try:
    from south import modelsinspector
    modelsinspector.add_introspection_rules(
        [], ["^uzewiki\.fields\.WikiSlugField"],
    )

except ImportError, e:
    # South not installed
    pass
