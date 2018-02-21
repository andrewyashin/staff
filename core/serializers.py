from rest_framework import serializers

from core.models import ContactType


class ContactTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactType
        fields = ('id', 'name', 'caption', 'template', 'infoText')
