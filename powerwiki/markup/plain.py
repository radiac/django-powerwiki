from django.utils.html import linebreaks

from .base import MarkupEngine


class PlainText(MarkupEngine):
    extensions = ["extra"]

    def to_html(self, raw: str) -> str:
        return linebreaks(raw, autoescape=True)