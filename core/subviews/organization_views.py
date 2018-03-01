from datetime import datetime, date
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from core.models import Organization, OrganizationCategory, OrganizationHasOrganizationCategory, Party, PartyType

organization_category_caption = 'Кафедра'
party_type = 'ORGANIZATION'


class OrganizationList(TemplateView):
    template_name = 'organization_templates/organizations.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization_list'] = load_organization(organization_category_caption)
        return context


class EditOrganization(TemplateView):
    template_name = 'organization_templates/organizationEdit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['id']
        person = Organization.objects.get(id=pk)
        context['organization'] = person
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


def load_organization(caption):
    organization_category = OrganizationCategory.objects.get(caption=caption)
    organization_has_organization_category = OrganizationHasOrganizationCategory.objects.filter(
        organizationCategory=organization_category)
    organizations = []
    for organization_id in organization_has_organization_category:
        if organization_id.organization.party.state == 'ACT':
            organizations.append(organization_id.organization)
    return organizations


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


def update_organization(pk, data):
    organization = Organization.objects.get(id=pk)
    organization.name = data.get('name')
    organization.infoText = data.get('infoText')
    organization.save()


def delete_organization(pk):
    organization = Organization.objects.get(id=pk)
    party = organization.party
    party.state = 'DEL'
    organization.endDate = datetime.now()
    party.save()
