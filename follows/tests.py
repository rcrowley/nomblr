from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import Client

import forms
import models
import views

def test_Follow_create():
    tester = User.objects.get(username='tester')
    othertester = User.objects.get(username='othertester')
    follow = models.Follow.objects.create(follower=tester,
                                          followee=othertester)
    assert follow.id is not None
    try:
        models.Follow.objects.create(follower=tester,
                                     followee=othertester)
        assert False
    except IntegrityError:
        assert True
    assert 1 == len(tester.following.all())
    assert 0 == len(othertester.following.all())
    assert 0 == len(tester.followers.all())
    assert 1 == len(othertester.followers.all())

def test_Follow_destroy():
    tester = User.objects.get(username='tester')
    othertester = User.objects.get(username='othertester')
    tester.following.filter(followee=othertester).delete()
    assert 0 == len(tester.following.all())
    assert 0 == len(othertester.followers.all())

def test_POST_follow():
    c = Client()
    c.login(username='tester', password='password')
    response = c.post('/othertester/follow/', {})
    assert 302 == response.status_code
    assert 'http://testserver/othertester/' == response['Location']
    tester = User.objects.get(username='tester')
    othertester = User.objects.get(username='othertester')
    assert 1 == len(tester.following.all())
    assert 0 == len(othertester.following.all())
    assert 0 == len(tester.followers.all())
    assert 1 == len(othertester.followers.all())

def test_POST_unfollow():
    c = Client()
    c.login(username='tester', password='password')
    response = c.post('/othertester/unfollow/', {})
    assert 302 == response.status_code
    assert 'http://testserver/othertester/' == response['Location']
    tester = User.objects.get(username='tester')
    othertester = User.objects.get(username='othertester')
    assert 0 == len(tester.following.all())
    assert 0 == len(othertester.followers.all())
