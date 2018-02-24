from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from core.submodels.organization_models import *
from core.submodels.party_models import *
from core.submodels.person_models import *


class DBAccess(models.Model):
    login = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    startDate = models.DateField
    endDate = models.DateField


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
