import markdown

from .base import MarkupEngine


class Markdown(MarkupEngine):
    label = "Markdown"
    extensions = ["extra"]

    def to_html(self, raw: str) -> str:
        md = markdown.markdown(raw, extensions=self.extensions)
        return md
