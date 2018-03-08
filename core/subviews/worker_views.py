from django.shortcuts import redirect
from django.views.generic import TemplateView

from core.subviews.service.workers_service import *

organization_category = 'Кафедра'
person_category = 'Співробітник'
party_type = 'PERSON'


class WorkerList(TemplateView):
    template_name = 'worker_templates/workers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('searchText') is not None:
            context['worker_list'] = load_workers_per_search_text(self.request.GET.get('searchText'))
        else:
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
        context['organization_relationship'] = load_person_organizations(load_all_organization(organization_category),
                                                                        person)
        context['contacts'] = load_contact_information(person)
        context['contact_types'] = load_contact_types()
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
            person_id = save_worker(request.POST).id
        else:
            update_worker(kwargs['id'], request.POST)
            person_id = kwargs['id']
        context['worker_list'] = load_workers()
        return redirect('/worker/edit/' + str(person_id))


class CreateWorker(TemplateView):
    template_name = 'worker_templates/workerEdit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization_list'] = load_organization(organization_category)
        return context


class DeleteRelationshipView(TemplateView):
    template_name = 'worker_templates/workerEdit.html'

    def get(self, request, *args, **kwargs):
        person = delete_relationship(kwargs['id'])
        return redirect('/worker/edit/' + str(person.id))


class SaveRelationshipView(TemplateView):
    template_name = 'worker_templates/workerEdit.html'

    def post(self, request, *args, **kwargs):
        create_relation(request.POST, Person.objects.get(pk=kwargs['id']))
        return redirect('/worker/edit/' + str(kwargs['id']))


class SaveContactInfoView(TemplateView):
    template_name = 'worker_templates/workerEdit.html'

    def post(self, request, *args, **kwargs):
        create_contact_info(request.POST, Person.objects.get(pk=kwargs['id']))
        return redirect('/worker/edit/' + str(kwargs['id']))


class SaveContactTypeView(TemplateView):
    template_name = 'worker_templates/workerEdit.html'

    def post(self, request, *args, **kwargs):
        create_contact_type(request.POST)
        return redirect('/worker/edit/' + str(kwargs['id']))


class DeleteContactTypeView(TemplateView):
    template_name = 'worker_templates/workerEdit.html'

    def get(self, request, *args, **kwargs):
        person = delete_contact(kwargs['id'])
        return redirect('/worker/edit/' + str(person.id))
