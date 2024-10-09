from django.db.models import Q
from utilities.choices import ChoiceSet
from django.utils.translation import gettext_lazy as _



class ResourceTypesChoices(ChoiceSet):

    RESOURCE_TYPE_1 = "TestSuite"
    RESOURCE_TYPE_2 = "Variables"
    RESOURCE_TYPE_3 = "CustomLibrary"
    RESOURCE_TYPE_4 = "Keywords"

    CHOICES = (
        (RESOURCE_TYPE_1, "Test Suite"),
        (RESOURCE_TYPE_2, "Variables"),
        (RESOURCE_TYPE_3, "Custom Library"),
        (RESOURCE_TYPE_4, "Keywords"),
    )

class VariableTypeChoices(ChoiceSet):

    TYPE_GENERIC = "generic"
    TYPE_FILTER = 'savedfilter'
    TYPE_QUERYSET = 'queryset'

    CHOICES = (
        (TYPE_GENERIC, _('Generic')),
        (TYPE_FILTER, _('Saved Filter')),
        (TYPE_QUERYSET, _('QuerySet'))
    )