from datetime import datetime, date

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from core.models import PersonCategory, PersonHasPersonCategory, Person, Party, PartyType

category_caption = 'Співробітник'
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


def load_workers():
    worker_category = PersonCategory.objects.get(caption=category_caption)
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
    worker.taxCode = data.get('taxCode')
    worker.infoText = data.get('infoText')
    worker.save()
    return worker


def create_person_category():
    person_category = PersonCategory.objects.get(caption=category_caption)
    return person_category


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
    worker.infoText = data.get('infoText')
    worker.save()


def delete_worker(pk):
    person = Person.objects.get(id=pk)
    party = person.party
    party.state = 'DEL'
    person.endDate = datetime.now()
    party.save()
