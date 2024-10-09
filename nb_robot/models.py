from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Lower
from django.conf import settings
from django import forms
import shutil



from netbox.models import NetBoxModel
from core.models import ManagedFile
from netbox.models.features import SyncedDataMixin, JobsMixin
from netbox.models import ChangeLoggedModel
from netbox.models.features import CloningMixin, ExportTemplatesMixin

import os

from . import choices

plugin_settings = settings.PLUGINS_CONFIG["nb_robot"]


class Project(NetBoxModel, JobsMixin):
    name = models.CharField(max_length=100)
    slug = models.SlugField(
        verbose_name=_('slug'),
        max_length=100
    )
    description = models.TextField(blank=True)

    @property
    def project_path(self):
        plugin_path = plugin_settings["projects_path"]
        project_path = os.path.join(plugin_path, self.slug)
        return project_path
    
    class Meta:
        constraints = (
            models.UniqueConstraint(
                Lower('name'),
                 name="%(app_label)s_%(class)s_unique_project_name"
            ),
            models.UniqueConstraint(
                Lower('slug'),
                 name="%(app_label)s_%(class)s_unique_project_slug"
            ),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:nb_robot:project', args=[self.pk])
    
    def clean(self):
        super().clean()
        if os.path.isdir(self.project_path):
            raise forms.ValidationError(f"Directory {self.project_path} already exists")
        else:
            os.makedirs(self.project_path)
    
    def save(self, *args, **kwargs):
        saved = super().save(*args, **kwargs)
        if not os.path.isdir(self.project_path):
            os.makedirs(self.project_path)
        return saved

    def delete(self, *args, **kwargs):
        deleted = super().delete(*args, **kwargs)
        if os.path.isdir(self.project_path):
            shutil.rmtree(self.project_path)
        return deleted


    
class Resource(NetBoxModel, SyncedDataMixin, ):
    name = models.CharField(
        verbose_name=_('name'),
        max_length=79, 
        editable=False,
    )
    slug = models.SlugField(
        verbose_name=_('slug'),
        max_length=100
    )
    description = models.TextField(blank=True)
    resource_type = models.CharField("Type", choices=choices.ResourceTypesChoices)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='resources') 
    
    class Meta:
        constraints = (
            models.UniqueConstraint(
                Lower('name'),
                 name="%(app_label)s_%(class)s_unique_resource_name"
            ),
            models.UniqueConstraint(
                Lower('slug'),
                 name="%(app_label)s_%(class)s_unique_resource_slug"
            ),
            models.UniqueConstraint(
                fields=("slug", "project"),
                name="%(app_label)s_%(class)s_unique_project_resource_slug",
            ),
            models.UniqueConstraint(
                fields=("name", "project"),
                name="%(app_label)s_%(class)s_unique_project_resource_name",
            ),
        )
    
    def delete(self, *args, **kwargs):
        deleted = super().delete(*args, **kwargs)
        if os.path.isfile(self.full_path):
            os.remove(self.full_path)
        return deleted
    
    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        if os.path.isfile(self.full_path):
            raise forms.ValidationError(f"File {self.full_path} already exists")
    
    def save(self, *args, **kwargs):
        self.file_root = self.project.project_path
        super().save(*args, **kwargs)

    def sync_data(self):
        if self.data_file:
            if self.name == '':
                self.name = os.path.basename(self.data_file.path)
                self.slug = self.name.replace(' ', '_')           
            self.file_path = self.full_path
            self.data_file.write_to_disk(self.full_path, overwrite=True)
            
    
    def __str__(self):
        return self.name
    
    @property
    def full_path(self):
        return os.path.join(self.project.project_path, self.slug)
    
    def get_absolute_url(self):
        return reverse('plugins:nb_robot:resource', args=[self.pk])


class Variable(NetBoxModel):

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='variables') 

    name = models.CharField(
        verbose_name=_('name'),
        max_length=79, 
    )

    type = models.CharField(
        verbose_name=_('type'),
        max_length=50,
        choices=choices.VariableTypeChoices,
        default=choices.VariableTypeChoices.TYPE_QUERYSET,
        help_text=_('The type of data this variable holds')
    )

    related_object_type = models.ForeignKey(
        to='core.ObjectType',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text=_('The type of NetBox object this field maps to (for object fields)')
    )

    description = models.TextField(blank=True)

    query_str = models.TextField(blank=True)

    saved_filter = models.ForeignKey(
        to='extras.SavedFilter',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text=_('The saved filter to use for this variable (for filter fields)')
    )
    
    @property
    def value(self):
        if self.type == choices.VariableTypeChoices.TYPE_FILTER:
            return self.saved_filter
        else:
            return self.query_str

    class Meta:
        constraints = (
            models.UniqueConstraint(
                Lower('name'),
                 name="%(app_label)s_%(class)s_unique_variable_name"
            ),
            models.UniqueConstraint(
                fields=("name", "project"),
                name="%(app_label)s_%(class)s_unique_project_variable_name",
            ),
        )
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:nb_robot:variable', args=[self.pk])