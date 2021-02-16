from __future__ import annotations

import typing

from django.contrib.auth.models import AbstractUser


if typing.TYPE_CHECKING:
    from ..models import Page, Wiki


class MarkupEngine:
    wiki: Wiki
    page: Page
    label: str = "Unknown"

    def __init__(self, wiki: Wiki, page: Page):
        self.wiki = wiki
        self.page = page

    def render(self, raw: str, user: AbstractUser) -> str:
        raw = self.pre(raw, user)
        html = self.to_html(raw, user)
        html = self.post(html, user)
        return html

    def pre(self, raw: str, user: AbstractUser) -> str:
        return raw

    def to_html(self, raw: str, user: AbstractUser) -> str:
        raise NotImplementedError()

    def post(self, html: str, user: AbstractUser) -> str:
        from ..html import process

        html = process(html, wiki=self.wiki, page=self.page, user=user)
        return html
