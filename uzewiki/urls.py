from django.conf.urls import include, url

from uzewiki import settings
from uzewiki import views

if settings.SINGLE:
    url_dict = {
        'wiki_slug': settings.SINGLE_SLUG,
    }

    urlpatterns = [
        url(
            r'^(?P<page_slug>[-\w]+(/[-\w]+)*)/:edit/$',
            views.edit,
            url_dict,
            name='edit',
        ),
        url(
            r'^(?P<page_slug>[-\w]+(/[-\w]+)*)/$',
            views.show,
            url_dict,
            name='show',
        ),
        url(
            r'^:import/$',
            views.wiki_import,
            url_dict,
            name='import',
        ),
        url(
            r'^:search/$',
            views.search,
            url_dict,
            name='search',
        ),
        url(
            r'^:asset/(?P<asset_name>[-\w]+)/$',
            views.asset_details,
            url_dict,
            name='asset',
        ),
        url(
            r'^:asset/(?P<asset_name>[-\w]+)/edit/$',
            views.asset_edit,
            url_dict,
            name='asset-edit',
        ),
        url(r'^$',
            views.show,
            url_dict,
            name='show',
        ),
        url(
            r'^$',
            views.show,
            url_dict,
            name='index',
        ),
    ]
else:
    urlpatterns = [
        url(
            r'^(?P<wiki_slug>[-\w]+)/(?P<page_slug>[-\w]+(/[-\w]+)*)/:edit/$',
            views.edit,
            name='edit',
        ),
        url(
            r'^(?P<wiki_slug>[-\w]+)/(?P<page_slug>[-\w]+(/[-\w]+)*)/$',
            views.show,
            name='show'
        ),
        url(
            r'^(?P<wiki_slug>[-\w]+)/$',
            views.show,
            name='show'
        ),
        url(
            r'^(?P<wiki_slug>[-\w]+)/:import/$',
            views.wiki_import,
            name='import',
        ),
        url(
            r'^(?P<wiki_slug>[-\w]+)/:search/$',
            views.search,
            name='search',
        ),
        url(
            r'^(?P<wiki_slug>[-\w]+)/:asset/(?P<asset_name>[-\w]+)/$',
            views.asset_details,
            name='asset',
        ),
        url(
            r'^(?P<wiki_slug>[-\w]+)/:asset/(?P<asset_name>[-\w]+)/edit/$',
            views.asset_edit,
            name='asset-edit',
        ),
        url(
            r'^$',
            views.index,
            name='index'
        ),
    ]
