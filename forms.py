from django import forms
from django.contrib.auth.models import User

class Search(forms.Form):
    q = forms.CharField(label='Search')

class Signup(forms.ModelForm):
    """
    Signup, taken mostly from django.contrib.auth.forms.UserCreationForm.
    """

    class Meta(object):
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    email = forms.EmailField(label='Email')
    username = forms.RegexField(label='Username',
                                max_length=30,
                                regex=r'^[\w.-]{2,30}$',
                                error_messages={'invalid': 'Required.  2 to 30 letters, numbers, periods, and dashes.'})
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',
                                widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('{0} already exists.'.format(email))

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('{0} already exists.'.format(username))

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('Confirm your password.')
        return password2

    def save(self, commit=True):
        user = super(Signup, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
