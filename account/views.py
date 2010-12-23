from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

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
