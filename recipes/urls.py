from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'nomblr.recipes.views.index'),
    (r'(?P<username>[^/]+)/$', 'nomblr.recipes.views.index'),
    (r'\*/(?P<slug>[^/]+)/$', 'nomblr.recipes.views.index'),
    (r'(?P<username>[^/]+)/(?P<slug>[^/]+)/$', 'nomblr.recipes.views.recipe'),
)
