"""
Powerwiki constants
"""

# Permissions
PERM_SU = 3
PERM_STAFF = 2
PERM_USERS = 1
PERM_PUBLIC = 0
PERM_CHOICES = (
    (PERM_SU, "Superusers only"),
    (PERM_STAFF, "Staff only"),
    (PERM_USERS, "All users"),
    (PERM_PUBLIC, "Public"),
)

# URL scheme names
SCHEME_WIKI = "wiki"
SCHEME_ASSET = "asset"
SCHEME_IMAGE = "image"
SCHEME_INDEX = "index"

# URL patterns
WIKI_SLUG_PATTERN = r"[a-zA-Z0-9][-\w]*"
PAGE_PATH_PATTERN = r"[a-zA-Z0-9].*?(/[a-zA-Z0-9][- \w]*)*"
ASSET_NAME_PATTERN = r"[a-zA-Z0-9].*?"

# Powerwiki tags
TAG_OPEN = "[["
TAG_SCHEME_SEPARATOR = ":"
TAG_LABEL_SEPARATOR = "|"
TAG_CLOSE = "]]"
