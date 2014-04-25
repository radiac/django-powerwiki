from django.conf import settings

from uzewiki import constants

# If true, add jQuery to the page when required
ADD_JQUERY = getattr(settings, 'UZEWIKI_ADD_JQUERY', True)

# If True, run uzewiki in single wiki mode
SINGLE = getattr(settings, 'UZEWIKI_SINGLE', False)

# Slug for the wiki definition to use in single wiki mode 
# Must be lower case
SINGLE_SLUG = getattr(settings, 'UZEWIKI_SINGLE_SLUG', 'default').lower()

# Permissions for who can see the wiki index (list of wikis)
# Users will only see those wikis which they have access to
PERM_INDEX = getattr(settings, 'UZEWIKI_PERM_INDEX', constants.PERM_PUBLIC)

# Slug for the front page of the wiki
# Must be lower case
FRONT_SLUG = getattr(settings, 'UZEWIKI_FRONT_SLUG', 'index').lower()
