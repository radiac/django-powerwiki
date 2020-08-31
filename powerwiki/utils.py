"""
Powerwiki utils
"""
import re

from django.urls import reverse
from django.utils.safestring import mark_safe

from . import app_settings, constants


def has_permission(user, permission):
    """
    See if the user has the specified level of permission
    """
    # If public, all can see
    if permission == constants.PERM_PUBLIC:
        return True

    # If not public, must be PERM_USER or higher
    if not user.is_authenticated:
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


def reverse_to_page(view, wiki_slug, page_path=None):
    """
    Return the URL for the given page
    """
    kwargs = {}
    if not app_settings.SINGLE_MODE:
        kwargs["wiki_slug"] = wiki_slug
    if page_path and not (
        view == "powerwiki:page" and page_path == app_settings.FRONT_PATH
    ):
        kwargs["page_path"] = page_path
    return reverse(view, kwargs=kwargs)


def wikipathify(value):
    """
    Like django.utils.text.slugify, but supports sub-pages
    """
    value = re.sub(r"(^/|[^\w\s/-]|/$)", "", value).strip().lower()
    return mark_safe(re.sub(r"[-\s]+", "-", value))


def title_from_path(value):
    """
    Make a best guess at converting a wiki path into a title
    """
    # Find slug at end of path
    slug_index = value.rfind("/")
    if slug_index > -1:
        value = value[slug_index + 1 :]

    return re.sub(r"[-\s_]+", " ", value).title()


def reverse_to_asset(view, wiki_slug, asset_name=None):
    """
    Return the URL for the given asset view
    """
    kwargs = {}
    if not app_settings.SINGLE_MODE:
        kwargs["wiki_slug"] = wiki_slug
    if asset_name:
        kwargs["asset_name"] = asset_name
    return reverse(view, kwargs=kwargs)
