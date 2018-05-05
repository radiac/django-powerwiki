
import re

from django import template
from django.conf import settings as django_settings
from django.template.defaultfilters import stringfilter
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text

from uzewiki.models import Page, Asset

register = template.Library()

# Characters for using as heading underlines
HEAD_CHR = ['=', '-', '`', "'", ':']

OP_LINK = 1
OP_ASSET = 2

def gen_wikilink(matchobj):
    slug = matchobj.group(1)

    # Split off op
    op = OP_LINK
    if slug.lower().startswith('asset:'):
        op = OP_ASSET
        slug = slug[len('asset:'):]

    # Split off the optional label
    label = None
    if '|' in slug:
        slug, label = slug.split('|', 1)

    # Build link_class and url depending on OP
    # (Or return early)
    link_class = 'wiki'
    if op == OP_ASSET:
        # Look up the asset
        try:
            asset = Asset.objects.get(name=slug)
        except Asset.DoesNotExist, e:
            # ++ Link to asset upload page
            return '(Missing asset: %s)' % slug

        # Find the URL
        url = django_settings.MEDIA_URL + asset.file.name

        # Try to embed
        lower_name = asset.file.name.lower()
        is_image = any(lower_name.endswith(ext) for ext in ('.jpg','.gif','.png'))
        if not label and is_image:
            return '<img src="%s" class="wiki_image">' % url

        # Link to the file instead

    else:
        slugged_slug = slugify(slug)
        try:
            page = Page.objects.get(slug=slugged_slug)
        except Page.DoesNotExist, e:
            link_class = 'wiki doesnotexist'

        # Reverse the URL
        url = reverse('wiki.views.show', kwargs={
            'page_slug':    slugged_slug
        })

    # Build and return the link
    link = '<a href="%s" class="%s">%s</a>' % (url, link_class, label or slug)
    return link

def wiki_preparse(line):
    # Skip empty lines or lines which are just ==== and spaces
    if not line or re.match(r'^[= ]+$', line):
        return [line]

    # Single line headings
    m = re.match(r'^(=={1,5}) *(.+?) *\1$', line)
    if m:
        header = m.group(2)
        head_chr = HEAD_CHR[ len(m.group(1)) - 2 ]
        return [header, head_chr * len(header)]

    # Wasn't anything interesting
    return [line]

def wikirest(value):
    """
    Add wiki support to restructuredtext filter
    Adds mediawiki-style support for:
    * Single-line headings:
        == H2 ==
        === H3 ===
        ==== H4 ====
        ===== H5 =====
        ====== H6 ======
    * Wiki links
        [[page_name]]
        [[page_name|Link text]]
    * Wiki assets
        [[Asset:asset_name]]
        [[Asset:asset_name|Link text]]
        Note: This is 'asset' instead of 'image', as it can be used for files
        If the asset is an image it will be embedded, unless Link Text is provided
    """

    # Before the parser
    lines = []
    for line in value.splitlines():
        lines += wiki_preparse(line)
    value = "\n".join(lines)

    # Convert to HTML
    try:
        from docutils.core import publish_parts
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError("Error in 'restructuredtext' filter: The Python docutils library isn't installed.")
        rested = force_text(value)
    else:
        docutils_settings = getattr(settings, "RESTRUCTUREDTEXT_FILTER_SETTINGS", {})
        parts = publish_parts(source=force_bytes(value), writer_name="html4css1", settings_overrides=docutils_settings)
        rested = force_text(parts["fragment"])

    # Look for wiki links and assets
    rested = re.sub(r'\[\[ *(.+?) *\]\]', gen_wikilink, rested)

    return mark_safe(rested)
wikirest.is_safe = True
register.filter(wikirest)

