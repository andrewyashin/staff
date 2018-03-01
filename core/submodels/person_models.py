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
    infoText = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.firstName, self.secondName, self.patronymicName)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'


class PassportType(models.Model):
    caption = models.CharField(max_length=45)
    infoText = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.caption)

    class Meta:
        verbose_name = 'Passport Type'
        verbose_name_plural = 'Passport Types'


class Passport(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    passportType = models.ForeignKey(PassportType, on_delete=models.CASCADE)
    startDate = models.DateField(max_length=255)
    endDate = models.DateField(max_length=255)
    serialNumber = models.CharField(max_length=16)
    name = models.CharField(max_length=128)
    issueDate = models.DateField(max_length=255)
    expirationDate = models.DateField(max_length=255)
    issueAuth = models.CharField(max_length=255)
    infoText = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return 'Passport: {} {} {}'.format(self.person.firstName, self.person.secondName, self.person.patronymicName)

    class Meta:
        verbose_name = 'Passport'
        verbose_name_plural = 'Passports'


class PersonCategory(models.Model):
    caption = models.CharField(max_length=128)
    infoText = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.caption)

    class Meta:
        verbose_name = 'Person Category'
        verbose_name_plural = 'Person Categories'


class PersonHasPersonCategory(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    personCategory = models.ForeignKey(PersonCategory, on_delete=models.CASCADE)
    startDate = models.DateField(max_length=255)
    endDate = models.DateField(max_length=255)
    infoText = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.person.secondName, self.personCategory.caption)

    class Meta:
        verbose_name = 'Person Has Person Category'
        verbose_name_plural = 'Person Has Person Category'
