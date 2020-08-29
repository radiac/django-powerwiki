import markdown

from .base import MarkupEngine


class Markdown(MarkupEngine):
    extensions = ["extra"]

    def to_html(self, raw: str) -> str:
        md = markdown.Markdown(extensions=self.extensions)
        md.convert(raw)
        return md
