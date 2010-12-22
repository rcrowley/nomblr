from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    (r'^admin/', include(admin.site.urls)),

    (r'^signup/$', 'nomblr.views.signup'),
    (r'^login/$', 'django.contrib.auth.views.login',
     {'template_name': 'login.html'}),
    (r'^logout/$', 'nomblr.views.logout',
     {'template_name': 'logged_out.html'}),

    # It's important username-based routes follow specific routes.
    (r'^(?P<username>[^/]+)/$', 'nomblr.recipes.views.recipes'),
    (r'^(?P<username>[^/]+)/(?P<slug>[^/]+)/$', 'nomblr.recipes.views.recipe'),

    (r'^$', 'nomblr.views.index'),

)
