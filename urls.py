from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    (r'^admin/', include(admin.site.urls)),

    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),

    (r'^recipes/', include('nomblr.recipes.urls')),

    (r'^signup/$', 'nomblr.views.signup'),
    (r'^$', 'nomblr.views.index'),

)
