from django.contrib.admin.models import LogEntry, CHANGE
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
import hashlib
import hmac

import forms

@login_required
def account(request):
    return render_to_response('account.html',
                              context_instance=RequestContext(request))

@login_required
def email(request):
    return render_to_response('email.html',
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
