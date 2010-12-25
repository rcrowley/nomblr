from django.conf import settings
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

    (r'^account/password/reset/$',
     'django.contrib.auth.views.password_reset',
     {'template_name': 'password_reset_form.html',
      'email_template_name': 'password_reset_email.txt'}),
    (r'^account/password/reset/sent/$',
     'django.contrib.auth.views.password_reset_done',
     {'template_name': 'password_reset_done.html'}),
    (r'^account/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
     'django.contrib.auth.views.password_reset_confirm',
     {'template_name': 'password_reset_confirm.html'}),
    (r'^account/password/reset/done/$',
     'django.contrib.auth.views.password_reset_complete',
     {'template_name': 'password_reset_complete.html'}),

    (r'^account/$', 'nomblr.account.views.account'),
    (r'^account/email/$', 'nomblr.account.views.email'),
    (r'^account/email/(?P<token>.+)/$',
     'nomblr.account.views.email_confirmation'),
    (r'^account/password/$', 'django.contrib.auth.views.password_change',
     {'template_name': 'password_change_form.html'}),
    (r'^account/password/done/$',
     'django.contrib.auth.views.password_change_done',
     {'template_name': 'password_change_done.html'}),
    (r'^account/username/$', 'nomblr.account.views.username'),

    # It's important username-based routes follow specific routes.
    (r'^(?P<username>[^/]+)/$', 'nomblr.recipes.views.recipes'),
    (r'^(?P<username>[^/]+)/(?P<slug>[^/]+)/$', 'nomblr.recipes.views.recipe'),

    (r'^$', 'nomblr.views.index'),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': '/home/vagrant/work/nomblr/static'}),
    )
