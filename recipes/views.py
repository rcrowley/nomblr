from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

import forms
import models

@login_required
def recipes(request, username=None):
    if username is None:
        owners = [f.followee for f in request.user.following.all()]
        owners.append(request.user)
        qs = models.Recipe.objects.filter(owner__in=owners) \
                                  .order_by('-created')
        newest_recipes = qs[0:3]
        paginator = Paginator(qs, 15)
        recipes = paginator.page(int(request.GET.get('page', 1)))
        viewed_recipes = [] # TODO
        return render_to_response('browse.html',
                                  {'newest_recipes': newest_recipes,
                                   'recipes': recipes,
                                   'viewed_recipes': viewed_recipes},
                                  context_instance=RequestContext(request))
    else:
        owner = get_object_or_404(User, username=username)
        paginator = Paginator(models.Recipe.objects.filter(owner=owner), 15)
        recipes = paginator.page(int(request.GET.get('page', 1)))
        return render_to_response('profile.html',
                                  {'owner': owner,
                                   'recipes': recipes},
                                  context_instance=RequestContext(request))

@login_required
def recipe(request, username, slug):
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
    if request.is_ajax():
        template_name = 'recipe_article.html'
    else:
        template_name = 'recipe.html'
    return render_to_response(template_name,
                              {'form': form,
                               'recipe': recipe},
                              context_instance=RequestContext(request))
