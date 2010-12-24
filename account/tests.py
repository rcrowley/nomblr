from django.test import Client

import forms
import views

def test_EmailForm_valid():
    form = forms.EmailForm({'email': 'test@nomblr.com'})
    assert form.is_valid()

def test_EmailForm_missing_email():
    form = forms.EmailForm({})
    assert not form.is_valid()
    assert 'email' in form.errors

def test_EmailForm_invalid_email():
    form = forms.EmailForm({'email': 'invalid email'})
    assert not form.is_valid()
    assert 'email' in form.errors

def test_UsernameForm_valid():
    form = forms.UsernameForm({'username': 'test'})
    assert form.is_valid()

def test_UsernameForm_missing_username():
    form = forms.UsernameForm({})
    assert not form.is_valid()
    assert 'username' in form.errors

def test_UsernameForm_invalid_username():
    form = forms.UsernameForm({'username': 'invalid username'})
    assert not form.is_valid()
    assert 'username' in form.errors

def test_GET_account():
    c = Client()
    c.login(username='tester', password='password')
    response = c.get('/account/')
    assert 200 == response.status_code

def test_GET_unauth_account():
    c = Client()
    response = c.get('/account/')
    assert 302 == response.status_code
    assert 'http://testserver/login/?next=/account/' == response['Location']

def test_GET_email():
    c = Client()
    c.login(username='tester', password='password')
    response = c.get('/account/email/')
    assert 200 == response.status_code

def test_POST_email():
    c = Client()
    c.login(username='tester', password='password')
    response = c.get('/account/email/', {'email': 'different@nomblr.com'})
    assert 200 == response.status_code
    response = c.get('/account/email/', {'email': 'tester@nomblr.com'})
    assert 200 == response.status_code

def test_POST_invalid_email():
    c = Client()
    c.login(username='tester', password='password')
    response = c.get('/account/email/', {'email': 'invalid email'})
    assert 200 == response.status_code

def test_GET_password():
    c = Client()
    c.login(username='tester', password='password')
    response = c.get('/account/password/')
    assert 200 == response.status_code

def test_GET_username():
    c = Client()
    c.login(username='tester', password='password')
    response = c.get('/account/username/')
    assert 200 == response.status_code

def test_POST_username():
    c = Client()
    c.login(username='tester', password='password')
    response = c.post('/account/username/', {'username': 'different'})
    assert 200 == response.status_code
    response = c.post('/account/username/', {'username': 'tester'})
    assert 200 == response.status_code

def test_POST_invalid_username():
    c = Client()
    c.login(username='tester', password='password')
    response = c.post('/account/username/', {'username': 'invalid username'})
    assert 200 == response.status_code
