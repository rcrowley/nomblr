from django.test import Client

import forms
import views

def test_SignupForm_valid():
    form = forms.SignupForm({'email': 'test@nomblr.com',
                             'username': 'test',
                             'password1': 'password',
                             'password2': 'password',
                             'invite_code': 'aa073e50954855d0533476ad002cce721d1b830d'})
    assert form.is_valid()

def test_SignupForm_missing_email():
    form = forms.SignupForm({'username': 'test',
                             'password1': 'password',
                             'password2': 'password',
                             'invite_code': 'aa073e50954855d0533476ad002cce721d1b830d'})
    assert not form.is_valid()
    assert 'email' in form.errors

def test_SignupForm_invalid_email():
    form = forms.SignupForm({'email': 'invalid email',
                             'username': 'test',
                             'password1': 'password',
                             'password2': 'password',
                             'invite_code': 'aa073e50954855d0533476ad002cce721d1b830d'})
    assert not form.is_valid()
    assert 'email' in form.errors

def test_SignupForm_missing_username():
    form = forms.SignupForm({'email': 'test@nomblr.com',
                             'password1': 'password',
                             'password2': 'password',
                             'invite_code': 'aa073e50954855d0533476ad002cce721d1b830d'})
    assert not form.is_valid()
    assert 'username' in form.errors

def test_SignupForm_invalid_username():
    form = forms.SignupForm({'email': 'test@nomblr.com',
                             'username': 'invalid username',
                             'password1': 'password',
                             'password2': 'password',
                             'invite_code': 'aa073e50954855d0533476ad002cce721d1b830d'})
    assert not form.is_valid()
    assert 'username' in form.errors

def test_SignupForm_long_username():
    form = forms.SignupForm({'email': 'test@nomblr.com',
                             'username': 'test_test_test_test_test_test_test',
                             'password1': 'password',
                             'password2': 'password',
                             'invite_code': 'aa073e50954855d0533476ad002cce721d1b830d'})
    assert not form.is_valid()
    assert 'username' in form.errors

def test_SignupForm_short_username():
    form = forms.SignupForm({'email': 'test@nomblr.com',
                             'username': 't',
                             'password1': 'password',
                             'password2': 'password',
                             'invite_code': 'aa073e50954855d0533476ad002cce721d1b830d'})
    assert not form.is_valid()
    assert 'username' in form.errors

def test_SignupForm_missing_password1():
    form = forms.SignupForm({'email': 'test@nomblr.com',
                             'username': 'test',
                             'password2': 'password',
                             'invite_code': 'aa073e50954855d0533476ad002cce721d1b830d'})
    assert not form.is_valid()
    assert 'password1' in form.errors

def test_SignupForm_missing_password2():
    form = forms.SignupForm({'email': 'test@nomblr.com',
                             'username': 'test',
                             'password1': 'password',
                             'invite_code': 'aa073e50954855d0533476ad002cce721d1b830d'})
    assert not form.is_valid()
    assert 'password2' in form.errors

def test_SignupForm_mismatch_password():
    form = forms.SignupForm({'email': 'test@nomblr.com',
                             'username': 'test',
                             'password1': 'password1',
                             'password2': 'password2',
                             'invite_code': 'aa073e50954855d0533476ad002cce721d1b830d'})
    assert not form.is_valid()
    assert 'password2' in form.errors

def test_SignupForm_missing_invite_code():
    form = forms.SignupForm({'email': 'test@nomblr.com',
                             'username': 'test',
                             'password1': 'password',
                             'password2': 'password'})
    assert not form.is_valid()
    assert 'invite_code' in form.errors

def test_SignupForm_invalid_invite_code():
    form = forms.SignupForm({'email': 'test@nomblr.com',
                             'username': 'test',
                             'password1': 'password',
                             'password2': 'password',
                             'invite_code': 'invalid invite code'})
    assert not form.is_valid()
    assert 'invite_code' in form.errors

def test_FlexibleAuthenticationForm_valid_username():
    form = forms.FlexibleAuthenticationForm(None,
                                            {'username': 'tester',
                                             'password': 'password'})
    assert form.is_valid()

def test_FlexibleAuthenticationForm_valid_email():
    form = forms.FlexibleAuthenticationForm(None,
                                            {'username': 'tester@nomblr.com',
                                             'password': 'password'})
    assert form.is_valid()

def test_FlexibleAuthenticationForm_invalid_username():
    form = forms.FlexibleAuthenticationForm(None,
                                            {'username': 'missing',
                                             'password': 'password'})
    assert not form.is_valid()

def test_FlexibleAuthenticationForm_invalid_email():
    form = forms.FlexibleAuthenticationForm(None,
                                            {'username': 'missing@nomblr.com',
                                             'password': 'password'})
    assert not form.is_valid()

def test_GET_index():
    c = Client()
    c.login(username='tester', password='password')
    response = c.get('/')
    assert 200 == response.status_code

def test_GET_unauth_index():
    c = Client()
    response = c.get('/')
    assert 302 == response.status_code
    assert 'http://testserver/login/?next=/' == response['Location']

def test_GET_search():
    c = Client()
    c.login(username='tester', password='password')
    response = c.get('/', {'q': 'foo'})
    assert 200 == response.status_code
    assert 1 == response.context['results'].paginator.count

def test_GET_other_search():
    c = Client()
    c.login(username='othertester', password='password')
    response = c.get('/', {'q': 'foo'})
    assert 200 == response.status_code
    assert 0 == response.context['results'].paginator.count

def test_GET_empty_search():
    c = Client()
    c.login(username='tester', password='password')
    response = c.get('/', {'q': ''})
    assert 200 == response.status_code

def test_POST_index():
    c = Client()
    c.login(username='tester', password='password')
    response = c.post('/', {'name': 'Another test',
                            'text': 'Test ingredients and directions.'})
    assert 302 == response.status_code
    assert 'http://testserver/tester/another-test/' == response['Location']

def test_POST_invalid_index():
    c = Client()
    c.login(username='tester', password='password')
    response = c.post('/', {})
    assert 400 == response.status_code

def test_GET_signup():
    c = Client()
    response = c.get('/signup/')
    assert 200 == response.status_code

def test_POST_signup():
    c = Client()
    response = c.post('/signup/', {'email': 'test@nomblr.com',
                            'username': 'test',
                            'password1': 'password',
                            'password2': 'password',
                            'invite_code': 'aa073e50954855d0533476ad002cce721d1b830d'})
    assert 302 == response.status_code
    assert 'http://testserver/' == response['Location']

def test_POST_invalid_signup():
    c = Client()
    response = c.post('/signup/', {'email': 'test@nomblr.com',
                            'username': 'test',
                            'password1': 'password1',
                            'password2': 'password2',
                            'invite_code': 'aa073e50954855d0533476ad002cce721d1b830d'})
    assert 200 == response.status_code

def test_GET_logout():
    c = Client()
    c.login(username='tester', password='password')
    response = c.get('/logout/')
    assert 405 == response.status_code

def test_POST_logout():
    c = Client()
    c.login(username='tester', password='password')
    response = c.post('/logout/')
    assert 200 == response.status_code
