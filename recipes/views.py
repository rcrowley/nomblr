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

        # TODO Only recipes request.user can access.  Something in between
        # wide open:
        #qs = models.Recipe.objects.all()
        # and completely private:
        qs = models.Recipe.objects.filter(owner=request.user)
        # must eventually be implemented.

        newest_recipes = qs.order_by('-created')[0:3]
        paginator = Paginator(qs, 15)
        recipes = paginator.page(int(request.GET.get('page', 1)))
        viewed_recipes = []
        return render_to_response('browse.html',
                                  {'newest_recipes': newest_recipes,
                                   'recipes': recipes,
                                   'viewed_recipes': viewed_recipes},
                                  context_instance=RequestContext(request))
    else:
        owner = get_object_or_404(User, username=username)

        # TODO Can request.user access owner?
        if owner != request.user:
            raise Http404
        paginator = Paginator(models.Recipe.objects.filter(owner=owner), 15)

        recipes = paginator.page(int(request.GET.get('page', 1)))
        return render_to_response('profile.html',
                                  {'owner': owner,
                                   'recipes': recipes},
                                  context_instance=RequestContext(request))

@login_required
def recipe(request, username, slug):
    owner = get_object_or_404(User, username=username)

    # TODO Can request.user access owner?
    if owner != request.user:
        raise Http404

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
