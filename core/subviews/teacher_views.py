from datetime import datetime, date

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from core.models import PersonCategory, PersonHasPersonCategory, Person, Party, PartyType

category_caption = 'Викладач'
party_type = 'PERSON'


class TeacherList(TemplateView):
    template_name = 'teacher_templates/teachers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher_list'] = load_teachers()
        return context


class EditTeacher(TemplateView):
    template_name = 'teacher_templates/teacherEdit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['id']
        person = Person.objects.get(id=pk)
        context['person'] = person
        return context


class DeleteTeacher(TemplateView):
    template_name = 'teacher_templates/teachers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        delete_teacher(kwargs['id'])
        context['teacher_list'] = load_teachers()
        return context


class SaveTeacher(TemplateView):
    template_name = 'teacher_templates/teachers.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if kwargs.get('id') is None:
            save_teacher(request.POST)
        else:
            update_teacher(kwargs['id'], request.POST)
        context['teacher_list'] = load_teachers()
        return HttpResponseRedirect('/teachers')


class CreateTeacher(TemplateView):
    template_name = 'teacher_templates/teacherEdit.html'


def load_teachers():
    teacher_category = PersonCategory.objects.get(caption=category_caption)
    teacher_has_teacher_category = PersonHasPersonCategory.objects.filter(
        personCategory=teacher_category)
    teachers = []
    for teacher_id in teacher_has_teacher_category:
        if teacher_id.person.party.state == 'ACT':
            teachers.append(teacher_id.person)
    return teachers


def save_teacher(data):
    party = create_party()
    teacher = create_teacher(data, party)
    person_category = create_person_category()
    create_teacher_has_person_category(person_category, teacher)


def create_party():
    party = Party()
    party.partyType = PartyType.objects.get(name=party_type)
    party.state = 'ACT'
    party.save()
    return party


def create_teacher(data, party):
    teacher = Person()
    teacher.party = party
    teacher.firstName = data.get('firstName')
    teacher.secondName = data.get('secondName')
    teacher.patronymicName = data.get('patronymicName')
    teacher.birthDate = data.get('birthDate')
    teacher.startDate = datetime.now()
    teacher.endDate = date.max
    teacher.gender = data.get('gender')
    teacher.taxCode = data.get('taxCode')
    teacher.infoText = data.get('infoText')
    teacher.save()
    return teacher


def create_person_category():
    person_category = PersonCategory.objects.get(caption=category_caption)
    return person_category


def create_teacher_has_person_category(person_category, teacher):
    teacher_has_person_category = PersonHasPersonCategory()
    teacher_has_person_category.personCategory = person_category
    teacher_has_person_category.person = teacher
    teacher_has_person_category.startDate = datetime.now()
    teacher_has_person_category.endDate = date.max
    teacher_has_person_category.save()


def update_teacher(pk, data):
    teacher = Person.objects.get(id=pk)
    teacher.firstName = data.get('firstName')
    teacher.secondName = data.get('secondName')
    teacher.patronymicName = data.get('patronymicName')
    teacher.birthDate = data.get('birthDate')
    teacher.infoText = data.get('infoText')
    teacher.save()


def delete_teacher(pk):
    person = Person.objects.get(id=pk)
    party = person.party
    party.state = 'DEL'
    person.endDate = datetime.now()
    party.save()
