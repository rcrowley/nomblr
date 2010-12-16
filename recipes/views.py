from django.shortcuts import render_to_response
from django.template import RequestContext

import models

#def index(request, username=None, slug=None):
def index(request, **kwargs):
    username = kwargs.get('username')
    slug = kwargs.get('slug')
    print(username)
    print(slug)
    if username is None:
        recipes = models.Recipe.objects.all()
    else:
        recipes = models.Recipe.objects.filter(username=username, slug=slug)
    return render_to_response('recipes/index.html',
                              {'recipes': recipes},
                              context_instance=RequestContext(request))

def recipe(request, username, slug):
    r = models.Recipe.objects.get(username=username, slug=slug)
    return render_to_response('recipes/recipe.html',
                              {'recipe': r},
                              context_instance=RequestContext(request))
