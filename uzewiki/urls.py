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
        url(r'^!import/$', 'import', url_dict,
            name='uzewiki-show',
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
        url(r'^$', 'index',
            name='uzewiki-index'
        ),
    )
