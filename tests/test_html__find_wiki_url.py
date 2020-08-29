"""
Test conversion functions in html.py
"""
from model_bakery import baker

from powerwiki.constants import SCHEME_WIKI
from powerwiki.html import find_wiki_url
from powerwiki.models import Page


def test_find_wiki_url__absolute_url__unchanged(wiki, page):
    url = "https://example.com"
    parsed = find_wiki_url(url, wiki, page)
    assert parsed is None


def test_find_wiki_url__mailto__unchanged(wiki, page):
    url = "mailto:bob@example.com"
    parsed = find_wiki_url(url, wiki, page)
    assert parsed is None


def test_find_wiki_url__wiki_scheme_as_single__unchanged(settings, wiki, page):
    settings.POWERWIKI_SINGLE_MODE = True
    url = "wiki:page"
    parsed = find_wiki_url(url, wiki, page)
    assert parsed == (SCHEME_WIKI, wiki.slug, "page")


def test_find_wiki_url__wiki_scheme_with_slug_as_single__validation_fails(
    settings, wiki, page
):
    settings.POWERWIKI_SINGLE_MODE = True
    url = "wiki:slug:page"
    parsed = find_wiki_url(url, wiki, page)
    assert parsed is None


def test_find_wiki_url__relative_outside_wiki__unchanged(wiki, page):
    # current url: /wiki/slug/parent/page/
    # url as absolute: /other/
    url = "../../../other"
    parsed = find_wiki_url(url, wiki, page)
    assert parsed is None


def test_find_wiki_url__absolute_inside_wiki__converted_to_wiki_scheme(wiki, page):
    url = "/wiki/slug/other"
    parsed = find_wiki_url(url, wiki, page)
    assert parsed == (SCHEME_WIKI, "slug", "other")


def test_find_wiki_url__relative_at_wiki_root__converted_to_wiki_scheme(wiki):
    url = "other"
    page = baker.make(Page, wiki=wiki, path="page")
    parsed = find_wiki_url(url, wiki, page)
    assert parsed == (SCHEME_WIKI, "slug", "other")


def test_find_wiki_url__relative_inside_wiki__converted_to_wiki_scheme(wiki, page):
    url = "other"
    parsed = find_wiki_url(url, wiki, page)
    assert parsed == (SCHEME_WIKI, "slug", "parent/other")


def test_find_wiki_url__absolute_child__converted_to_wiki_scheme(wiki, page):
    url = "/wiki/slug/parent/other"
    parsed = find_wiki_url(url, wiki, page)
    assert parsed == (SCHEME_WIKI, "slug", "parent/other")


def test_find_wiki_url__relative_child__converted_to_wiki_scheme(wiki, page):
    url = "./other"
    parsed = find_wiki_url(url, wiki, page)
    assert parsed == (SCHEME_WIKI, "slug", "parent/page/other")


def test_find_wiki_url__relative_parent_sibling__converted_to_wiki_scheme(wiki, page):
    url = "../parent-sibling"
    parsed = find_wiki_url(url, wiki, page)
    assert parsed == (SCHEME_WIKI, "slug", "parent-sibling")


def test_find_wiki_url__absolute_in_different_wiki__converted_to_wiki_scheme(
    wiki, page
):
    url = "/wiki/other/page"
    parsed = find_wiki_url(url, wiki, page)
    assert parsed == (SCHEME_WIKI, "other", "page")


def test_find_wiki_url__relative_in_different_wiki__converted_to_wiki_scheme(
    wiki, page
):
    url = "../../other/page"
    parsed = find_wiki_url(url, wiki, page)
    assert parsed == (SCHEME_WIKI, "other", "page")
