from __future__ import annotations

import typing


if typing.TYPE_CHECKING:
    from ..models import Page, Wiki


class MarkupEngine:
    wiki: Wiki
    page: Page
    label: str = "Unknown"

    def __init__(self, wiki: Wiki, page: Page):
        self.wiki = wiki
        self.page = page

    def render(self, raw: str) -> str:
        raw = self.pre(raw)
        html = self.to_html(raw)
        html = self.post(html)
        return html

    def pre(self, raw: str) -> str:
        return raw

    def to_html(self, raw) -> str:
        raise NotImplementedError()

    def post(self, html: str) -> str:
        from ..html import process

        html = process(html, wiki=self.wiki, page=self.page)
        return html
