from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
import os.path

admin.autodiscover()

urlpatterns = patterns('',

    # For your eyes only.
    (r'^admin/', include(admin.site.urls)),

    # Authentication.
    (r'^signup/$', 'nomblr.views.signup'),
    (r'^signup/(?P<invite_code>[0-9a-f]{40})/$', 'nomblr.views.signup'),
    (r'^login/$', 'django.contrib.auth.views.login',
     {'template_name': 'login.html'}),
    (r'^logout/$', 'nomblr.views.logout',
     {'template_name': 'logged_out.html'}),

    # Passwords.
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

    # Email addresses and usernames.
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

    # Recipes.  It's important username-based routes follow specific routes
    # and for the recipe slug route to follow more specific username-based
    # routes.
    (r'^(?P<username>[^/]+)/$', 'nomblr.recipes.views.recipes'),
    (r'^(?P<username>[^/]+)/follow/$', 'nomblr.follows.views.follow'),
    (r'^(?P<username>[^/]+)/unfollow/$', 'nomblr.follows.views.unfollow'),
    (r'^(?P<username>[^/]+)/(?P<slug>[^/]+)/$', 'nomblr.recipes.views.recipe'),

    # Homepage.
    (r'^$', 'nomblr.views.index'),

)

# Static file serving for development.
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': os.path.join(os.path.dirname(__file__), 'static')}),
    )
