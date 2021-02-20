"""
Powerwiki models
"""
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.html import mark_safe

from . import app_settings, constants, utils
from .markup.loader import engine_field_choices, get_engine, load_engines


if "django.contrib.postgres" in settings.INSTALLED_APPS:
    from django.contrib.postgres.search import SearchVector

#  Preload engines
load_engines()


class Wiki(models.Model):
    """
    Wiki
    """

    title = models.CharField(max_length=255, help_text="Title of the wiki",)
    slug = models.SlugField(unique=True, help_text="Slug for the wiki",)
    description = models.TextField(blank=True, help_text="Description of wiki")
    perm_read = models.IntegerField(
        default=constants.PERM_SU,
        choices=constants.PERM_CHOICES,
        verbose_name="Read permission",
        help_text="Default read permissions",
    )
    perm_edit = models.IntegerField(
        default=constants.PERM_SU,
        choices=constants.PERM_CHOICES,
        verbose_name="Edit permission",
        help_text="Default edit permissions",
    )
    markup_engine = models.CharField(
        max_length=255,
        default=app_settings.MARKUP_ENGINE_DEFAULT,
        choices=engine_field_choices(),
    )
    users = models.ManyToManyField(
        get_user_model(), through="WikiPermissions", related_name="wikis"
    )

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return "%s" % self.title

    def get_absolute_url(self):
        return utils.reverse_to_page(
            "powerwiki:page", self.slug, app_settings.FRONT_PATH
        )

    def can_read(self, user):
        """
        Check that the user can read
        Returns bool
        """
        # Check generic wiki permission
        if utils.has_permission(user, self.perm_read):
            return True

        # Check overrides
        if not user.is_authenticated:
            return False
        try:
            user_perm = self.user_permissions.get(user=user)
        except self.user_permissions.model.DoesNotExist:
            return False
        return user_perm.can_read

    def can_edit(self, user):
        """
        Check that the user can read
        Returns bool
        """
        # Check generic wiki permission
        if utils.has_permission(user, self.perm_edit):
            return True

        # Check overrides
        if not user.is_authenticated:
            return False
        try:
            user_perm = self.user_permissions.get(user=user)
        except self.user_permissions.model.DoesNotExist:
            return False
        return user_perm.can_edit

    def gen_breadcrumbs(self, page_path=None):
        """
        Given a wiki and page path, build breadcrumbs
        """
        breadcrumbs = [
            {"title": self.title, "class": "", "url": self.get_absolute_url()}
        ]
        if page_path and page_path != app_settings.FRONT_PATH:
            path_root = ""
            for path_fragment in page_path.split("/"):
                path = path_root + path_fragment
                try:
                    crumb = Page.objects.get(wiki=self, path=path)
                    breadcrumbs.append(
                        {
                            "title": crumb.full_title(),
                            "class": "",
                            "url": crumb.get_absolute_url(),
                        }
                    )
                except Page.DoesNotExist:
                    breadcrumbs.append(
                        {
                            "title": utils.title_from_path(path_fragment),
                            "class": " doesnotexist",
                            "url": utils.reverse_to_page(
                                "powerwiki:page-edit", self.slug, path,
                            ),
                        }
                    )
                path_root += path_fragment + "/"
        return breadcrumbs

    def search(self, query):
        if "django.contrib.postgres" in settings.INSTALLED_APPS:
            return self.pages.annotate(search=SearchVector("title", "content")).filter(
                search=query
            )
        else:
            return self.pages.filter(
                models.Q(title__icontains=query) | models.Q(content__icontains=query)
            )


class WikiPermissions(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name="wiki_permissions", on_delete=models.CASCADE
    )
    wiki = models.ForeignKey(
        Wiki, related_name="user_permissions", on_delete=models.CASCADE
    )
    can_read = models.BooleanField(default=True, help_text="User can read the wiki")
    can_edit = models.BooleanField(default=True, help_text="User can edit the wiki")


class Page(models.Model):
    """
    Wiki page
    """

    wiki = models.ForeignKey(Wiki, related_name="pages", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, help_text="Title of the page",)
    path = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                r"^[a-z0-9][a-z0-9_\-]*(/[a-z0-9][a-z0-9_\-]*)*$",
                (
                    "A path can only be lowercase, numbers, hyphens and underscores, "
                    "using forward slashes to separate sub-pages, "
                    "with each page starting with a lowercase or number."
                ),
                "invalid",
            )
        ],
        help_text="Path for the page, under the wiki root",
    )
    is_locked = models.BooleanField(
        default=False, help_text="If locked, can only be edited by wiki admin",
    )
    content = models.TextField(blank=True, help_text="Page content")
    markup_engine = models.CharField(
        max_length=255,
        default=app_settings.MARKUP_ENGINE_DEFAULT,
        choices=engine_field_choices(),
    )

    class Meta:
        unique_together = ("wiki", "path")
        ordering = ("title",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return utils.reverse_to_page("powerwiki:page", self.wiki.slug, self.path)

    def get_edit_url(self):
        return utils.reverse_to_page("powerwiki:page-edit", self.wiki.slug, self.path)

    def full_title(self):
        return "%s" % (self.title)

    def render_content(self, user: AbstractUser):
        engine_class = get_engine(self.markup_engine)
        engine = engine_class(wiki=self.wiki, page=self)
        html = engine.render(self.content, user=user)
        return mark_safe(html)


def asset_upload_to(asset, filename):
    return os.path.join("powerwiki", asset.wiki.slug, filename)


class Asset(models.Model):
    """
    Wiki asset
    """

    wiki = models.ForeignKey(Wiki, related_name="assets", on_delete=models.CASCADE)
    name = models.SlugField(help_text="Internal name for the asset")
    file = models.FileField(upload_to=asset_upload_to)

    def get_absolute_url(self):
        """
        Asset download url
        """
        return utils.reverse_to_asset("powerwiki:asset", self.wiki.slug, self.name)

    def get_edit_url(self):
        return utils.reverse_to_asset("powerwiki:asset-edit", self.wiki.slug, self.name)

    def get_media_url(self):
        return self.file.url
