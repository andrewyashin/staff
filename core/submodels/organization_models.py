from django.db import models

from core.models import party_models


class OrganizationCategory(models.Model):
    caption = models.CharField(max_length=255)
    infoText = models.CharField(max_length=255, blank=True, null=True)


class Organization(models.Model):
    party = models.ForeignKey(party_models.Party, on_delete=models.CASCADE)
    startDate = models.DateField
    endDate = models.DateField
    name = models.CharField(max_length=255)
    infoText = models.CharField(max_length=255, blank=True, null=True)


class OrganizationHasOrganizationCategory(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    organizationCategory = models.ForeignKey(OrganizationCategory, on_delete=models.CASCADE)
    startDate = models.DateField
    endDate = models.DateField

