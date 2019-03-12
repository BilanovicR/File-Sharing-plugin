from PySide2 import QtWidgets, QtCore, QtGui, QtNetwork
from ..model.broadcaster import Broadcaster
from ..model.device import Device

class SelectReceiverDialog(QtWidgets.QDialog):
    def __init__(self, lista, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select receiver")
        self.setWindowIcon(QtGui.QIcon("resources/icons/user-share.png"))
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.devices = list(lista)
        self.selected_device = None

        self.button_refresh = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/arrow-circle-double-135.png"), None, self)
        self.button_refresh.clicked.connect(self.populate_receivers)

        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, parent=self)
        self.button_box.accepted.connect(self.on_accept)
        self.button_box.rejected.connect(self.reject)

        self.table_view_receivers = QtWidgets.QTableWidget()
        self.table_view_receivers.setSelectionMode(QtWidgets.QTableView.MultiSelection)
        self.table_view_receivers.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        
        self.vbox_layout.addWidget(self.button_refresh)
        self.vbox_layout.addWidget(self.table_view_receivers)
        self.vbox_layout.addWidget(self.button_box)
        self.setLayout(self.vbox_layout)
        self.populate_receivers()


    def populate_receivers(self):
        self.table_view_receivers.setColumnCount(2)
        self.table_view_receivers.setRowCount(len(self.devices))
        self.table_view_receivers.setHorizontalHeaderLabels(["Name", "Ip address"])
        for i in range(len(self.devices)):
            name = QtWidgets.QTableWidgetItem()
            name.setText(self.devices[i].get_name())
            name.setFlags(name.flags()^QtCore.Qt.ItemIsEditable)
            ip = QtWidgets.QTableWidgetItem()
            ip.setText((self.devices[i].get_ip_address()).toString())
            ip.setFlags(ip.flags()^QtCore.Qt.ItemIsEditable)
            self.table_view_receivers.setItem(i, 0, name)
            self.table_view_receivers.setItem(i, 1, ip)
            self.table_view_receivers.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)

    def on_accept(self):
        selected_item = self.table_view_receivers.selectedItems()
        if len(selected_item) == 0:
            return
        else:
            self.selected_device = Device()
            self.selected_device.set_name(selected_item[0].text())
            self.selected_device.set_ip_address(QtNetwork.QHostAddress(selected_item[1].text()))
            self.accept()
