from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
import haystack.forms

import forms
import recipes.forms
import recipes.views

@login_required
def index(request):
    """
    The homepage is a workhorse.  Requested via GET with no parameters,
    it is a simple navigation page.  Requested via GET with parameters,
    it searches recipes.  Requested via POST, it saves a recipe.
    """
    if 'GET' == request.method and 'q' in request.GET:
        form = haystack.forms.SearchForm(request.GET)
        if form.is_valid():
            owners = [f.followee for f in request.user.following.all()]
            owners.append(request.user)
            paginator = Paginator(form.search().filter(owner__in=owners), 15)
        else:
            paginator = Paginator([], 15)
        results = paginator.page(int(request.GET.get('page', 1)))
        return render_to_response('search.html',
                                  {'form': form,
                                   'results': results},
                                  context_instance=RequestContext(request))
    elif 'POST' == request.method:
        form = recipes.forms.RecipeForm(request.user, request.POST)
        if form.is_valid():
            recipe = form.save()
            return redirect(recipe)
        else:
            return HttpResponseBadRequest()
    else:
        return recipes.views.recipes(request)

def signup(request, invite_code=''):
    if 'POST' == request.method:
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('/')
    else:
        form = forms.SignupForm(initial={'invite_code': invite_code})
    return render_to_response('signup.html',
                              {'form': form},
                              context_instance=RequestContext(request))

@login_required
def logout(request, *args, **kwargs):
    if 'POST' == request.method:
        return views.logout(request, *args, **kwargs)
    return HttpResponseNotAllowed(['POST'])
