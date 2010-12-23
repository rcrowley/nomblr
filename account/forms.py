from django import forms
from django.contrib.auth.models import User

class EmailForm(forms.ModelForm):
    email = forms.EmailField(label='Email')

    class Meta(object):
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('{0} already exists.'.format(email))

    def save(self, commit=True):
        user = super(EmailForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class UsernameForm(forms.ModelForm):
    username = forms.RegexField(label='Username',
                                max_length=30,
                                regex=r'^[\w.-]{2,30}$',
                                error_messages={'invalid': 'Required.  2 to 30 letters, numbers, periods, and dashes.'})

    class Meta(object):
        model = User
        fields = ('username',)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('{0} already exists.'.format(username))

    def save(self, commit=True):
        user = super(UsernameForm, self).save(commit=False)
        if commit:
            user.save()
        return user
