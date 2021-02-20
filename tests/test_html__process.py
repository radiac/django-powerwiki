"""
Test conversion functions in html.py
"""

from django.contrib.auth.models import AnonymousUser
from django.test.html import parse_html

from powerwiki.html import process


def test_process__sample__links_are_updated(wiki, page, asset):
    raw = f"""
    <p><a href="/app">example</a></p>
    <p><a href="other">other</a></p>
    <p><a href="wiki:sibling">sibling</a></p>
    <p><img src="asset:{asset.name}"></p>
    """
    expected = f"""
    <p>
        <a href="/app">example</a>
    </p>
    <p>
        <a
            href="/wiki/slug/parent/other/"
            data-edit="/wiki/slug/parent/other/_edit/"
            data-missing="True"
            class="powerwiki__wiki"
        >other</a>
    </p>
    <p>
        <a
            href="/wiki/slug/sibling/"
            data-edit="/wiki/slug/sibling/_edit/"
            data-missing="True"
            class="powerwiki__wiki"
        >sibling</a>
    </p>
    <p>
        <img
            src="{asset.file.url}"
            data-edit="/wiki/slug/_asset/{asset.name}/_edit/"
            class="powerwiki__asset"
        >
    </p>
    """

    processed = process(raw, wiki=wiki, page=page, user=AnonymousUser())
    assert parse_html(processed) == parse_html(expected)
