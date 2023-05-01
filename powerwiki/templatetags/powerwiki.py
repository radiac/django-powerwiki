from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape

from ..models import HEADLINE_START, HEADLINE_STOP

register = template.Library()


@register.simple_tag(takes_context=True)
def render_wiki(context, page):
    rendered = page.render_content(user=context["request"].user)
    return mark_safe(rendered)


@register.filter
def powerwiki_summary(summary):
    # TODO: Replace this with a properly sanitised cached render on the model
    escaped = escape(summary)
    return mark_safe(
        escaped.replace(HEADLINE_START, "<b>").replace(HEADLINE_STOP, "</b>")
    )
