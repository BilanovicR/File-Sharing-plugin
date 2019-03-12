from plugin_framework.plugin_interface import PluginInterface


class Plugin(PluginInterface):

    def __init__(self, plugin_specification):
        super().__init__()
        self._plugin_specification = plugin_specification

    