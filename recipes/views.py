from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

import forms
import models

@login_required
def recipes(request, username=None):
    # TODO Check permissions.
    if username is None:
        owner = None
        recipes = models.Recipe.objects.all()
    else:
        owner = get_object_or_404(User, username=username)
        recipes = models.Recipe.objects.filter(owner=owner)
    return render_to_response('recipes.html',
                              {'owner': owner,
                               'recipes': recipes},
                              context_instance=RequestContext(request))

@login_required
def recipe(request, username, slug):
    # TODO Check permissions.
    owner = get_object_or_404(User, username=username)
    recipe = get_object_or_404(models.Recipe, owner=owner, slug=slug)
    if 'POST' == request.method:
        form = forms.RecipeForm(request.user, request.POST, instance=recipe)
        if form.is_valid():
            recipe = form.save()
            if slug != recipe.slug:
                return redirect(recipe)
    else:
        form = forms.RecipeForm(request.user, instance=recipe)
    return render_to_response('recipe.html',
                              {'form': form,
                               'recipe': recipe},
                              context_instance=RequestContext(request))
