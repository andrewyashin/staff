from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from .views import OrganizationList, TeacherList

urlpatterns = {
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'', OrganizationList.as_view(), name='Organizations'),
    url(r'^organizations/', OrganizationList.as_view(), name='Organizations'),
    url(r'^teachers/', TeacherList.as_view(), name='Teachers'),
}

urlpatterns = format_suffix_patterns(urlpatterns)
