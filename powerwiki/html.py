"""
HTML tools
"""
import re
from collections import defaultdict
from functools import lru_cache
from typing import Optional, Tuple
from urllib.parse import urljoin, urlparse

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.urls import reverse

from bs4 import BeautifulSoup

from . import app_settings
from .constants import (
    ASSET_NAME_PATTERN,
    PAGE_PATH_PATTERN,
    SCHEME_ASSET,
    SCHEME_IMAGE,
    SCHEME_WIKI,
    WIKI_SLUG_PATTERN,
    WIKILINK_CLOSE,
    WIKILINK_LABEL_SEPARATOR,
    WIKILINK_OPEN,
    WIKILINK_SCHEME_SEPARATOR,
)
from .models import Asset, Page, Wiki


re_valid_wiki_slug = re.compile(fr"^{WIKI_SLUG_PATTERN}$")
re_valid_page_path = re.compile(fr"^{PAGE_PATH_PATTERN}$")
re_valid_asset_name = re.compile(fr"^{ASSET_NAME_PATTERN}$")


@lru_cache()
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


def process(html: str, wiki: Wiki, page: Page, user: AbstractUser):
    """
    Convert wiki links into relative paths
    """
    soup = BeautifulSoup(html, features=app_settings.HTML_PARSER)

    # Convert wiki format links [[page|label]]
    for text in soup.findAll(text=True):
        ptr = 0
        replacement = BeautifulSoup(features=app_settings.HTML_PARSER)
        while ptr > -1:
            # Find next wikilink
            match_open = text.find(WIKILINK_OPEN, ptr)
            if match_open == -1:
                break
            match_close = text.find(WIKILINK_CLOSE, match_open)
            if match_close == -1:
                break

            # Capture text before tag open, and advance ptr to end of area of interest
            if ptr != match_open:
                replacement.append(text[ptr:match_open])
            ptr = match_close + len(WIKILINK_CLOSE)

            # Detect scheme
            path = text[match_open + len(WIKILINK_OPEN) : match_close]
            if WIKILINK_SCHEME_SEPARATOR in path:
                scheme, path = path.split(WIKILINK_SCHEME_SEPARATOR, 1)
            else:
                scheme = SCHEME_WIKI

            # Detect label
            if WIKILINK_LABEL_SEPARATOR in path:
                path, label = path.split(WIKILINK_LABEL_SEPARATOR, 1)
            else:
                label = ""

            # Image scheme can't have a label
            if scheme == SCHEME_IMAGE and label:
                # Invalid tag, skip
                continue

            # Build replacement tag
            if scheme == SCHEME_IMAGE:
                replacement.append(soup.new_tag("img", src=f"{SCHEME_ASSET}:{path}"))
            else:
                link = soup.new_tag("a", href=f"{scheme}:{path}")
                link.string = label
                replacement.append(link)

            # Restart loop to look for next tag

        # Capture anything at the end of the string
        if ptr < len(text):
            replacement.append(text[ptr:])

        # TODO: Might be worth performance testing the above against 3 regexps:
        """
        replaced = re_wiki_link.sub(
            lambda match: '<a href="{path}">{label}</a>'.format(
                path=match.group("path"),
                label=match.group("label") or match.group("path"),
            ),
            text,
        )
        """
        text.replaceWith(replacement)

    # Build lookup tables for tags
    #   found[wiki][path] = [tag, tag, tag ...]
    page_tags = defaultdict(lambda: defaultdict(list))
    asset_tags = defaultdict(lambda: defaultdict(list))

    for tag_name, attr in app_settings.LINK_TAGS:
        for tag in soup.findAll(tag_name):
            wiki_url = find_wiki_url(tag[attr], wiki, page)

            if wiki_url is None:
                continue

            # We need to look up the pages and assets
            # Defer so we can do the lookup in one go
            scheme, wiki_slug, page_slug = wiki_url
            if scheme == SCHEME_WIKI:
                # We don't need to know anything concrete about a link yet, fake it
                page_tags[wiki_slug][page_slug].append((tag, attr))

            elif scheme == SCHEME_ASSET:
                asset_tags[wiki_slug][page_slug].append((tag, attr))

            else:
                continue

            tag["class"] = f"{tag.get('class', '')} powerwiki__{scheme}".strip()

    # Look up wikis and check permissions
    wiki_slugs = list(page_tags.keys()) + list(asset_tags.keys())
    wikis = Wiki.objects.filter(slug__in=wiki_slugs)
    available_wikis = [wiki.slug for wiki in wikis if wiki.can_read(user)]

    # Look up and replace pages
    for wiki_slug, paths in page_tags.items():
        if wiki_slug in available_wikis:
            # Lookup pages for this wiki
            pages = Page.objects.filter(wiki__slug=wiki_slug, path__in=paths.keys())
        else:
            pages = []

        path_to_page = {page.path: page for page in pages}
        fake_wiki = Wiki(slug=wiki_slug)

        # Loop over paths
        for path, tags in paths.items():
            page = path_to_page.get(path)
            if not page:
                page = Page(wiki=fake_wiki, path=path)

            for tag, attr in tags:
                tag[attr] = page.get_absolute_url()
                tag["data-edit"] = page.get_edit_url()
                if not page.pk:
                    tag["data-missing"] = True

                if tag.string == "" and tag.name in app_settings.LINK_TAG_CONTAINERS:
                    if page.pk:
                        tag.string = page.title
                    else:
                        tag.string = path

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
                media_url = asset.get_media_url()
            else:
                asset = Asset(wiki=fake_wiki, name=path)
                media_url = ""

            edit_url = asset.get_edit_url()
            for tag, attr in tags:
                tag[attr] = media_url
                tag["data-edit"] = edit_url
                if not asset.pk:
                    tag["data-missing"] = True

    return str(soup)
