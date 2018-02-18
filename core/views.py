from rest_framework import generics
from rest_framework import permissions

from .models import ContactType
from .serializers import ContactTypeSerializer
from .permissions import IsOwner


# Create your views here.
class CreateView(generics.ListCreateAPIView):
    queryset = ContactType.objects.all()
    serializer_class = ContactTypeSerializer
    permission_classes = (
        permissions.IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
