from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from core.subviews.service.organization_service import *

organization_category_caption = 'Кафедра'
party_type = 'ORGANIZATION'


class OrganizationList(TemplateView):
    template_name = 'organization_templates/organizations.html'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('searchText') is not None:
            context['organization_list'] = load_organization_by_search_text(self.request.GET.get('searchText'),
                                                                            organization_category_caption)
        else:
            context['organization_list'] = load_organization(organization_category_caption)
        return context


class EditOrganization(TemplateView):
    template_name = 'organization_templates/organizationEdit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['id']
        organization = Organization.objects.get(id=pk)
        context['organization'] = organization
        context['worker_list'] = load_workers_per_organization(organization)
        return context


class DeleteOrganization(TemplateView):
    template_name = 'organization_templates/organizations.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        delete_organization(kwargs['id'])
        context['organization_list'] = load_organization(organization_category_caption)
        return context


class SaveOrganization(TemplateView):
    template_name = 'organization_templates/organizations.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if kwargs.get('id') is None:
            save_organization(request.POST)
        else:
            update_organization(kwargs['id'], request.POST)
        context['organization_list'] = load_organization(organization_category_caption)
        return HttpResponseRedirect('/organizations')


class CreateOrganization(TemplateView):
    template_name = 'organization_templates/organizationEdit.html'
