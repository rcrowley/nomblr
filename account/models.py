from django.contrib.auth.models import User
from django.db import IntegrityError, models
from django.db.models.signals import post_save
import hashlib

class Profile(models.Model):
    """
    The user's profile, following the common Django pattern for extending
    django.contrib.auth.models.User.
    """
    user = models.OneToOneField(User, related_name='profile')
    facebook_id = models.CharField(blank=True,
                                   default=None,
                                   max_length=255,
                                   null=True,
                                   unique=True)
    facebook_token = models.CharField(blank=True,
                                      default=None,
                                      max_length=255,
                                      null=True)
    facebook_expiry = models.DateTimeField(blank=True,
                                           default=None,
                                           null=True)

    def __repr__(self):
        return '<Profile: {0}>'.format(self.user)

    def __unicode__(self):
        return '{0} (profile)'.format(self.user)

    def get_absolute_url(self):
        return '/{0}/'.format(self.user)

    def gravatar(self, size):
        return 'http://gravatar.com/avatar/{0}.jpg?size={1}'.format(
            hashlib.md5(self.user.email.strip().lower()).hexdigest(),
            size)
    @property
    def gravatar32(self):
        return self.gravatar(32)
    @property
    def gravatar64(self):
        return self.gravatar(64)

def create_profile(sender, instance, created, **kwargs):
    try:
        Profile(user=instance).save()
    except IntegrityError:
        pass
post_save.connect(create_profile, sender=User)
