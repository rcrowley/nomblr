from django.contrib.auth import forms
from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    return render_to_response('index.html',
                              context_instance=RequestContext(request))

def signup(request):
    if 'POST' == request.method:
    else:
        form = forms.UserCreationForm()
    return render_to_response('signup.html',
                              {'form': form},
                              context_instance=RequestContext(request))
