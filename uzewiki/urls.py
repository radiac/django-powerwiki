from django.conf.urls.defaults import patterns, include, url

from uzewiki import settings

if settings.SINGLE:
    url_dict = {
        'wiki_slug': settings.SINGLE_SLUG,
    }
    
    urlpatterns = patterns('uzewiki.views',
        url(r'^(?P<page_slug>[-\w]+(/[-\w]+)*)/!edit/$', 'edit', url_dict,
            name='uzewiki-edit',
        ),
        url(r'^(?P<page_slug>[-\w]+(/[-\w]+)*)/$', 'show', url_dict,
            name='uzewiki-show',
        ),
        url(r'^!import/$', 'wiki_import', url_dict,
            name='uzewiki-import',
        ),
        url(r'^!search/$', 'search', url_dict,
            name='uzewiki-search',
        ),
        url(r'^$', 'show', url_dict,
            name='uzewiki-show',
        ),
    )
else:
    urlpatterns = patterns('uzewiki.views',
        url(r'^(?P<wiki_slug>[-\w]+)/(?P<page_slug>[-\w]+(/[-\w]+)*)/!edit/$',
            'edit',
            name='uzewiki-edit',
        ),
        url(r'^(?P<wiki_slug>[-\w]+)/(?P<page_slug>[-\w]+(/[-\w]+)*)/$',
            'show',
            name='uzewiki-show'
        ),
        url(r'^(?P<wiki_slug>[-\w]+)/$', 'show',
            name='uzewiki-show'
        ),
        url(r'^(?P<wiki_slug>[-\w]+)/!import/$', 'wiki_import',
            name='uzewiki-import',
        ),
        url(r'^(?P<wiki_slug>[-\w]+)/!search/$', 'search',
            name='uzewiki-search',
        ),
        url(r'^$', 'index',
            name='uzewiki-index'
        ),
    )
