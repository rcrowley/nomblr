from django.contrib.auth.models import User
from django.db import connection
from django.db import IntegrityError
from django.test import Client
import haystack.forms

import forms
import models
import search_indexes
import templatetags.mdown
import views

def setup():
    connection.cursor().execute(
        'CREATE UNIQUE INDEX uri ON recipes_recipe (owner_id, slug);')

def test_RecipeForm_valid():
    user = User.objects.get(username='tester')
    form = forms.RecipeForm(user, {'name': 'Test recipe',
                                   'text': 'Test ingredients and directions.'})
    assert form.is_valid()

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

def test_RecipeIndex_signalled():
    form = haystack.forms.SearchForm({'q': 'Test recipe'})
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
