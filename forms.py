from django import forms
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

    class Meta(object):
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('Confirm your password.')
        return password2

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
