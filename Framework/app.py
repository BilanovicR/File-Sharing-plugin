# from plugin1.plugin import Plugin
from plugin_framework.plugin_specification import PluginSpecification
from plugin_framework.plugin_manager import *
from PySide2 import QtWidgets
from interface.main_window import MainWindow
import sys



plugin_manager = PluginManager()

plugin_manager.install()
# print(len(plugin_manager._plugins))


app = QtWidgets.QApplication(sys.argv)
main_window = MainWindow(plugin_manager=plugin_manager)
main_window.show()
sys.exit(app.exec_())


