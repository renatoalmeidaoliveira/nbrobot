# Generated by Django 5.1.5 on 2025-02-11 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nb_robot', '0002_remove_variable_nb_robot_variable_unique_variable_name'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='resource',
            name='nb_robot_resource_unique_resource_name',
        ),
    ]
