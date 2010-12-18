from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
import haystack.forms

import forms

@login_required
def index(request):
    """
    The homepage is a workhorse.  Requested via GET with no parameters,
    it is a simple navigation page.  Requested via GET with parameters,
    it searches recipes.  Requested via POST, it saves a recipe.
    """
    if 'POST' == request.method:
        pass
    elif 'q' in request.GET:
        form = haystack.forms.SearchForm(request.GET)
        if form.is_valid():
            results = form.search().filter(owner=request.user)
        else:
            results = []
        return render_to_response('search.html',
                                  {'form': form,
                                   'results': results},
                                  context_instance=RequestContext(request))
    return render_to_response('index.html',
                              context_instance=RequestContext(request))

def signup(request):
    if 'POST' == request.method:
        form = forms.Signup(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('/')
    else:
        form = forms.Signup()
    return render_to_response('signup.html',
                              {'form': form},
                              context_instance=RequestContext(request))
