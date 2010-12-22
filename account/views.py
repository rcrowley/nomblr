from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

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
    return render_to_response('username.html',
                              context_instance=RequestContext(request))
