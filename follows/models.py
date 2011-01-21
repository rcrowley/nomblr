from django.contrib.auth.models import User
from django.db import models

class FollowManager(models.Manager):
    """
    A custom manager that implements __contains__.
    """

    def __contains__(self, user):
        try:
            follow = self.get(followee=user)
            return True
        except Follow.DoesNotExist:
            return False

class Follow(models.Model):
    """
    A one-way relationship between two users.
    """
    follower = models.ForeignKey(User, related_name='following')
    followee = models.ForeignKey(User, related_name='followers', db_index=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = FollowManager()

    class Meta(object):
        unique_together = (('follower', 'followee'),)
