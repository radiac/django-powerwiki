from django.urls import re_path

from . import app_settings, views
from .constants import ASSET_NAME_PATTERN, PAGE_PATH_PATTERN, WIKI_SLUG_PATTERN


app_name = "powerwiki"


url_dict = {}
url_prefix = ""

if app_settings.SINGLE_MODE:
    url_dict = {
        "wiki_slug": app_settings.SINGLE_SLUG,
    }

else:
    url_prefix = fr"(?P<wiki_slug>{WIKI_SLUG_PATTERN})/"


urlpatterns = [
    re_path(
        fr"^{url_prefix}(?P<page_path>{PAGE_PATH_PATTERN})/_edit/$",
        views.page_edit,
        url_dict,
        name="page-edit",
    ),
    re_path(
        fr"^{url_prefix}(?P<page_path>{PAGE_PATH_PATTERN})/$",
        views.page,
        url_dict,
        name="page",
    ),
    re_path(fr"^{url_prefix}_import/$", views.wiki_import, url_dict, name="import",),
    re_path(fr"^{url_prefix}_search/$", views.search, url_dict, name="search",),
    re_path(
        fr"^{url_prefix}_asset/(?P<asset_name>{ASSET_NAME_PATTERN})/$",
        views.asset,
        url_dict,
        name="asset",
    ),
    re_path(
        fr"^{url_prefix}_asset/(?P<asset_name>{ASSET_NAME_PATTERN})/_edit/$",
        views.asset_edit,
        url_dict,
        name="asset-edit",
    ),
    re_path(fr"^{url_prefix}$", views.page, url_dict, name="page"),
]

if not app_settings.SINGLE_MODE:
    urlpatterns.append(re_path(r"^$", views.index, name="index"),)
