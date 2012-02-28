from django.conf.urls import patterns, include, url

from packages.views import PackageList, PackageDetailView, VersionDetailView
"""
Lifted directly from https://github.com/refreshoxford/django-cbv-inspector/blob/master/inspector/cbv/urls.py

URL variations:
project
project/version
project/version/module
project/version/module/class

e.g.
django
django/1.41a
django/1.41a/core
django/1.41a/core/DjangoRuntimeWarning

"""

urlpatterns = patterns('',
    url(r'^$', PackageList.as_view(), name='package_list'),
    url(r'^(?P<package>[a-zA-Z_-]+)/$', PackageDetailView.as_view(), name='package-detail'),
    url(r'^(?P<package>[a-zA-Z_-]+)/(?P<version>[^/]+)/$', VersionDetailView.as_view(), name='version-detail'),
#     url(r'^(?P<package>[a-zA-Z_-]+)/(?P<version>[^/]+)/(?P<module>[\.A-Za-z_-]+)/$', ModuleDetailView.as_view(), name='module-detail'),
#     url(r'^(?P<package>[a-zA-Z_-]+)/(?P<version>[^/]+)/(?P<module>[\.A-Za-z_-]+)/(?P<klass>[A-Za-z_-]*)/$', KlassDetailView.as_view(), name='klass-detail'),
)
