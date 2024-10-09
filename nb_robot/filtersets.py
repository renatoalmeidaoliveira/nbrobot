from netbox.filtersets import NetBoxModelFilterSet
from django.db.models import Q
import django_filters
from . import models

# Project Filters

class ProjectFilterSet(NetBoxModelFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )

    class Meta:
        model = models.Project
        fields = ["name", "description", "id", "slug"]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
            | Q(description__icontains=value)
        )

# Resource Filters
class ResourceFilterSet(NetBoxModelFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )

    class Meta:
        model = models.Resource
        fields = ["name", "resource_type", "project", "id"]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
            | Q(resource_type__icontains=value)
            | Q(status__icontains=value)
        )

# Variable Filters

class VariableFilterSet(NetBoxModelFilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )

    class Meta:
        model = models.Variable
        fields = ["name", "type", "project"]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
            | Q(type__icontains=value)
            | Q(project__name__icontains=value)
        )