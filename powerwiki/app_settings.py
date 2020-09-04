from yaa_settings import AppSettings

from . import constants


class PowerwikiSettings(AppSettings):
    prefix = "POWERWIKI"

    # If True, run powerwiki in single wiki mode
    SINGLE_MODE = False

    # Slug for the wiki definition to use in single wiki mode
    # Must be lower case
    def SINGLE_SLUG(self, value):
        return (value or "default").lower()

    # Permissions for who can see the wiki index (list of wikis)
    # Users will only see those wikis which they have access to
    PERM_INDEX = constants.PERM_PUBLIC

    # Path for the front page of the wiki
    # Must be lower case
    def FRONT_PATH(self, value):
        return (value or "index").lower()

    # Tags to check for wiki links
    # List of (tag, attribute) pairs
    LINK_TAGS = [
        ("a", "href"),
        ("img", "src"),
    ]

    # Available markup engines
    MARKUP_ENGINES = [
        "powerwiki.markup.rest.RestructuredText",
        "powerwiki.markup.md.Markdown",
        "powerwiki.markup.plain.PlainText",
    ]

    # Default markup engine
    MARKUP_ENGINE_DEFAULT = "powerwiki.markup.rest.RestructuredText"

    # HTML parser for BeautifulSoup
    HTML_PARSER = "html.parser"
