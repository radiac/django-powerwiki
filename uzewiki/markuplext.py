"""
Custom markuple parser with wiki support
"""
import re

import markuple

from uzewiki import models
from uzewiki.utils import (
    reverse_to_page, reverse_to_asset, wikislugify, title_from_slug
)


inline_registry = markuple.inlines.default_registry.copy()

class Page(markuple.inlines.RegexInline):
    name = 'page'
    registry = inline_registry
    
    match = re.compile(
        r'\[\[(?P<slug>(?!(http|ftp)s?://).+?)(?P<frag>#.*?)?(\|(?P<label>.+?))?\]\]',
        re.IGNORECASE
    )
    html = '<a href="%(url)s" class="%(class)s">%(label)s</a>'
    
    def html_kwargs(self, context):
        kwargs = super(Page, self).html_kwargs()
        
        if not kwargs['label']:
            kwargs['label'] = kwargs['slug'].split('/')[-1]
        
        wiki = context['wiki']
        link_class = 'wiki'
        page_slug = wikislugify(kwargs['slug'])
        label = kwargs['label']
        try:
            page = models.Page.objects.get(
                wiki=wiki,
                slug=page_slug,
            )
            url = page.get_absolute_url()
            label = label or page.title
        except models.Page.DoesNotExist:
            link_class += ' doesnotexist'
            url = reverse_to_page('uzewiki-show', wiki.slug, page_slug)
            label = label or title_from_slug(self.args[0])
            
        return {
            'url':      url + (kwargs['frag'] or ''),
            'label':    label,
            'class':    link_class,
        }


class Asset(markuple.inlines.RegexInline):
    name = 'asset'
    registry = inline_registry
    match = re.compile(
        r'\[\[asset:(?P<asset_name>[-\w]+)\]\]',
        re.IGNORECASE
    )
    html = '<a href="%(url)s" class="%(class)s">%(_)s</a>'
    
    def as_html(self, context):
        html_kwargs = self.html_kwargs(context)
        wiki = context['wiki']
        link_class = 'wiki'
        
        # Get asset
        asset_name = wikislugify(html_kwargs['asset_name'])
        try:
            asset = wiki.assets.get(name=asset_name)
        except wiki.assets.model.DoesNotExist:
            link_class += ' doesnotexist'
            content = asset_name
            url = reverse_to_asset('uzewiki-asset-edit', wiki.slug, asset_name)
        else:
            content = '<img src="%(url)s">' % {
                'url':  asset.image.url
            }
            url = reverse_to_asset('uzewiki-asset', wiki.slug, asset_name)
        
        return self.html % {
            'class': link_class,
            'url':  url,
            '_':    content,
        }
        
parser = markuple.parser.Parser(
    inline_parser=markuple.inlines.InlineParser(inline_registry)
)
