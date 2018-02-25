from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from core.subviews.organization_views import OrganizationList, EditOrganization, DeleteOrganization, SaveOrganization, \
    CreateOrganization
from core.subviews.teacher_views import EditTeacher, DeleteTeacher, SaveTeacher, CreateTeacher, TeacherList

urlpatterns = {
    path('', OrganizationList.as_view(), name='Organizations'),
    path('organization/edit/<int:id>', EditOrganization.as_view(), name='EditOrganization'),

    path('organization/delete/<int:id>', DeleteOrganization.as_view(), name='DeleteOrganization'),
    path('organization/save/<int:id>', SaveOrganization.as_view(), name='SaveOrganization'),
    path('organization/save/', SaveOrganization.as_view(), name='SaveOrganization'),
    path('organization/add', CreateOrganization.as_view(), name='CreateOrganization'),
    path('organizations/', OrganizationList.as_view(), name='Organizations'),

    path('teacher/edit/<int:id>', EditTeacher.as_view(), name='EditTeacher'),
    path('teacher/delete/<int:id>', DeleteTeacher.as_view(), name='EditTeacher'),
    path('teacher/save/<int:id>', SaveTeacher.as_view(), name='SaveTeacher'),
    path('teacher/save/', SaveTeacher.as_view(), name='SaveTeacher'),
    path('teacher/add', CreateTeacher.as_view(), name='UpdateTeacher'),
    path('teachers/', TeacherList.as_view(), name='Teachers'),
}

urlpatterns = format_suffix_patterns(urlpatterns)
