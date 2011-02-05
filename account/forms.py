from datetime import datetime
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.template import Context, loader
import hashlib
import hmac

# This line causes IntegrityError to be raised in `models.create_profile`,
# which is called via a signal.
import models

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
        """
        Send an email address confirmation, too.
        """
        user = super(EmailForm, self).save(commit=False)
        t = loader.get_template('email_confirmation.txt')
        from django.core.mail import send_mail
        send_mail('Confirm your email address on Nomblr',
                  t.render(Context({'email': user.email,
                                    'user': user,
                                    'token': hmac.new(
                                        settings.SECRET_KEY,
                                        user.email,
                                        hashlib.sha1).hexdigest()})),
                  settings.DEFAULT_FROM_EMAIL,
                  [user.email])
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
        if username in settings.USERNAME_BLACKLIST:
            raise forms.ValidationError('That username is not allowed.')
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

class FacebookSessionForm(forms.ModelForm):
    facebook_id = forms.CharField(max_length=255)
    facebook_token = forms.CharField(max_length=255)
    facebook_expiry = forms.IntegerField()

    class Meta(object):
        model = models.Profile
        fields = ('facebook_id', 'facebook_token', 'facebook_expiry')

    def clean_facebook_expiry(self):
        expiry = self.cleaned_data['facebook_expiry']
        try:
            return datetime.fromtimestamp(expiry)
        except ValueError:
            raise forms.ValidationError('{0} not a timestamp.'.format(expiry))

    def save(self, commit=True):
        profile = super(FacebookSessionForm, self).save(commit=False)
        if commit:
            profile.save()
        return profile
