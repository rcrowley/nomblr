from datetime import datetime
from django.contrib.admin.models import LogEntry, CHANGE
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseNotAllowed
from django.shortcuts import render_to_response
from django.template import RequestContext
import hashlib
import hmac
import json
import urllib2

import forms
import models

@login_required
def account(request):
    return render_to_response('account.html',
                              context_instance=RequestContext(request))

@login_required
def email(request):
    if 'POST' == request.method:
        form = forms.EmailForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = forms.EmailForm(instance=request.user)
    return render_to_response('email.html',
                              {'form': form},
                              context_instance=RequestContext(request))

@login_required
def email_confirmation(request, token):
    if token != hmac.new(settings.SECRET_KEY,
                         request.user.email,
                         hashlib.sha1).hexdigest():
        raise Http404
    LogEntry(user=request.user,
             action_flag=CHANGE,
             change_message='confirmed {0}'.format(request.user.email)).save()
    return render_to_response('email_confirmation.html',
                              context_instance=RequestContext(request))

@login_required
def username(request):
    if 'POST' == request.method:
        form = forms.UsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = forms.UsernameForm(instance=request.user)
    return render_to_response('username.html',
                              {'form': form},
                              context_instance=RequestContext(request))

@login_required
def friends(request):
    if 'POST' == request.method:
        form = forms.FacebookSessionForm(request.POST,
                                         instance=request.user.get_profile())
        if form.is_valid():
            form.save()

    # Fetch the followers/followees.
    following = request.user.following.all()
    followers = request.user.followers.all()

    # Compute Facebook graph intersections.
    # TODO Pagination.
    profile = request.user.get_profile()
    expiry = profile.facebook_expiry
    facebook_login = expiry is None or expiry < datetime.now()
    try:
        response = urllib2.urlopen(
            'https://graph.facebook.com/{0}/friends?access_token={1}'.format(
                profile.facebook_id,
                profile.facebook_token))
        object = json.loads(response.read())
        facebook_friends = models.Profile.objects.select_related().filter(
            facebook_id__in=[friend[u'id'] for friend in object[u'data']])
    except urllib2.HTTPError as e:
        # TODO Log e.
        facebook_friends = []

    return render_to_response('friends.html',
                              {'following': following,
                               'followers': followers,
                               'facebook_login': facebook_login,
                               'facebook_friends': facebook_friends},
                              context_instance=RequestContext(request))
