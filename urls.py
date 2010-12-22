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

    (r'^forgot/$', 'django.contrib.auth.views.password_reset',
     {'template_name': 'password_reset_form.html',
      'email_template_name': 'password_reset_email.txt'}),
    (r'^forgot/sent/$', 'django.contrib.auth.views.password_reset_done',
     {'template_name': 'password_reset_done.html'}),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
     'django.contrib.auth.views.password_reset_confirm',
     {'template_name': 'password_reset_confirm.html'}),
    (r'^reset/done/$',
     'django.contrib.auth.views.password_reset_complete',
     {'template_name': 'password_reset_complete.html'}),

    # It's important username-based routes follow specific routes.
    (r'^(?P<username>[^/]+)/$', 'nomblr.recipes.views.recipes'),
    (r'^(?P<username>[^/]+)/(?P<slug>[^/]+)/$', 'nomblr.recipes.views.recipe'),

    (r'^$', 'nomblr.views.index'),

)
