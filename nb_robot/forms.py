import os
import json
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from netbox.forms import (
    NetBoxModelForm,
    NetBoxModelFilterSetForm,
    NetBoxModelBulkEditForm,
    NetBoxModelImportForm,
)
from core.models import ObjectType
from core.forms.mixins import SyncedDataMixin
from ipam.models import IPAddress
from dcim.models import Device, DeviceType
from extras.models import SavedFilter
from utilities.forms.fields import (
    DynamicModelMultipleChoiceField,
    ContentTypeChoiceField,
    SlugField,
    DynamicModelChoiceField,
    CSVModelMultipleChoiceField,
    CSVModelChoiceField,
    CSVContentTypeField,
)
from utilities.forms.rendering import FieldSet
from utilities.forms import add_blank_choice, get_field_value


from . import models, choices


# Project Forms

class ProjectForm(NetBoxModelForm):
    slug = SlugField()
    class Meta:
        model = models.Project
        fields = ['name', 'slug', 'description', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['slug'].disabled = True

class ProjectFilterForm(NetBoxModelFilterSetForm):
    model = models.Project
    q = forms.CharField(
        required=False,
        label='Search'
    )

class ProjectBulkImportForm(NetBoxModelImportForm):
    
    class Meta:
        model = models.Project
        fields = ['name', 'slug', 'description', ]

# Resource Forms

class ResourceForm(SyncedDataMixin, NetBoxModelForm):
    upload_file = forms.FileField(
        required=False
    )

    fieldsets = (
        FieldSet('resource', 'project', 'resource_type', 'description', name=_('Resource')),
        FieldSet('upload_file', name=_('File Upload')),
        FieldSet('data_source', 'data_file', 'auto_sync_enabled', name=_('Data Source')),
    )

    def clean(self):
        cleaned_data = super().clean()

        if self.cleaned_data.get('upload_file') and self.cleaned_data.get('data_file'):
            raise forms.ValidationError(_("Cannot upload a file and sync from an existing file"))
        if not self.cleaned_data.get('upload_file') and not self.cleaned_data.get('data_file'):
            raise forms.ValidationError(_("Must upload a file or select a data file to sync"))

        if self.cleaned_data['upload_file']:
            self.cleaned_data['name'] = self.cleaned_data['upload_file'].name
        return self.cleaned_data
    
    def save(self, *args, **kwargs):
        # If a file was uploaded, save it to disk
        if self.cleaned_data['upload_file']:
            full_path = f"{self.instance.full_path}"
            if os.path.isfile(full_path):
                raise forms.ValidationError(f"File {full_path} already exists")
            with open(full_path, 'wb+') as new_file:
                new_file.write(self.cleaned_data['upload_file'].read())

        return super().save(*args, **kwargs)

    class Meta:
        model = models.Resource
        fields = [ 'project', 'resource_type', 'description', 'data_source', 'data_file', 'auto_sync_enabled' ]

class ResourceFilterForm(NetBoxModelFilterSetForm):
    model = models.Resource
    q = forms.CharField(
        required=False,
        label='Search'
    )

# Variable Forms

class VariableFilterForm(NetBoxModelFilterSetForm):
    model = models.Variable
    q = forms.CharField(
        required=False,
        label='Search'
    )

class VariableForm(NetBoxModelForm):

    related_object_type = ContentTypeChoiceField(
        label=_('Related object type'),
        queryset=ObjectType.objects.public(),
        help_text=_("Type of the related object")
    )

    query_str = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label=_('Variable Data'),
        help_text=_("Value of the variable")
    )

    saved_filter = DynamicModelChoiceField(
        queryset=SavedFilter.objects.all(),
        required=False,
        help_text=_("Select a saved filter to apply to this variable"),
        query_params={'content_type': '$related_object_type'},
    )

    class Meta:
        model = models.Variable
        fields = ['project', 'name', 'type',  'query_str', 'description', 'related_object_type', 'saved_filter']
    
    fieldsets = (
        FieldSet('variable', 'project', 'name', 'type', 'description'),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Mimic HTMXSelect()
        self.fields['type'].widget.attrs.update({
            'hx-get': '.',
            'hx-include': '#form_fields',
            'hx-target': '#form_fields',
        })

        # Disable changing the type of a CustomField as it almost universally causes errors if custom field data
        # is already present.
        if self.instance.pk:
            self.fields['type'].disabled = True

        field_type = get_field_value(self, 'type')

        if field_type in (
                choices.VariableTypeChoices.TYPE_QUERYSET,
        ):
            self.fields['query_str'].help_text = _("Enter context data in JSON format.")
            self.fieldsets = (
                    self.fieldsets[0],
                    FieldSet('related_object_type', 'query_str', name=_('Variable Data')),
                )
        elif field_type in (
                choices.VariableTypeChoices.TYPE_FILTER,
        ):
            self.fields['saved_filter'].required = True
            self.fields['saved_filter'].help_text = _("Select a saved filter to apply to this variable.")
            self.fieldsets = (
                    self.fieldsets[0],
                    FieldSet('related_object_type', 'saved_filter', name=_('Variable Data')),
                )
        else:
            self.fieldsets = (
                    self.fieldsets[0],
                    FieldSet('query_str', name=_('Variable Data')),
                )

    def clean(self):
                
        if self.cleaned_data.get('type') == choices.VariableTypeChoices.TYPE_QUERYSET:
            try:
                if self.cleaned_data.get('value'):
                    value = json.loads(self.cleaned_data['value'])
            except json.JSONDecodeError as e:
                raise forms.ValidationError(_("Invalid JSON data: {e}"))

