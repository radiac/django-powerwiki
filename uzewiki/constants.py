"""
Uzewiki constants
"""

# Permissions
PERM_SU     = 3
PERM_STAFF  = 2
PERM_USERS  = 1
PERM_PUBLIC = 0
PERM_CHOICES = (
    (PERM_SU,       'Superusers only'),
    (PERM_STAFF,    'Staff only'),
    (PERM_USERS,    'All users'),
    (PERM_PUBLIC,   'Public'),
)

