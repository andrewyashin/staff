from django.views.generic import TemplateView

from core.models import Organization, PersonCategory, PersonHasPersonCategory, Person


class OrganizationList(TemplateView):
    template_name = 'organizations.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org_list'] = Organization.objects.all()
        return context


class TeacherList(TemplateView):
    template_name = 'teachers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacherCategory = PersonCategory.objects.get(caption='Teacher')
        teacherHasTeacherCategory = PersonHasPersonCategory.objects.filter(
            personCategory=teacherCategory)
        teachers = []
        for teacherId in teacherHasTeacherCategory:
            teachers.append(teacherId.person)

        context['teacher_list'] = teachers
        return context
