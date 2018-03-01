from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from core.subviews.organization_views import OrganizationList, EditOrganization, DeleteOrganization, SaveOrganization, \
    CreateOrganization
from core.subviews.worker_views import EditWorker, DeleteWorker, SaveWorker, CreateWorker, WorkerList, \
    DeleteRelationshipView, SaveRelationshipView

urlpatterns = {
    path('', OrganizationList.as_view(), name='Organizations'),
    path('organization/edit/<int:id>', EditOrganization.as_view(), name='EditOrganization'),

    path('organization/delete/<int:id>', DeleteOrganization.as_view(), name='DeleteOrganization'),
    path('organization/save/<int:id>', SaveOrganization.as_view(), name='SaveOrganization'),
    path('organization/save/', SaveOrganization.as_view(), name='SaveOrganization'),
    path('organization/add', CreateOrganization.as_view(), name='CreateOrganization'),
    path('organizations/', OrganizationList.as_view(), name='Organizations'),

    path('worker/edit/<int:id>', EditWorker.as_view(), name='EditWorker'),
    path('worker/relationship/delete/<int:id>', DeleteRelationshipView.as_view(), name='DeleteRelationshipView'),
    path('worker/relationship/save/<int:id>', SaveRelationshipView.as_view(), name='SaveRelationshipView'),
    path('worker/delete/<int:id>', DeleteWorker.as_view(), name='EditWorker'),
    path('worker/save/<int:id>', SaveWorker.as_view(), name='SaveWorker'),
    path('worker/save/', SaveWorker.as_view(), name='SaveWorker'),
    path('worker/add', CreateWorker.as_view(), name='UpdateWorker'),
    path('workers/', WorkerList.as_view(), name='Workers'),
}

urlpatterns = format_suffix_patterns(urlpatterns)
