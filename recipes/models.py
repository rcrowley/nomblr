from django.db import models

class Recipe(object):
    # FIXME Fields.

    def __unicode__(self):
        return self.slug # FIXME

    def get_absolute_url(self):
        return '/{username}/{slug}/'.format(**self.__dict__)

setattr(Recipe, 'objects', Manager(Recipe))
