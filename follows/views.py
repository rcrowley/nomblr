from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext

import models

@login_required
def follow(request, username):
    if 'POST' != request.method:
        return HttpResponseNotAllowed(['POST'])
    other = get_object_or_404(User, username=username)
    models.Follow.objects.create(follower=request.user,
                                 followee=other)
    return redirect('/{0}/'.format(other.username))

@login_required
def unfollow(request, username):
    if 'POST' != request.method:
        return HttpResponseNotAllowed(['POST'])
    other = get_object_or_404(User, username=username)
    request.user.following.filter(followee=other).delete()
    return redirect('/{0}/'.format(other.username))
