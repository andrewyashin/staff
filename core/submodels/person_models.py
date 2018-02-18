from django.db import models

from core.submodels.party_models import Party


class Person(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    startDate = models.DateField(max_length=100)
    endDate = models.DateField(max_length=100)
    firstName = models.CharField(max_length=45)
    secondName = models.CharField(max_length=45)
    patronymicName = models.CharField(max_length=45)
    birthDate = models.DateField(max_length=255)
    gender = models.CharField(max_length=20, choices=GENDER)
    taxCode = models.CharField(max_length=18)
    infoText = models.CharField(max_length=255, blank=True, null=True)


class PassportType(models.Model):
    caption = models.CharField(max_length=45)
    infoText = models.CharField(max_length=255, null=True, blank=True)


class Passport(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    passportType = models.ForeignKey(PassportType, on_delete=models.CASCADE)
    startDate = models.DateField
    endDate = models.DateField
    serialNumber = models.CharField(max_length=16)
    name = models.CharField(max_length=128)
    issueDate = models.DateField
    expirationDate = models.DateField
    issueAuth = models.CharField(max_length=255)
    infoText = models.CharField(max_length=255, null=True, blank=True)


class PersonCategory(models.Model):
    caption = models.CharField(max_length=128)
    infoText = models.CharField(max_length=255, null=True, blank=True)


class PersonHasPersonCategory(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    personCategory = models.ForeignKey(PersonCategory, on_delete=models.CASCADE)
    startDate = models.DateField
    endDate = models.DateField
    infoText = models.CharField(max_length=255, null=True, blank=True)
