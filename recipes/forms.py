from django import forms

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

    def save(self, commit=True):
        recipe = super(RecipeForm, self).save(commit=False)
        recipe.owner = self.user
        if commit:
            recipe.save()
        return recipe
