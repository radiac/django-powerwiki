"""
Uzewiki utils
"""
import unicodedata
import re

from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from uzewiki import constants
from uzewiki import settings


def has_permission(user, permission):
    """
    See if the user has the specified level of permission
    """
    # If public, all can see
    if permission == constants.PERM_PUBLIC:
        return True

    # If not public, must be PERM_USER or higher
    if not user.is_authenticated():
        return False

    # Superuser can see all
    # Staff can see STAFF and lower
    # Anyone here must be a user, so can see USERS
    if (
        user.is_superuser
        or (user.is_staff and permission <= constants.PERM_STAFF)
        or permission == constants.PERM_USERS
        ):
        return True

    return False


def reverse_to_page(view, wiki_slug, page_slug=None):
    """
    Return the URL for the given page
    """
    kwargs = {}
    if not settings.SINGLE:
        kwargs['wiki_slug'] = wiki_slug
    if page_slug and not (view == 'uzewiki:show' and page_slug == settings.FRONT_SLUG):
        kwargs['page_slug'] = page_slug
    return reverse(view, kwargs=kwargs)


def wikislugify(value):
    """
    Like django.utils.text.slugify, but supports sub-pages
    """
    # ++ This bit was causing problems. Fine without it?
    #value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('(^/|[^\w\s/-]|/$)', '', value).strip().lower()
    return mark_safe(re.sub('[-\s]+', '-', value))


def title_from_slug(value):
    """
    Make a best guess at converting a wikislug into a title
    """
    # Find true slug at end of wikislug
    slug_index = value.rfind('/')
    if slug_index > -1:
        value = value[slug_index+1:]

    return re.sub('[-\s_]+', ' ', value).title()


def reverse_to_asset(view, wiki_slug, asset_name=None):
    """
    Return the URL for the given asset view
    """
    kwargs = {}
    if not settings.SINGLE:
        kwargs['wiki_slug'] = wiki_slug
    if asset_name:
        kwargs['asset_name'] = asset_name
    return reverse(view, kwargs=kwargs)
