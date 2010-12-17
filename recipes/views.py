from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

import models

@login_required
def recipes(request, username=None):
    # TODO Check permissions.
    if username is None:
        recipes = models.Recipe.objects.all()
    else:
        recipes = models.Recipe.objects.filter(username=username)
    return render_to_response('recipes.html',
                              {'recipes': recipes},
                              context_instance=RequestContext(request))

@login_required
def recipe(request, username, slug):
    # TODO Check permissions.
    recipe = models.Recipe.objects.get(username=username, slug=slug)
    return render_to_response('recipe.html',
                              {'recipe': recipe},
                              context_instance=RequestContext(request))
