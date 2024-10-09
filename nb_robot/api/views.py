from netbox.api.viewsets import NetBoxModelViewSet

from .. import models
from . import serializers

# Project ViewSets

class ProjectViewSet(NetBoxModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer

# Resource ViewSets
class ResourceViewSet(NetBoxModelViewSet):
    queryset = models.Resource.objects.all()
    serializer_class = serializers.ResourceSerializer


# Variable ViewSets
class VariableViewSet(NetBoxModelViewSet):
    queryset = models.Variable.objects.all()
    serializer_class = serializers.VariableSerializer