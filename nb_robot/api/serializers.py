from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from netbox.api.fields import ChoiceField, ContentTypeField, SerializedPKRelatedField
from utilities.api import get_serializer_for_model


from netbox.api.serializers import NetBoxModelSerializer

from .. import models


# Project Serializers

class ProjectSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.Project
        fields = ['id', 'name', 'description', 'created', 'last_updated', 'slug']

# Resource Serializers
class ResourceSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.Resource
        fields = ['id', 'name', 'project', 'resource_type']

# Variable Serializers

class VariableSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.Variable
        fields = ['id', 'name', 'type', 'project', 'value', 'related_object_type']