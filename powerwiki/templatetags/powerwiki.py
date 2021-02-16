from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag(takes_context=True)
def render_wiki(context, page):
    rendered = page.render_content(user=context["request"].user)
    return mark_safe(rendered)
