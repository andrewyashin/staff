from datetime import date

from django.db import models


class ContactType(models.Model):
    name = models.CharField(max_length=45)
    caption = models.CharField(max_length=128)
    template = models.CharField(max_length=64)
    infoText = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Contact Type'
        verbose_name_plural = 'Contact Types'


class PartyType(models.Model):
    name = models.CharField(max_length=45)
    caption = models.CharField(max_length=60)
    infoText = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{}, {}".format(self.name, self.caption)

    class Meta:
        verbose_name = 'Party Type'
        verbose_name_plural = 'Party Types'


class Party(models.Model):
    STATE_TYPE = (
        ('ACT', 'Active'),
        ('SUS', 'Suspended'),
        ('DEL', 'Deleted')
    )
    partyType = models.ForeignKey(PartyType, on_delete=models.CASCADE)
    state = models.CharField(max_length=5, choices=STATE_TYPE)
    infoText = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{}: {}, {}'.format(self.id, self.partyType.name, self.state)

    class Meta:
        verbose_name = 'Party'
        verbose_name_plural = 'Parties'


class PartyContact(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE, blank=True, null=True)
    contactType = models.ForeignKey(ContactType, on_delete=models.CASCADE)
    contact = models.CharField(max_length=512)
    infoText = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.contact)

    class Meta:
        verbose_name = 'Party Contact'
        verbose_name_plural = 'Party Contacts'


class RelationshipType(models.Model):
    caption = models.CharField(max_length=64)
    srcDef = models.CharField(max_length=45)
    dstDef = models.CharField(max_length=45)
    infoText = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.caption)

    class Meta:
        verbose_name = 'Relationship Type'
        verbose_name_plural = 'Relationship Types'


class Role(models.Model):
    caption = models.CharField(max_length=128)
    roleFlag = models.CharField(max_length=8)
    infoText = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.caption)

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'


class PartyHasRole(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    startDate = models.DateField(max_length=255)
    endDate = models.DateField(max_length=255)
    infoText = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.party.id, self.role.caption)

    class Meta:
        verbose_name = 'Party Has Role'
        verbose_name_plural = 'Party Has Role'


class Relationship(models.Model):
    caption = models.CharField(max_length=64)
    relationshipType = models.ForeignKey(RelationshipType, on_delete=models.CASCADE)
    srcParty = models.ForeignKey(Party, on_delete=models.CASCADE, related_name="srcParty")
    destParty = models.ForeignKey(Party, on_delete=models.CASCADE, related_name="destParty")
    startDate = models.DateField(max_length=255)
    endDate = models.DateField(max_length=255)

    def __str__(self):
        return '{}'.format(self.caption)

    class Meta:
        verbose_name = 'Relationship'
        verbose_name_plural = 'Relationships'

    @property
    def is_max(self):
        return self.endDate == date.max
