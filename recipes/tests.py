from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import Client
import haystack.forms

import forms
import models
import search_indexes
import templatetags.mdown
import views

def test_RecipeForm_valid():
    user = User.objects.get(username='tester')
    form = forms.RecipeForm(user, {'name': 'Test recipe',
                                   'text': 'Test ingredients and directions.'})
    assert form.is_valid()

def test_RecipeForm_blacklisted_name():
    user = User.objects.get(username='tester')
    form = forms.RecipeForm(user, {'name': 'follow',
                                   'text': 'Test ingredients and directions.'})
    assert not form.is_valid()
    assert 'name' in form.errors

def test_RecipeForm_missing_name():
    user = User.objects.get(username='tester')
    form = forms.RecipeForm(user, {'text': 'Test ingredients and directions.'})
    assert not form.is_valid()
    assert 'name' in form.errors

def test_RecipeForm_missing_text():
    user = User.objects.get(username='tester')
    form = forms.RecipeForm(user, {'name': 'Test recipe'})
    assert not form.is_valid()
    assert 'text' in form.errors

def test_Recipe_create():
    user = User.objects.get(username='tester')
    recipe = models.Recipe.objects.create(
        owner=user,
        name='Test recipe',
        text='Test ingredients and directions.')
    assert recipe.id is not None
    assert 'test-recipe' == recipe.slug
    try:
        models.Recipe.objects.create(
            owner=user,
            name='Test recipe',
            text='Test ingredients and directions.')
        assert False
    except IntegrityError:
        assert True

# TODO Test models further.  Editing, for example.

def test_RecipeIndex_name():
    form = haystack.forms.SearchForm({'q': 'Test recipe'})
    assert form.is_valid()
    user = User.objects.get(username='tester')
    results = form.search().filter(owner=user)
    assert 1 == len(results)

def test_RecipeIndex_text():
    form = haystack.forms.SearchForm({'q': 'ingredients'})
    assert form.is_valid()
    user = User.objects.get(username='tester')
    results = form.search().filter(owner=user)
    assert 1 == len(results)

def test_mdown():
    assert """<ul>
<li>
<p>foo</p>
</li>
<li>
<p>bar</p>
</li>
</ul>
<ol>
<li>baz</li>
</ol>""" == templatetags.mdown.mdown('* foo\n\n* bar\n\n1. baz')

def test_GET_recipes():
    c = Client()
    c.login(username='tester', password='password')
    response = c.get('/tester/')
    assert 200 == response.status_code

def test_GET_other_recipes():
    c = Client()
    c.login(username='othertester', password='password')
    response = c.get('/tester/')
    assert 200 == response.status_code

def test_GET_missing_recipes():
    c = Client()
    c.login(username='tester', password='password')
    response = c.get('/missing/')
    assert 404 == response.status_code

def test_GET_recipe():
    c = Client()
    c.login(username='tester', password='password')
    response = c.get('/tester/foo-bar/')
    assert 200 == response.status_code

def test_GET_other_recipe():
    c = Client()
    c.login(username='othertester', password='password')
    response = c.get('/tester/foo-bar/')
    assert 200 == response.status_code

def test_GET_missing_recipe():
    c = Client()
    c.login(username='tester', password='password')
    response = c.get('/tester/missing/')
    assert 404 == response.status_code
    response = c.get('/missing/missing/')
    assert 404 == response.status_code

def test_POST_recipe():
    c = Client()
    c.login(username='tester', password='password')
    response = c.post('/tester/foo-bar/',
                      {'name': 'Foo bar',
                       'text': '* foo\n* bar\n\n1. baz\n1. bang'})
    assert 200 == response.status_code

def test_POST_invalid_recipe():
    c = Client()
    c.login(username='tester', password='password')
    response = c.post('/tester/foo-bar/', {'name': 'Foo bar'})
    assert 200 == response.status_code

def test_POST_recipe_rename():
    c = Client()
    c.login(username='tester', password='password')
    response = c.post('/tester/foo-bar/',
                      {'name': 'Foo bar baz',
                       'text': '* foo\n* bar\n\n1. baz\n1. bang'})
    assert 302 == response.status_code
    assert 'http://testserver/tester/foo-bar-baz/' == response['Location']

def test_DELETE_recipe():
    c = Client()
    c.login(username='tester', password='password')
    c.post('/', {'name': 'Deletable', 'text': 'Deletable.'})
    user = User.objects.get(username='tester')
    models.Recipe.objects.create(owner=user, name='Delete me', text='')
    response = c.delete('/tester/delete-me/')
    assert 302 == response.status_code
    try:
        models.Recipe.objects.get(owner=user, slug='delete-me')
        assert False
    except models.Recipe.DoesNotExist:
        assert True
