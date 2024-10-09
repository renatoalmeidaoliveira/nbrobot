# Generated by Django 5.0.9 on 2024-10-08 00:06

import django.db.models.deletion
import django.db.models.functions.text
import taggit.managers
import utilities.json
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0012_job_object_type_optional'),
        ('extras', '0121_customfield_related_object_filter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('data_path', models.CharField(blank=True, editable=False, max_length=1000)),
                ('auto_sync_enabled', models.BooleanField(default=False)),
                ('data_synced', models.DateTimeField(blank=True, editable=False, null=True)),
                ('name', models.CharField(editable=False, max_length=79)),
                ('slug', models.SlugField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('resource_type', models.CharField()),
                ('data_file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.datafile')),
                ('data_source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='core.datasource')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='nb_robot.project')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(max_length=79)),
                ('type', models.CharField(default='queryset', max_length=50)),
                ('description', models.TextField(blank=True)),
                ('query_str', models.TextField(blank=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variables', to='nb_robot.project')),
                ('related_object_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.objecttype')),
                ('saved_filter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='extras.savedfilter')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
        ),
        migrations.AddConstraint(
            model_name='project',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='nb_robot_project_unique_project_name'),
        ),
        migrations.AddConstraint(
            model_name='project',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('slug'), name='nb_robot_project_unique_project_slug'),
        ),
        migrations.AddConstraint(
            model_name='resource',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='nb_robot_resource_unique_resource_name'),
        ),
        migrations.AddConstraint(
            model_name='resource',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('slug'), name='nb_robot_resource_unique_resource_slug'),
        ),
        migrations.AddConstraint(
            model_name='resource',
            constraint=models.UniqueConstraint(fields=('slug', 'project'), name='nb_robot_resource_unique_project_resource_slug'),
        ),
        migrations.AddConstraint(
            model_name='resource',
            constraint=models.UniqueConstraint(fields=('name', 'project'), name='nb_robot_resource_unique_project_resource_name'),
        ),
        migrations.AddConstraint(
            model_name='variable',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='nb_robot_variable_unique_variable_name'),
        ),
        migrations.AddConstraint(
            model_name='variable',
            constraint=models.UniqueConstraint(fields=('name', 'project'), name='nb_robot_variable_unique_project_variable_name'),
        ),
    ]
