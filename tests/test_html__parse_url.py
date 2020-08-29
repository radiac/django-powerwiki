"""
Test parse_url in html.py
"""
from django.core.exceptions import ValidationError

import pytest

from powerwiki.constants import SCHEME_ASSET, SCHEME_WIKI
from powerwiki.html import parse_url


def test_parse_url__absolute_url__unchanged(wiki, page):
    url = "https://example.com"
    parsed = parse_url(url, wiki, page)
    assert parsed is None


def test_parse_url__mailto__unchanged(wiki, page):
    url = "mailto:bob@example.com"
    parsed = parse_url(url, wiki, page)
    assert parsed is None


def test_parse_url__wiki_scheme_as_single__unchanged(settings, wiki, page):
    settings.POWERWIKI_SINGLE_MODE = True
    url = "wiki:page"
    parsed = parse_url(url, wiki, page)
    assert parsed == (SCHEME_WIKI, wiki.slug, "page")


def test_parse_url__wiki_scheme_with_slug_as_single__validation_fails(
    settings, wiki, page
):
    settings.POWERWIKI_SINGLE_MODE = True
    url = "wiki:slug:page"
    with pytest.raises(ValidationError) as excinfo:
        parse_url(url, wiki, page)
    assert (
        excinfo.value.message
        == "Wiki link wiki:slug:page specifies a wiki in single mode"
    )


def test_parse_url__wiki_scheme_with_multiple_colons__validation_fails(wiki, page):
    url = "wiki:slug:page:extra"
    with pytest.raises(ValidationError) as excinfo:
        parse_url(url, wiki, page)
    assert (
        excinfo.value.message == "Wiki link wiki:slug:page:extra has too many sections"
    )


def test_parse_url__wiki_scheme_with_invalid_wiki_slug__validation_fails(wiki, page):
    url = "wiki:invalid#fail:page"
    with pytest.raises(ValidationError) as excinfo:
        parse_url(url, wiki, page)
    assert excinfo.value.message == f"Wiki link {url} has an invalid wiki slug"


def test_parse_url__asset_scheme_with_invalid_wiki_slug__validation_fails(wiki, page):
    url = "asset:invalid#fail:file"
    with pytest.raises(ValidationError) as excinfo:
        parse_url(url, wiki, page)
    assert excinfo.value.message == f"Asset link {url} has an invalid wiki slug"


def test_parse_url__wiki_scheme_with_invalid_path__validation_fails(wiki, page):
    url = "wiki:slug:invalid#fail"
    with pytest.raises(ValidationError) as excinfo:
        parse_url(url, wiki, page)
    assert excinfo.value.message == f"Wiki link {url} has an invalid page path"


def test_parse_url__asset_scheme_with_invalid_name__validation_fails(wiki, page):
    url = "asset:slug:invalid#fail"
    with pytest.raises(ValidationError) as excinfo:
        parse_url(url, wiki, page)
    assert excinfo.value.message == f"Asset link {url} has an invalid asset name"


def test_parse_url__wiki_scheme__unchanged(wiki, page):
    url = "wiki:page"
    parsed = parse_url(url, wiki, page)
    assert parsed == (SCHEME_WIKI, wiki.slug, "page")


def test_parse_url__wiki_scheme_with_current_slug__unchanged(wiki, page):
    url = "wiki:slug:page"
    parsed = parse_url(url, wiki, page)
    assert parsed == (SCHEME_WIKI, "slug", "page")


def test_parse_url__wiki_scheme_with_other_slug__unchanged(wiki, page):
    url = "wiki:other:page"
    parsed = parse_url(url, wiki, page)
    assert parsed == (SCHEME_WIKI, "other", "page")


def test_parse_url__implied_wiki_scheme__unchanged(wiki, page):
    url = ":page"
    parsed = parse_url(url, wiki, page)
    assert parsed == (SCHEME_WIKI, wiki.slug, "page")


def test_parse_url__implied_wiki_scheme_with_current_slug__unchanged(wiki, page):
    url = ":slug:page"
    parsed = parse_url(url, wiki, page)
    assert parsed == (SCHEME_WIKI, "slug", "page")


def test_parse_url__implied_wiki_scheme_with_other_slug__unchanged(wiki, page):
    url = ":other:page"
    parsed = parse_url(url, wiki, page)
    assert parsed == (SCHEME_WIKI, "other", "page")


def test_parse_url__asset_scheme__unchanged(wiki, page):
    url = "asset:file"
    parsed = parse_url(url, wiki, page)
    assert parsed == (SCHEME_ASSET, wiki.slug, "file")


def test_parse_url__asset_scheme_with_current_slug__unchanged(wiki, page):
    url = "asset:slug:file"
    parsed = parse_url(url, wiki, page)
    assert parsed == (SCHEME_ASSET, "slug", "file")


def test_parse_url__asset_scheme_with_other_slug__unchanged(wiki, page):
    url = "asset:other:file"
    parsed = parse_url(url, wiki, page)
    assert parsed == (SCHEME_ASSET, "other", "file")


def test_parse_url__absolute_outside_wiki__unchanged(wiki, page):
    url = "/other"
    parsed = parse_url(url, wiki, page)
    assert parsed is None
