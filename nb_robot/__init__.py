from django.conf import settings
from netbox.plugins import PluginConfig

from .version import __version__
import os


class NbrobotConfig(PluginConfig):
    name = 'nb_robot'
    verbose_name = 'Robot Framework Integration'
    description = 'Robot Framework Integration Plugin'
    version = __version__
    author = 'Renato Almeida de Oliveira Zaroubin'
    author_email = 'renato.almeida.oliveira@gmail.com'
    min_version = "4.1.0"
    max_version = "4.1.99"
    required_settings = []
    default_settings = {
        "projects_path": "/opt/netbox/netbox/robot_projects",
    }

    def ready(self):
        from . import signals
        super().ready()
        plugin_settings = settings.PLUGINS_CONFIG["nb_robot"]
        if not os.path.isdir(plugin_settings["projects_path"]):
            raise Exception(f"Directory {plugin_settings['projects_path']} does not exist")


config = NbrobotConfig # noqa
