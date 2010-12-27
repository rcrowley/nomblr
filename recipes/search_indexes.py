import datetime
from haystack import indexes
from haystack import site

import models

class RecipeIndex(indexes.RealTimeSearchIndex):
    owner = indexes.CharField(model_attr='owner')
    gravatar32 = indexes.CharField(model_attr='owner__profile__gravatar32',
                                   indexed=False)
    slug = indexes.CharField(model_attr='slug', indexed=False)
    name = indexes.CharField(model_attr='name')
    text = indexes.CharField(document=True, use_template=True)

    def get_queryset(self):
        return models.Recipe.objects.all()

site.register(models.Recipe, RecipeIndex)
