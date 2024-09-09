from netbox.plugins import PluginConfig
from .version import __version__


class NbrobotConfig(PluginConfig):
    name = 'nb_robot'
    verbose_name = 'Robot Framework Integration'
    description = 'Robot Framework Integration for NetBox'
    version = __version__
    author = 'Renato Almeida de Oliveira Zaroubin'
    author_email = 'renato.almeida.oliveira@gmail.com'
    required_settings = []
    default_settings = {}


config = NbrobotConfig # noqa
