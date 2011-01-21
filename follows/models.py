from django.contrib.auth.models import User
from django.db import models

class Follow(models.Model):
    """
    A one-way relationship between two users.
    """
    follower = models.ForeignKey(User, related_name='following')
    followee = models.ForeignKey(User, related_name='followers', db_index=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        unique_together = (('follower', 'followee'),)
