from django.contrib.auth.models import User
from django.test import Client

import forms
import models
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

def test_UsernameForm_blacklisted_username():
    form = forms.UsernameForm({'username': 'api'})
    assert not form.is_valid()
    assert 'username' in form.errors

def test_UsernameForm_invalid_username():
    form = forms.UsernameForm({'username': 'invalid username'})
    assert not form.is_valid()
    assert 'username' in form.errors

def test_FacebookSessionForm_valid():
    form = forms.FacebookSessionForm({'facebook_id': '3101064',
                                      'facebook_token': '195241420501723|2.pt6jSDUVTpdaJAXHJElLdg__.3600.1296867600-3101064|Ho71oAPel6ectNVSECtvzge4UgM',
                                      'facebook_expiry': 2147483647})
    assert form.is_valid()

def test_FacebookSessionForm_invalid_expiry():
    form = forms.FacebookSessionForm({'facebook_id': '3101064',
                                      'facebook_token': '195241420501723|2.pt6jSDUVTpdaJAXHJElLdg__.3600.1296867600-3101064|Ho71oAPel6ectNVSECtvzge4UgM',
                                      'facebook_expiry': 99999999999999999999})
    assert not form.is_valid()
    assert 'facebook_expiry' in form.errors

def test_Profile_create():
    try:
        user = User(username='testprofile')
        user.save()
        assert user == user.get_profile().user
    except models.Profile.DoesNotExist as e:
        assert False

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
    response = c.post('/account/email/', {'email': 'different@nomblr.com'})
    assert 200 == response.status_code
    response = c.post('/account/email/', {'email': 'tester@nomblr.com'})
    assert 200 == response.status_code

def test_POST_invalid_email():
    c = Client()
    c.login(username='tester', password='password')
    response = c.get('/account/email/', {'email': 'invalid email'})
    assert 200 == response.status_code

def test_GET_email_confirmation():
    c = Client()
    c.login(username='tester', password='password')
    response = c.get(
        '/account/email/0123456789012345678901234567890123456789/',
        {'email': 'invalid email'})
    assert 404 == response.status_code
    response = c.get(
        '/account/email/008f397608af6f1eff8c6ff1e7231b3f4e500334/',
        {'email': 'invalid email'})
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

def test_GET_friends():
    c = Client()
    c.login(username='tester', password='password')
    response = c.get('/friends/')
    assert 200 == response.status_code

def test_POST_friends():
    c = Client()
    c.login(username='tester', password='password')
    response = c.post('/friends/', {'facebook_id': '3101064',
                                    'facebook_token': '195241420501723|2.pt6jSDUVTpdaJAXHJElLdg__.3600.1296867600-3101064|Ho71oAPel6ectNVSECtvzge4UgM',
                                    'facebook_expiry': 2147483647})
    assert 200 == response.status_code
