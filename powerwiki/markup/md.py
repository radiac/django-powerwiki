from django.contrib.auth.models import AbstractUser

import markdown

from .base import MarkupEngine


class Markdown(MarkupEngine):
    label = "Markdown"
    extensions = ["extra"]

    def to_html(self, raw: str, user: AbstractUser) -> str:
        md = markdown.markdown(raw, extensions=self.extensions)
        return md
