from django.urls import path, include
from utilities.urls import get_model_urls
from netbox.views.generic import ObjectChangeLogView, ObjectJournalView

from . import models, views

app_name = 'nb_robot'

urlpatterns = (
    # Project Views
        # path('project/<int:pk>/', include(get_model_urls(app_name, 'project'))),

        path('project/', views.ProjectListView.as_view(), name='project_list'),
        path('project/add/', views.ProjectEditView.as_view(), name='project_add'),
        path("project/<int:pk>/", views.ProjectView.as_view(), name="project"),
        path('project/<int:pk>/edit/', views.ProjectEditView.as_view(), name='project_edit'),
        path('project/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
        path('project/delete/', views.ProjectBulkDeleteView.as_view(), name='project_bulk_delete'),
        path('project/import/', views.ProjectBulkImportView.as_view(), name='project_bulk_import'),
        path('project/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='project_changelog', kwargs={
            'model': models.Project
        }),
        path('project/<int:pk>/journal/', ObjectJournalView.as_view(), name='project_journal', kwargs={
            'model': models.Project
        }),
        path("project/<int:pk>/jobs/", views.ProjectJobsView.as_view(), name="project_jobs"),
        path('project/results/<int:pk>/', views.ProjectJobResultView.as_view(), name='project_job_result'),
        path('project/results/<int:pk>/result', views.ProjectJobResultTableView.as_view(), name='project_job_result_result'),
        path('project/results/<int:pk>/xml', views.ProjectJobResultXMLView.as_view(), name='project_job_result_xml'),
    # Resource Views
        path('resource/<int:pk>/', include(get_model_urls(app_name, 'resource'))),
        path('resource/', views.ResourceListView.as_view(), name='resource_list'),
        path('resource/add/', views.ResourceEditView.as_view(), name='resource_add'),
        path("resource/<int:pk>/", views.ResourceView.as_view(), name="resource"),
        path('resource/<int:pk>/edit/', views.ResourceEditView.as_view(), name='resource_edit'),
        path('resource/<int:pk>/delete/', views.ResourceDeleteView.as_view(), name='resource_delete'),

    # Variable Views
        path('variable/<int:pk>/', include(get_model_urls(app_name, 'variable'))),
        path('variable/', views.VariableListView.as_view(), name='variable_list'),
        path('variable/add/', views.VariableEditView.as_view(), name='variable_add'),
        path("variable/<int:pk>/", views.VariableView.as_view(), name="variable"),
        path('variable/<int:pk>/edit/', views.VariableEditView.as_view(), name='variable_edit'),
        path('variable/<int:pk>/delete/', views.VariableDeleteView.as_view(), name='variable_delete'),
)