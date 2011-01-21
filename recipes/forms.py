from django import forms
from django.conf import settings

import models

class RecipeForm(forms.ModelForm):
    name = forms.CharField(label='Name', max_length=255)
    text = forms.CharField(label='Recipe', widget=forms.Textarea)

    class Meta(object):
        model = models.Recipe
        fields = ('name', 'text')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(RecipeForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        if name in settings.RECIPE_BLACKLIST:
            raise forms.ValidationError('That recipe name is not allowed.')
        return name

    def save(self, commit=True):
        recipe = super(RecipeForm, self).save(commit=False)
        recipe.owner = self.user
        if commit:
            recipe.save()
        return recipe
