"""
Decorators
"""

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from . import constants, models, utils


#
# Wiki util
#


def get_wiki(fn):
    """
    Look up the wiki in kwargs['wiki_slug']
    Return 404 if not found, otherwise pass on to decorated fn as second arg
    """

    def wrapper(request, *args, **kwargs):
        wiki = get_object_or_404(models.Wiki, slug=kwargs.get("wiki_slug", None))
        return fn(request, wiki, *args, **kwargs)

    return wrapper


#
# Permission handling
#


def permission_required(permission, login_url=None):
    """
    Ensures that the user has specified permission to access the current page
    """

    def check_perms(user):
        # Check if user not logged in
        if not user.is_authenticated:
            if permission == constants.PERM_PUBLIC:
                # They're not, but it's public
                return True

            # User not logged in, needs a permission, show the login form
            return False

        # User is logged in, just lacks permission
        if not utils.has_permission(user, permission):
            raise PermissionDenied

        return True

    return user_passes_test(check_perms, login_url=login_url)


def read_required(fn):
    """
    Must be called on a function already decorated with @get_wiki
    """

    def wrapper(request, wiki, *args, **kwargs):
        if not wiki.can_read(request.user):
            if request.user.is_authenticated:
                raise PermissionDenied
            # Make auth decorator fail to force user to login form
            return user_passes_test(lambda u: False)(lambda r: None)(request)
        return fn(request, wiki, *args, **kwargs)

    return wrapper


def edit_required(fn):
    """
    Must be called on a function already decorated with @get_wiki
    """

    def wrapper(request, wiki, *args, **kwargs):
        if not wiki.can_edit(request.user):
            if request.user.is_authenticated:
                raise PermissionDenied
            # Make auth decorator fail to force user to login form
            return user_passes_test(lambda u: False)(lambda r: None)(request)
        return fn(request, wiki, *args, **kwargs)

    return wrapper
