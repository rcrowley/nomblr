from django.shortcuts import render_to_response
from django.template import RequestContext

import models

def recipes(request, username=None):
    print(username)
    if username is None:
        recipes = models.Recipe.objects.all()
    else:
        recipes = models.Recipe.objects.filter(username=username)
    return render_to_response('recipes.html',
                              {'recipes': recipes},
                              context_instance=RequestContext(request))

def recipe(request, username, slug):
    recipe = models.Recipe.objects.get(username=username, slug=slug)
    return render_to_response('recipe.html',
                              {'recipe': recipe},
                              context_instance=RequestContext(request))
