from django.contrib.auth.models import AbstractUser

from docutils import nodes, utils
from docutils.core import publish_parts
from docutils.parsers.rst.roles import _roles, set_implicit_options

from ..utils import wikipathify
from .base import MarkupEngine


def role_link_wiki(name, rawtext, text, lineno, inliner, options={}, content=[]):
    node = nodes.reference(
        rawtext, utils.unescape(text), refuri=wikipathify(text), **options
    )
    return [node], []


def role_link_asset(name, rawtext, text, lineno, inliner, options={}, content=[]):
    node = nodes.reference(
        rawtext, utils.unescape(text), refuri=f"asset:{wikipathify(text)}", **options
    )
    return [node], []


# According to docutils we're supposed to call roles.register_local_role, but that would
# potentially clash with any other use of docutils in the system. We'll therefore
# reimplement it in this module - calling `set_implicit_options` directly, then setting
# and unsetting _roles within the markup engine later using TmpRole
set_implicit_options(role_link_wiki)
set_implicit_options(role_link_asset)


class TmpRole:
    def __init__(self, name, fn):
        self.name = name
        self.fn = fn

    def __enter__(self):
        self.archive = _roles.pop(self.name, None)
        _roles[self.name] = self.fn

    def __exit__(self, type, value, traceback):
        del _roles[self.name]
        if self.archive is not None:
            _roles[self.name] = self.archive


class RestructuredText(MarkupEngine):
    label = "reStructuredText"
    docutils_settings = {
        "doctitle_xform": False,
    }

    def to_html(self, raw: str, user: AbstractUser) -> str:
        # Prepare docutils for custom roles
        with TmpRole("wiki", role_link_wiki), TmpRole("asset", role_link_asset):
            # Convert to HTML
            parts = publish_parts(
                source=raw,
                writer_name="html",
                settings_overrides=self.docutils_settings,
            )
        html = parts["fragment"]
        return html
