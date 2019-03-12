from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2.QtCore import Qt

class PluginsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, plugin_manager=None):
        super().__init__(parent)
        self.setWindowTitle("Plugins")
        self.setWindowIcon(QtGui.QIcon("resources/icons/puzzle.png"))
        self.resize(600, 400)

        self.plugin_manager = plugin_manager
        
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.set_plugin_button = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/application-plus.png"), "Set as central")
        self.install_plugin_button = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/plus.png"), "Install plugin", self)
        self.uninstall_plugin_button = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/minus.png"), "Uninstall plugin", self)
        self.enable_plugin_button = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/tick.png"), "Enable plugin", self)
        self.disable_plugin_button = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/cross.png"), "Disable plugin", self)
        self.plugins_layout = QtWidgets.QVBoxLayout()
        self.plugins_table = QtWidgets.QTableWidget(self)
        self.plugins_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.plugins_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok|
            QtWidgets.QDialogButtonBox.Close, parent=self)

        self._populate_plugins_table()

        self.set_plugin_button.clicked.connect(self._on_set)

        self.buttons_layout.addWidget(self.set_plugin_button)
        self.buttons_layout.addWidget(self.install_plugin_button)
        self.buttons_layout.addWidget(self.uninstall_plugin_button)
        self.buttons_layout.addWidget(self.enable_plugin_button)
        self.buttons_layout.addWidget(self.disable_plugin_button)
        self.plugins_layout.addLayout(self.buttons_layout)
        self.plugins_layout.addWidget(self.plugins_table)
        self.plugins_layout.addWidget(self.button_box)
        self.setLayout(self.plugins_layout)
        self.button_box.rejected.connect(self._on_reject) # FIXME: dodati callback funkciju
        self.button_box.accepted.connect(self._on_accept) # FIXME: dodati callback funkciju

    def _on_accept(self):
        # TODO:
        self.reject()

    def _on_reject(self):
        # TODO: 
        self.accept()

    def _on_set(self):
        """
        Metoda koja se poziva kada se pritisne na dugme set central.
        """
        selected_items = self.plugins_table.selectedItems()
        if len(selected_items) == 0:
            return
        # na drugoj poziciji se nalazi simbolicko ime plugina.
        symbolic_name = selected_items[2].text()
        self.parent().set_central_widget(symbolic_name)


    def _on_install_plugin(self):
        # Ova metoda bi nam znacila ako odaberemo da se instaliraju pluginovi
        # tako sto se odabere folder u kojem se nalazi plugin
        pass
        # TODO: azurirati konfiguracioni fajl sa pluginovima, kako bi se pri svakom sledecem
        # pokretanju instalirani pluginovi dodali u aplikaciju

    def _populate_plugins_table(self):
        self.plugins_table.setColumnCount(4)
        self.plugins_table.setRowCount(len(self.plugin_manager._plugins))
        self.plugins_table.setHorizontalHeaderLabels(["Author", "Version", "Symbolic name", "Status"])
        for i, plugin in enumerate(self.plugin_manager._plugins):
            author = QtWidgets.QTableWidgetItem(plugin._plugin_specification.author)
            author.setFlags(author.flags()^Qt.ItemIsEditable)
            version = QtWidgets.QTableWidgetItem(plugin._plugin_specification.version)
            version.setFlags(version.flags()^Qt.ItemIsEditable)
            symbolic_name = QtWidgets.QTableWidgetItem(plugin._plugin_specification.symbolic_name)
            symbolic_name.setFlags(version.flags()^Qt.ItemIsEditable)
            enabled = QtWidgets.QTableWidgetItem("Enabled")
            enabled.setFlags(enabled.flags()^Qt.ItemIsEditable)
            self.plugins_table.setItem(i, 0, author)
            self.plugins_table.setItem(i, 1, version)
            self.plugins_table.setItem(i, 2, symbolic_name)
            self.plugins_table.setItem(i, 3, enabled)

        
        

    
        