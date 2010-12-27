from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

class Recipe(models.Model):
    """
    A single recipe, known on the site as a "nom."
    """
    owner = models.ForeignKey(User, related_name='recipes')
    slug = models.SlugField(max_length=255, db_index=False)
    name = models.CharField(max_length=255)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        unique_together = (('owner', 'slug'),)

    def __repr__(self):
        return '<Recipe: {0}>'.format(self.slug)

    def __unicode__(self):
        return unicode(self.name)

    def get_absolute_url(self):
        return '/{0}/{1}/'.format(self.owner, self.slug)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Recipe, self).save(*args, **kwargs)
