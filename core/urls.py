from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'nomblr.core.views.index'),
)
