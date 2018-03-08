from datetime import datetime, date

from django.db import transaction

from core.models import PersonCategory, PersonHasPersonCategory, Person, Party, PartyType, OrganizationCategory, \
    OrganizationHasOrganizationCategory, RelationshipType, Relationship, Organization, PartyContact, ContactType

organization_category = 'Кафедра'
person_category = 'Співробітник'
party_type = 'PERSON'


def load_organization(caption):
    organization_category = OrganizationCategory.objects.get(caption=caption)
    organization_has_organization_category = OrganizationHasOrganizationCategory.objects.filter(
        organizationCategory=organization_category)
    organizations = []
    for organization_id in organization_has_organization_category:
        if organization_id.organization.party.state == 'ACT':
            organizations.append(organization_id.organization)
    return organizations


def load_all_organization(caption):
    organization_category = OrganizationCategory.objects.get(caption=caption)
    organization_has_organization_category = OrganizationHasOrganizationCategory.objects.filter(
        organizationCategory=organization_category)
    organizations = []
    for organization_id in organization_has_organization_category:
        organizations.append(organization_id.organization)
    return organizations


def load_person_organizations(organization_list, person):
    party_person = person.party
    relationships = Relationship.objects.filter(destParty=party_person)
    organization_relationship = []
    for relationship in relationships:
        for organization in organization_list:
            if relationship.srcParty == organization.party:
                relationship_organization = RelationshipOrganization()
                relationship_organization.relationship = relationship
                relationship_organization.organization = organization
                organization_relationship.append(relationship_organization)

    return organization_relationship


def load_workers():
    worker_category = PersonCategory.objects.get(caption=person_category)
    worker_has_worker_category = PersonHasPersonCategory.objects.filter(
        personCategory=worker_category)
    workers = []
    for worker_id in worker_has_worker_category:
        if worker_id.person.party.state == 'ACT':
            workers.append(worker_id.person)
    return workers


def load_workers_per_search_text(search_text):
    workers = load_workers()
    search_text_workers = []
    for worker in workers:
        if str(search_text).lower() in str(worker.firstName).lower() or str(search_text).lower() in str(
                worker.secondName).lower() or str(search_text).lower() in str(worker.patronymicName).lower():
            search_text_workers.append(worker)
    return search_text_workers


@transaction.atomic
def save_worker(data):
    party = create_party()
    worker = create_worker(data, party)
    person_category = create_person_category()
    create_worker_has_person_category(person_category, worker)
    return worker


def create_relation(data, worker):
    relationship_type = get_or_create_relationship_type()
    create_relationship(relationship_type, data, worker)


def create_relationship(relationship_type, data, worker):
    relationship = Relationship()
    relationship.caption = data.get('caption')
    relationship.relationshipType = relationship_type
    relationship.srcParty = Organization.objects.get(pk=data['organization']).party
    relationship.destParty = worker.party
    relationship.startDate = datetime.now()
    relationship.endDate = date.max
    relationship.save()


def get_or_create_relationship_type():
    if not RelationshipType.objects.filter(caption=person_category).exists():
        relationship_type = RelationshipType()
        relationship_type.caption = person_category
        relationship_type.srcDef = organization_category
        relationship_type.dstDef = person_category
        relationship_type.save()

    return RelationshipType.objects.get(caption=person_category)


def create_party():
    party = Party()
    party.partyType = PartyType.objects.get(name=party_type)
    party.state = 'ACT'
    party.save()
    return party


def create_worker(data, party):
    worker = Person()
    worker.party = party
    worker.firstName = data.get('firstName')
    worker.secondName = data.get('secondName')
    worker.patronymicName = data.get('patronymicName')
    worker.birthDate = data.get('birthDate')
    worker.startDate = datetime.now()
    worker.endDate = date.max
    worker.gender = data.get('gender')
    worker.infoText = data.get('infoText')
    worker.save()
    return worker


def create_person_category():
    person__category = PersonCategory.objects.get(caption=person_category)
    return person__category


def create_worker_has_person_category(person_category, worker):
    worker_has_person_category = PersonHasPersonCategory()
    worker_has_person_category.personCategory = person_category
    worker_has_person_category.person = worker
    worker_has_person_category.startDate = datetime.now()
    worker_has_person_category.endDate = date.max
    worker_has_person_category.save()


def update_worker(pk, data):
    worker = Person.objects.get(id=pk)
    worker.firstName = data.get('firstName')
    worker.secondName = data.get('secondName')
    worker.patronymicName = data.get('patronymicName')
    worker.birthDate = data.get('birthDate')
    worker.gender = data.get('gender')
    worker.infoText = data.get('infoText')
    worker.save()


@transaction.atomic
def delete_worker(pk):
    person = Person.objects.get(id=pk)
    party = person.party
    party.state = 'DEL'
    person.endDate = datetime.now()
    party.save()

    Relationship.objects.filter(destParty=party).update(endDate=datetime.now())


@transaction.atomic
def delete_relationship(pk):
    relationship = Relationship.objects.get(id=pk)
    relationship.endDate = datetime.now()
    relationship.save()
    return Person.objects.get(party=relationship.destParty)


def load_contact_information(person):
    party = person.party
    return PartyContact.objects.filter(party=party)


def load_contact_types():
    return ContactType.objects.all()


@transaction.atomic
def create_contact_info(data, person):
    contact_type_id = data.get('contact_types')
    contact_type = ContactType.objects.get(pk=contact_type_id)
    contact = PartyContact()
    contact.party = person.party
    contact.contact = data.get('contact')
    contact.contactType = contact_type
    contact.save()


@transaction.atomic
def create_contact_type(data):
    contact_type = ContactType()
    contact_type.name = data.get('name')
    contact_type.template = data.get('template')
    contact_type.save()


@transaction.atomic
def delete_contact(contact_id):
    party = PartyContact.objects.get(pk=contact_id).party
    PartyContact.objects.get(pk=contact_id).delete()
    return Person.objects.get(party=party)


class RelationshipOrganization:
    organization = Organization()
    relationship = Relationship()
