from django.core.exceptions import MultipleObjectsReturned, ValidationError, ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext as _


from netbox.views import generic


from netbox.plugins.utils import get_plugin_config
from utilities.views import ViewTab, register_model_view
from utilities.request import copy_safe_request
from utilities.rqworker import get_workers_for_queue
from core.models import Job
from core.tables import JobTable


import logging

logger = logging.getLogger(__name__)

from . import forms, models, tables, filtersets, jobs

# Project Views

class ProjectView(generic.ObjectView):
    queryset = models.Project.objects.all()

    def get_extra_context(self, request, instance):
        return {
            "resource_table" : tables.ResourceTable(instance.resources.all(), request=request),
        }
    
    def post(self, request, **kwargs):

        instance = self.get_object(**kwargs)
        print(request.POST)
        if not get_workers_for_queue('default'):
            messages.error(request, _("Unable to run script: RQ worker process not running."))
        robot_job = jobs.RobotJob.enqueue(instance=instance,
                                          request=copy_safe_request(request),
                                          project=instance,
                                          user=request.user
                                        )

        return render(request, self.get_template_name(), {
            'object': instance,
            'tab': self.tab,
            **self.get_extra_context(request, instance),
        })

class ProjectJobsView(generic.ObjectChildrenView):
    queryset = models.Project.objects.all()
    child_model = Job
    table = tables.JobsTable
    template_name = "nb_robot/project_jobs.html"
    # tab = ViewTab(label='Jobs', badge=lambda obj: obj.jobs.filter(status='completed').count(), hide_if_empty=True)

    def get_children(self, request, parent):
            childrens = parent.jobs.filter(status='completed')
            return childrens

    def get_extra_context(self, request, instance):

        return {
            'custom_tab': instance.jobs.filter(status='completed').count()
        }
    
class ProjectJobResultView(generic.ObjectView):
    queryset = Job.objects.all()
    template_name = "nb_robot/project_jobs_result.html"

class ProjectJobResultTableView(generic.ObjectView):
    queryset = Job.objects.all()
    template_name = "nb_robot/project_jobs_result_table.html"

class ProjectJobResultXMLView(generic.ObjectView):
    queryset = Job.objects.all()
    template_name = "nb_robot/project_job_xml.html"



class ProjectListView(generic.ObjectListView):
    queryset = models.Project.objects.all()
    filterset = filtersets.ProjectFilterSet
    filterset_form = forms.ProjectFilterForm
    table = tables.ProjectTable

class ProjectEditView(generic.ObjectEditView):
    queryset = models.Project.objects.all()
    form = forms.ProjectForm

class ProjectDeleteView(generic.ObjectDeleteView):
    queryset = models.Project.objects.all()

class ProjectBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Project.objects.all()
    table = tables.ProjectTable

class ProjectBulkImportView(generic.BulkImportView):
    queryset = models.Project.objects.all()
    table = tables.ProjectTable
    form = forms.ProjectBulkImportForm

# Resouce Views

class ResourceView(generic.ObjectView):
    queryset = models.Resource.objects.all()

@register_model_view(models.Resource, name='resource_source')
class ResouceSourceView(generic.ObjectView):
    queryset = models.Resource.objects.all()
    template_name = "nb_robot/resource_source.html"
    tab = ViewTab(label='Source')

    def get_extra_context(self, request, instance):
        resource_path = instance.full_path
        content = ""
        try:
            with open(resource_path, 'r') as f:
                content = f.read()
        except Exception as e:
            content = f"Error reading file: {e}"
        return {
            'content': content,
        }



class ResourceListView(generic.ObjectListView):
    queryset = models.Resource.objects.all()
    filterset = filtersets.ResourceFilterSet
    filterset_form = forms.ResourceFilterForm
    table = tables.ResourceTable

class ResourceEditView(generic.ObjectEditView):
    queryset = models.Resource.objects.all()
    form = forms.ResourceForm

    def alter_object(self, instance, request, *args, **kwargs):
        if 'upload_file' in request.FILES:
            instance.name = request.FILES['upload_file'].name
            instance.slug = instance.name.replace(' ', '_')

        
        return instance

class ResourceDeleteView(generic.ObjectDeleteView):
    queryset = models.Resource.objects.all()

class ResourceBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Resource.objects.all()
    table = tables.ResourceTable


# Variable Views

class VariableView(generic.ObjectView):
    queryset = models.Variable.objects.all()

class VariableEditView(generic.ObjectEditView):
    queryset = models.Variable.objects.all()
    form = forms.VariableForm

class VariableListView(generic.ObjectListView):
    queryset = models.Variable.objects.all()
    filterset = filtersets.VariableFilterSet
    filterset_form = forms.VariableFilterForm
    table = tables.VariableTable

class VariableDeleteView(generic.ObjectDeleteView):
    queryset = models.Variable.objects.all()