from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
# from django.db import models
from django.db.models.manager import ManagerDescriptor
from django.db.models.manager import ManagerDescriptor
import os

class Manager(object):
    """
    A fake manager for a fake model.
    """

    def __init__(self, model):
        self.model = model

    def all(self):
        return self.filter()

    def filter(self, username=None, slug=None):
        if username is None:
            usernames = os.listdir(settings.RECIPES_ROOT) # FIXME Generator
        else:
            usernames = [username]
        if slug is None:
            for username in usernames:
                for slug in os.listdir(os.path.join(settings.RECIPES_ROOT,
                                                    username)): # FIXME
                    yield self.model(username, slug)
        else:
            for username in usernames:
                if os.path.exists(os.path.join(settings.RECIPES_ROOT,
                                               username)):
                    yield self.model(username, slug)

    def get(self, username, slug):
        if os.path.exists(os.path.join(settings.RECIPES_ROOT, username)):
            return self.model(username=username, slug=slug)
        raise ObjectDoesNotExist()

    def search(self):
        pass

class Recipe(object):
    """
    A fake model that uses the filesystem to store recipes.
    """

    def __init__(self, username, slug):
        self.username = username
        self.slug = slug

    def __unicode__(self):
        return self.slug # FIXME

    def get_absolute_url(self):
        return '/recipes/{username}/{slug}/'.format(**self.__dict__)

setattr(Recipe, 'objects', Manager(Recipe))
