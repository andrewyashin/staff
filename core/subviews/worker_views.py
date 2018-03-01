from datetime import datetime, date

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from core.models import PersonCategory, PersonHasPersonCategory, Person, Party, PartyType, OrganizationCategory, \
    OrganizationHasOrganizationCategory, RelationshipType, Relationship, Organization

organization_category = 'Кафедра'
person_category = 'Співробітник'
party_type = 'PERSON'


class WorkerList(TemplateView):
    template_name = 'worker_templates/workers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['worker_list'] = load_workers()
        return context


class EditWorker(TemplateView):
    template_name = 'worker_templates/workerEdit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['id']
        person = Person.objects.get(id=pk)
        context['person'] = person
        context['organization_list'] = load_organization(organization_category)
        context['person_organization_list'] = load_person_organizations(load_organization(organization_category),
                                                                        person)
        context['now_date'] = datetime.now()
        return context


class DeleteWorker(TemplateView):
    template_name = 'worker_templates/workers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        delete_worker(kwargs['id'])
        context['worker_list'] = load_workers()
        return context


class SaveWorker(TemplateView):
    template_name = 'worker_templates/workers.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if kwargs.get('id') is None:
            save_worker(request.POST)
        else:
            update_worker(kwargs['id'], request.POST)
        context['worker_list'] = load_workers()
        return HttpResponseRedirect('/workers')


class CreateWorker(TemplateView):
    template_name = 'worker_templates/workerEdit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization_list'] = load_organization(organization_category)
        return context


class DeleteRelationshipView(TemplateView):
    template_name = 'worker_templates/workerEdit.html'

    def get(self, request, *args, **kwargs):
        delete_relationship(kwargs['id'])
        return HttpResponseRedirect('/workers')


class SaveRelationshipView(TemplateView):
    template_name = 'worker_templates/workerEdit.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        create_relation(request.POST, Person.objects.get(pk=kwargs['id']))
        context['worker_list'] = load_workers()
        return HttpResponseRedirect('/workers')


def load_organization(caption):
    organization_category = OrganizationCategory.objects.get(caption=caption)
    organization_has_organization_category = OrganizationHasOrganizationCategory.objects.filter(
        organizationCategory=organization_category)
    organizations = []
    for organization_id in organization_has_organization_category:
        if organization_id.organization.party.state == 'ACT':
            organizations.append(organization_id.organization)
    return organizations


def load_person_organizations(organization_list, person):
    party_person = person.party
    relationships = Relationship.objects.filter(destParty=party_person)
    person_organizations = []
    for relationship in relationships:
        for organization in organization_list:
            if relationship.srcParty == organization.party:
                person_organizations.append(relationship)

    return person_organizations


def load_workers():
    worker_category = PersonCategory.objects.get(caption=person_category)
    worker_has_worker_category = PersonHasPersonCategory.objects.filter(
        personCategory=worker_category)
    workers = []
    for worker_id in worker_has_worker_category:
        if worker_id.person.party.state == 'ACT':
            workers.append(worker_id.person)
    return workers


def save_worker(data):
    party = create_party()
    worker = create_worker(data, party)
    person_category = create_person_category()
    create_worker_has_person_category(person_category, worker)
    if data.get('organization') != 0:
        create_relation(data, worker)


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


def delete_worker(pk):
    person = Person.objects.get(id=pk)
    party = person.party
    party.state = 'DEL'
    person.endDate = datetime.now()
    party.save()


def delete_relationship(pk):
    relationship = Relationship.objects.get(id=pk)
    relationship.endDate = datetime.now()
    relationship.save()
