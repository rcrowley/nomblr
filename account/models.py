from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
import hashlib

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

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
    if created:
        Profile(user=instance).save()
post_save.connect(create_profile, sender=User)
