from docutils.core import publish_parts

from .base import MarkupEngine


class RestructuredText(MarkupEngine):
    docutils_settings = {}

    def to_html(self, raw: str) -> str:
        # Convert to HTML
        parts = publish_parts(
            source=raw,
            writer_name="html4css1",
            settings_overrides=self.docutils_settings,
        )
        html = parts["fragment"]

        return html
