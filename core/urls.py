from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns

from .views import CreateView

urlpatterns = {
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^contact-type/$', CreateView.as_view(), name='create'),
    url(r'^get-token/', obtain_auth_token),
}

urlpatterns = format_suffix_patterns(urlpatterns)
