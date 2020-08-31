from docutils.core import publish_parts

from .base import MarkupEngine


class RestructuredText(MarkupEngine):
    label = "reStructuredText"
    docutils_settings = {
        "doctitle_xform": False,
    }

    def to_html(self, raw: str) -> str:
        # Convert to HTML
        parts = publish_parts(
            source=raw, writer_name="html", settings_overrides=self.docutils_settings,
        )
        html = parts["fragment"]

        return html
