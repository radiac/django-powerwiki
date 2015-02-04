"""
Uzewiki models
"""
import os

from django.db import models

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from uzewiki import constants, settings, utils, fields


class Wiki(models.Model):
    """
    Wiki
    """
    title       = models.CharField(
        max_length=255, help_text="Title of the wiki",
    )
    slug        = models.SlugField(
        unique=True, help_text="Slug for the wiki",
    )
    description = models.TextField(blank=True, help_text="Description of wiki")
    perm_read   = models.IntegerField(
        default=constants.PERM_SU, choices=constants.PERM_CHOICES,
        verbose_name='Read permission',
        help_text="Default read permissions",
    )
    perm_edit   = models.IntegerField(
        default=constants.PERM_SU, choices=constants.PERM_CHOICES,
        verbose_name='Edit permission',
        help_text="Default edit permissions",
    )
    users       = models.ManyToManyField(
        User, through='WikiPermissions', related_name="wikis"
    )
    
    def __unicode__(self):
        return u'%s' % self.title
    
    def get_absolute_url(self):
        return utils.reverse_to_page(
            'uzewiki-show', self.slug, settings.FRONT_SLUG,
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
        if not user.is_authenticated():
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
        if not user.is_authenticated():
            return False
        try:
            user_perm = self.user_permissions.get(user=user)
        except self.user_permissions.model.DoesNotExist:
            return False
        return user_perm.can_edit
        
    def gen_breadcrumbs(self, page_slug=None):
        """
        Given a wiki and page slug, build breadcrumbs
        """
        breadcrumbs = [{
            'title':    self.title,
            'class':    '',
            'url':      self.get_absolute_url()
        }]
        if page_slug and page_slug != settings.FRONT_SLUG:
            slug_root = ''
            for slug_fragment in page_slug.split('/'):
                slug = slug_root + slug_fragment
                try:
                    crumb = Page.objects.get(wiki=self, slug=slug)
                    breadcrumbs.append({
                        'title':    crumb.full_title(),
                        'class':    '',
                        'url':      crumb.get_absolute_url(),
                    })
                except Page.DoesNotExist:
                    breadcrumbs.append({
                        'title':    utils.title_from_slug(slug_fragment),
                        'class':    ' doesnotexist',
                        'url':      utils.reverse_to_page(
                            'uzewiki-edit', self.slug, slug,
                        ),
                    })
                slug_root += slug_fragment + '/'
        return breadcrumbs
    
    class Meta:
        ordering = ('title',)


class WikiPermissions(models.Model):
    user = models.ForeignKey(User, related_name="wiki_permissions")
    wiki = models.ForeignKey(Wiki, related_name="user_permissions")
    can_read    = models.BooleanField(
        default=True, help_text="User can read the wiki",
    )
    can_edit = models.BooleanField(
        default=True, help_text="User can edit the wiki",
    )
    
    
class Page(models.Model):
    """
    Wiki page
    """
    wiki        = models.ForeignKey(Wiki, related_name='pages')
    slug        = fields.WikiSlugField(
        max_length=100, help_text="Slug for the page",
    )
    title       = models.CharField(
        max_length=255, help_text="Title of the page",
    )
    is_locked   = models.BooleanField(
        default=False, help_text="If locked, can only be edited by wiki admin",
    )
    content     = models.TextField(blank=True, help_text="Page content",)
    
    def full_title(self):
        return '%s' % (self.title)
    
    def get_absolute_url(self):
        return utils.reverse_to_page('uzewiki-show', self.wiki.slug, self.slug)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        unique_together = ('wiki', 'slug')
        ordering = ('title',)
    
    
def asset_upload_to(asset, filename):
    return os.path.join('wiki', asset.wiki.slug, filename)

class Asset(models.Model):
    """
    Wiki asset
    """
    wiki        = models.ForeignKey(Wiki, related_name='assets')
    name        = models.SlugField(help_text="Internal name for the asset")
    image       = models.ImageField(upload_to=asset_upload_to)

    def get_absolute_url(self):
        return utils.reverse_to_asset(
            'uzewiki-asset', self.wiki.slug, self.name,
        )