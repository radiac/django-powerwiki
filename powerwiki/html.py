"""
HTML tools
"""
import re
from collections import defaultdict
from functools import lru_cache
from typing import Optional, Tuple
from urllib.parse import urljoin, urlparse

from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.urls import reverse

from bs4 import BeautifulSoup

from . import app_settings
from .constants import (
    ASSET_NAME_PATTERN,
    PAGE_PATH_PATTERN,
    SCHEME_ASSET,
    SCHEME_WIKI,
    WIKI_SLUG_PATTERN,
)
from .models import Asset, Page, Wiki


re_valid_wiki_slug = re.compile(fr"^{WIKI_SLUG_PATTERN}$")
re_valid_page_path = re.compile(fr"^{PAGE_PATH_PATTERN}$")
re_valid_asset_name = re.compile(fr"^{ASSET_NAME_PATTERN}$")


@lru_cache
def get_wiki_root():
    return reverse("powerwiki:index")


def parse_url(url: str, wiki: Wiki, page: Page) -> Optional[Tuple[str, str, str]]:
    """
    Parse a wiki URL

    Returns:
        (scheme, wiki_slug, page_path) if it's a wiki url
        None if it's not a wiki url
    """
    # Get the scheme
    if ":" not in url:
        return None

    scheme, wiki_path = url.split(":", 1)
    if scheme == "":
        scheme = SCHEME_WIKI
    elif scheme not in [SCHEME_WIKI, SCHEME_ASSET]:
        return None

    # Resolve wiki
    wiki_slug = wiki.slug
    if ":" in wiki_path:
        # Wiki is specified
        if app_settings.SINGLE_MODE:
            raise ValidationError(f"Wiki link {url} specifies a wiki in single mode")

        wiki_slug, page_path = wiki_path.split(":", 1)
        page_path = page_path.lstrip("/")

        if ":" in page_path:
            raise ValidationError(f"Wiki link {url} has too many sections")

    else:
        wiki_slug = wiki.slug
        page_path = wiki_path

    # Check values are valid
    if not re_valid_wiki_slug.match(wiki_slug):
        if scheme == SCHEME_WIKI:
            raise ValidationError(f"Wiki link {url} has an invalid wiki slug")
        else:
            raise ValidationError(f"Asset link {url} has an invalid wiki slug")
    if scheme == SCHEME_WIKI and not re_valid_page_path.match(page_path):
        raise ValidationError(f"Wiki link {url} has an invalid page path")
    if scheme == SCHEME_ASSET and not re_valid_asset_name.match(page_path):
        raise ValidationError(f"Asset link {url} has an invalid asset name")

    # Ensure path is slugified
    page_path = "/".join([slugify(slug) for slug in page_path.split("/") if slug])

    return scheme, wiki_slug, page_path


def find_wiki_url(url: str, wiki: Wiki, page: Page) -> Optional[Tuple[str, str, str]]:
    """
    Normalises urls into a wiki link, or return None if not a wiki link

    Returns:
        (scheme: str, wiki_slug: str, page_path: str)  A wiki link
    """
    # Absolute urls stay the same
    # TODO: Is there a faster way to do this? This should also detect the current site.
    is_absolute = bool(urlparse(url).netloc)
    if is_absolute:
        return

    # See if we have a wiki or asset url
    try:
        parsed = parse_url(url, wiki, page)
    except ValidationError:
        # Silence errors
        return

    if parsed:
        return parsed

    # Convert relative wiki paths
    page_url = page.get_absolute_url()
    if not url.startswith("./"):
        # Strip trailing / so foo:bar is a sibling of the current page
        # If url starts ./ we want it to be a child
        page_url = page_url.rstrip("/")

    normalised = urljoin(page_url, url)
    wiki_root = get_wiki_root()
    if normalised.startswith(wiki_root):
        # Relative to the root
        relative = normalised[len(wiki_root) :]

        # Slugify the slugs
        slugs = relative.split("/")
        slugs = [slugify(slug) for slug in slugs]
        relative = "/".join(slugs)

        if app_settings.SINGLE_MODE:
            return SCHEME_WIKI, wiki.slug, relative

        elif "/" in relative:
            wiki_slug, page_path = relative.split("/", 1)
            return SCHEME_WIKI, wiki_slug, page_path
        else:
            return SCHEME_WIKI, wiki.slug, relative

    return


def clean(html: str, wiki: Wiki, page: Page):
    """
    Clean new HTML from the user

    * Convert relative paths to wiki urls
    """
    soup = BeautifulSoup(html, features=app_settings.HTML_PARSER)

    for tag_name, attr in app_settings.LINK_TAGS:
        for tag in soup.findAll(tag_name):
            parse_url(tag[attr], wiki, page)


def process(html: str, wiki: Wiki, page: Page):
    """
    Convert wiki links into relative paths
    """
    soup = BeautifulSoup(html, features=app_settings.HTML_PARSER)

    # Build lookup table for asset tags
    #   found[wiki][path] = [tag, tag, tag ...]
    asset_tags = defaultdict(lambda: defaultdict(list))

    for tag_name, attr in app_settings.LINK_TAGS:
        for tag in soup.findAll(tag_name):
            wiki_url = find_wiki_url(tag[attr], wiki, page)

            if wiki_url is None:
                continue

            scheme, wiki_slug, page_slug = wiki_url
            if scheme == SCHEME_WIKI:
                # We don't need to know anything concrete about a link yet, fake it
                obj = Page(wiki=Wiki(slug=wiki_slug), path=page_slug)
                tag[attr] = obj.get_absolute_url()

            elif scheme == SCHEME_ASSET:
                # We need to look up the assets to get the media urls
                # Defer so we can do the lookup in one go
                asset_tags[wiki_slug][page_slug].append((tag, attr))

            else:
                continue

            tag["class"] = f"{tag.get('class', '')} powerwiki__{scheme}".strip()

    # Look up and replace assets
    for wiki_slug, paths in asset_tags.items():
        fake_wiki = Wiki(slug=wiki_slug)

        # Lookup pages for this wiki
        assets = Asset.objects.filter(wiki__slug=wiki_slug, name__in=paths.keys())
        name_to_asset = {asset.name: asset for asset in assets}

        # Loop over paths
        for path, tags in paths.items():
            if path in name_to_asset:
                asset = name_to_asset[path]
            else:
                asset = Asset(wiki=fake_wiki, name=path)

            media_url = asset.get_media_url()
            edit_url = asset.get_edit_url()
            for tag, attr in tags:
                tag[attr] = media_url
                tag["data-edit"] = edit_url

    return str(soup)
