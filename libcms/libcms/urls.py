from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    (r'^', include('index.urls', namespace='index')),
    (r'^core/', include('core.urls', namespace='core')),
    (r'^accounts/', include('accounts.urls', namespace='accounts')),
    (r'^filebrowser/', include('filebrowser.urls', namespace='filebrowser')),
    (r'^menu/', include('menu.urls', namespace='menu')),
    (r'^pages/', include('pages.urls', namespace='pages')),
    (r'^news/', include('news.urls', namespace='news')),
    (r'^newinlib/', include('newinlib.urls', namespace='newinlib')),
    (r'^gallery/', include('gallery.urls', namespace='gallery')),
    (r'^polls/', include('polls.urls', namespace='polls')),
    (r'^ask_librarian/', include('ask_librarian.urls', namespace='ask_librarian')),
    (r'^events/', include('events.urls', namespace='events')),
    url(r'^testapp/', include('testapp.urls', namespace='testapp')),
    url(r'^radmin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^radmin/', include(admin.site.urls)),
)

# urlpatterns = patterns('',
#     (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
# )

from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )