from datetime import datetime, date

from django.db import transaction

from core.models import Organization, OrganizationCategory, OrganizationHasOrganizationCategory, Party, PartyType, \
    Relationship, Person

organization_category_caption = 'Кафедра'
party_type = 'ORGANIZATION'


def load_organization(caption):
    organization_category = OrganizationCategory.objects.get(caption=caption)
    organization_has_organization_category = OrganizationHasOrganizationCategory.objects.filter(
        organizationCategory=organization_category)
    organizations = []
    for organization_id in organization_has_organization_category:
        if organization_id.organization.party.state == 'ACT':
            organizations.append(organization_id.organization)
    return organizations


def load_organization_by_search_text(search_text, caption):
    organization_category = OrganizationCategory.objects.get(caption=caption)
    organization_has_organization_category = OrganizationHasOrganizationCategory.objects.filter(
        organizationCategory=organization_category)
    organizations = []
    for organization_id in organization_has_organization_category:
        if organization_id.organization.party.state == 'ACT':
            if str(search_text).lower() in organization_id.organization.name.lower():
                organizations.append(organization_id.organization)
    return organizations


@transaction.atomic
def save_organization(data):
    party = create_party()
    organization = create_organization(data, party)
    organization_category = get_organization_category()
    create_organization_has_organization_category(organization_category, organization)


def create_party():
    party = Party()
    party.partyType = PartyType.objects.get(name=party_type)
    party.state = 'ACT'
    party.save()
    return party


def create_organization(data, party):
    organization = Organization()
    organization.party = party
    organization.startDate = date.today()
    organization.endDate = date.max
    organization.name = data.get('name')
    organization.infoText = data.get('infoText')
    organization.save()
    return organization


def get_organization_category():
    organization_category = OrganizationCategory.objects.get(caption=organization_category_caption)
    return organization_category


def create_organization_has_organization_category(organization_category, organization):
    organization_has_organization_category = OrganizationHasOrganizationCategory()
    organization_has_organization_category.organizationCategory = organization_category
    organization_has_organization_category.organization = organization
    organization_has_organization_category.startDate = datetime.now()
    organization_has_organization_category.endDate = date.max
    organization_has_organization_category.save()
    return organization_has_organization_category


@transaction.atomic
def update_organization(pk, data):
    organization = Organization.objects.get(id=pk)
    organization.name = data.get('name')
    organization.infoText = data.get('infoText')
    organization.save()


@transaction.atomic
def delete_organization(pk):
    organization = Organization.objects.get(id=pk)
    party = organization.party
    party.state = 'DEL'
    organization.endDate = datetime.now()
    party.save()

    Relationship.objects.filter(srcParty=party).update(endDate=datetime.now())


def load_workers_per_organization(organization):
    party_organization = organization.party
    workers_parties = Relationship.objects.filter(srcParty=party_organization)
    workers = []
    for workers_party in workers_parties:
        person = Person.objects.get(party=workers_party.destParty)
        if person not in workers:
            if person.party.state == 'ACT':
                workers.append(person)
    return workers
