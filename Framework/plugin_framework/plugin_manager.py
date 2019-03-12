import json
import os
from plugin_framework.plugin_specification import PluginSpecification
from importlib import import_module
from inspect import getmembers, isclass

class PluginManager:
    def __init__(self):
        self._plugins = []

    def activate(self, plugin):
        plugin.activate()
        self._plugins.append(plugin)

    def deactivate(self, plugin):
        plugin.deactivate()
        self._plugins.remove(plugin)
    
    def install(self, path="plugins"):
        for d in os.scandir(path):
            if d.is_dir() and (d.name != "__pycache__"):
                package_path = os.path.join(path, d.name)
                plugin_path = os.path.join(package_path, "plugin.py")
                spec_path = os.path.join(package_path, "spec.json")
                with open(spec_path, "r") as fp:
                    spec = json.load(fp)
                    plugin_module = import_module(plugin_path.replace(os.path.sep, ".").rstrip(".py"))
                    class_members = getmembers(plugin_path, isclass)
                    if len(class_members) == 1:
                        plugin = plugin_module.Main(PluginSpecification(spec))
                        self.activate(plugin)

    def uninstall(self, plugin):
        # deaktivirati plugin
        # izmenimo specifikaciju konfiguracione datoteke da je plugin obrisan
        self.deactivate(plugin)

    def get_by_symbolic_name(self, symbolic_name):
        """
        Vraca plugin koji ima naziv symbolic_name. Ukoliko se podesi da vise pluginova ima isti symbolic_name, vraca
        se samo prvi.

        :param symbolic_name: naziv spram kog pretrazujemo sve dostupne pluginove.
        :type symbolic_name: str
        :returns: Plugin -- pronadjeni plugin.
        :raises: IndexError -- ukoliko ne postoji ni jedan plugin koji je zadovoljio filter.
        """
        print(self._plugins[0]._plugin_specification.symbolic_name, symbolic_name)
        return list(filter(lambda x: x._plugin_specification.symbolic_name == symbolic_name, self._plugins))[0]
    

        
