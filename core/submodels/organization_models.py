from django.db import models

from core.submodels.party_models import Party


class OrganizationCategory(models.Model):
    caption = models.CharField(max_length=255)
    infoText = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.caption)

    class Meta:
        verbose_name = 'Organization Category'
        verbose_name_plural = 'Organization Categories'


class Organization(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    startDate = models.DateField
    endDate = models.DateField
    name = models.CharField(max_length=255)
    infoText = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'


class OrganizationHasOrganizationCategory(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    organizationCategory = models.ForeignKey(OrganizationCategory, on_delete=models.CASCADE)
    startDate = models.DateField
    endDate = models.DateField

    def __str__(self):
        return '{} - {}'.format(self.organization.name, self.organizationCategory.caption)

    class Meta:
        verbose_name = 'Organization Has Organization Category'
        verbose_name_plural = 'Organization Has Organization Category'
