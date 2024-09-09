from django.urls import path, include
from utilities.urls import get_model_urls
from netbox.views.generic import ObjectChangeLogView, ObjectJournalView

from . import models, views

app_name = 'nb_robot'

urlpatterns = ()