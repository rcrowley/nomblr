from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

import account.forms

class SignupForm(account.forms.EmailForm, account.forms.UsernameForm):
    """
    Signup, taken mostly from django.contrib.auth.forms.UserCreationForm.
    """
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',
                                widget=forms.PasswordInput)
    invite_code = forms.CharField(label='Invite code')

    class Meta(object):
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('Confirm your password.')
        return password2

    def clean_invite_code(self):
        invite_code = self.cleaned_data['invite_code']
        if invite_code in settings.INVITE_CODES:
            return invite_code
        raise forms.ValidationError('That invite code is no good.')

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class FlexibleAuthenticationForm(AuthenticationForm):
    """
    Allow authentication with a username or an email address.  The stock
    Django implementation only accepts usernames.
    """

    def clean_username(self, *args, **kwargs):
        """
        If the username field actually contains an email address, switch
        it out for the matching username.
        """
        username = self.cleaned_data['username']
        if -1 == username.find('@'):
            return username
        try:
            user = User.objects.get(email=username)
            return user.username
        except User.DoesNotExist:
            raise forms.ValidationError('Please enter a correct username '
                                        'and password. Note that both '
                                        'fields are case-sensitive.')
