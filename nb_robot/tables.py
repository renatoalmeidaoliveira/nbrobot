import django_tables2 as tables
from django_tables2.utils import Accessor
from django.utils.html import format_html
from django.urls import reverse

from netbox.tables import NetBoxTable, columns
from django.db.models import Count
from core.models import Job

from . import models


# Project Tables

class ProjectTable(NetBoxTable):

    name = tables.Column(linkify=True)


    class Meta(NetBoxTable.Meta):
        model = models.Project
        fields = ['pk', 'name', 'description']
        default_columns = ['name', 'description']


# Resource Tables

class ResourceTable(NetBoxTable):

    name = tables.Column(linkify=True)
    project = tables.Column("Project", linkify=True, accessor=Accessor('project.name'))

    class Meta(NetBoxTable.Meta):
        model = models.Resource
        fields = ['pk', 'name', 'project', 'description', 'resource_type'] 
        default_columns = ['name','resource_type', 'project']

class JobsTable(NetBoxTable):

    actions = columns.ActionsColumn(actions=('delete',))

    results = tables.Column(verbose_name="Results", orderable=False,empty_values=() )
    
    def render_results(self, record):
        job_data = record.data
        passed = job_data.get("passed",0)
        failed = job_data.get("failed",0)
        total = job_data.get("total",0)
        html = f'<span class="badge bg-success">{ passed }</span> <span class="badge bg-danger">{ failed }</span> <span class="badge bg-secondary">{ total }</span>'
        return format_html(html)

    def render_id(self, record):
        """
        This function will render over the default id column. 
        By adding <a href> HTML formatting around the id number a link will be added, 
        thus acting the same as linkify. The record stands for the entire record
        for the row from the table data.
        """
        return format_html('<a href="{}">{}</a>',
                           reverse('plugins:nb_robot:project_job_result',
                           kwargs={'pk': record.id}),
                           record.id)
    
    class Meta(NetBoxTable.Meta):
        model = Job
        fields = ['pk', 'name', 'created', 'completed', 'status', 'results' ]
        default_columns = ['id', 'created', 'completed', 'status', 'results']

# Variable Tables

class VariableTable(NetBoxTable):
    
        name = tables.Column(linkify=True)
        project = tables.Column("Project", linkify=True, accessor=Accessor('project.name'))
    
        class Meta(NetBoxTable.Meta):
            model = models.Variable
            fields = ['pk', 'name', 'project', 'type']
            default_columns = ['name', 'type', 'project']