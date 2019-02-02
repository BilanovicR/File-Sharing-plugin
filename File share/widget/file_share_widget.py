from PySide2 import QtWidgets, QtGui, QtCore
from .select_receiver_dialog import SelectReceiverDialog
from .setup_dialog import SetupDialog
from ..model.setup import Setup
from ..model.broadcaster import Broadcaster
from ..model.device import Device
from ..model.sender import Sender
from ..util.converter import Converter
from PySide2.QtCore import QFile, QDataStream
import os


class FileShareWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.vbox_layout = QtWidgets.QVBoxLayout()

        self.header = QtWidgets.QLabel()
        self.header.setText("File Share")

        self.hbox_layout = QtWidgets.QHBoxLayout()
        self.button_select_file = QtWidgets.QPushButton(QtGui.QIcon(
            "resources/icons/document-share.png"), "Select file", self)
        self.button_select_file.clicked.connect(self.on_select_file)
        self.button_select_file.setMinimumSize(100, 50)
        self.button_select_file.setMaximumSize(150, 50)
        self.button_setup = QtWidgets.QPushButton(
            QtGui.QIcon("resources/icons/wrench.png"), "Settings", self)
        self.button_setup.clicked.connect(self.on_setup)
        self.button_setup.setMinimumSize(100, 50)
        self.button_setup.setMaximumSize(150, 50)

        self.hbox_layout.addWidget(self.button_setup)
        self.hbox_layout.addWidget(self.button_select_file)

        self.vbox_layout_upload = QtWidgets.QVBoxLayout()
        self.label_upload = QtWidgets.QLabel()
        self.label_upload.setText("Upload")
        self.table_view_upload = QtWidgets.QTableWidget()
        self.table_view_upload.setSelectionMode(
            QtWidgets.QTableView.SingleSelection)
        self.table_view_upload.setSelectionBehavior(
            QtWidgets.QTableView.SelectionBehavior.SelectRows)
        self.table_view_upload.setColumnCount(3)
        self.header_upload = self.table_view_upload.horizontalHeader()
        self.header_upload.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        self.header_upload.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        self.header_upload.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)
        self.table_view_upload.setHorizontalHeaderLabels(
            ["File", "Size", "Completed"])
        self.vbox_layout_upload.addWidget(self.label_upload)
        self.vbox_layout_upload.addWidget(self.table_view_upload)

        self.splitter = QtWidgets.QSplitter()
        self.splitter.setHandleWidth(2)

        self.vbox_layout_download = QtWidgets.QVBoxLayout()
        self.label_download = QtWidgets.QLabel()
        self.label_download.setText("Download")
        self.table_view_download = QtWidgets.QTableWidget()
        self.table_view_download.setSelectionMode(
            QtWidgets.QTableView.SingleSelection)
        self.table_view_download.setColumnCount(3)
        self.header_download = self.table_view_download.horizontalHeader()
        self.header_download.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        self.header_download.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        self.header_download.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)
        self.table_view_download.setHorizontalHeaderLabels(
            ["File", "Size", "Completed"])
        self.table_view_download.setSelectionBehavior(
            QtWidgets.QTableView.SelectionBehavior.SelectRows)
        self.vbox_layout_download.addWidget(self.label_download)
        self.vbox_layout_download.addWidget(self.table_view_download)

        self.vbox_layout.addWidget(self.header)
        self.vbox_layout.addLayout(self.hbox_layout)
        self.vbox_layout.addLayout(self.vbox_layout_upload)
        self.vbox_layout.addWidget(self.splitter)
        self.vbox_layout.addLayout(self.vbox_layout_download)
        self.setLayout(self.vbox_layout)
        self.broadcaster = Broadcaster()
        self.this_device = Device()
        self.this_device.set_this_device()
        self.broadcaster.start_broadcast()
        self.selected_file_path = None
        self.selected_device = None

    def on_select_file(self):
        select_file_dialog = QtWidgets.QFileDialog(self)
        if select_file_dialog.exec_():
            self.selected_file_path = select_file_dialog.selectedFiles()[0]
        select_receiver_dialog = SelectReceiverDialog(
            self.broadcaster.get_other_devices())
        if select_receiver_dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.selected_device = select_receiver_dialog.selected_device
            self.send_file(self.selected_file_path, self.selected_device)

    def on_setup(self):
        dialog = SetupDialog(self.parent())
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            # TODO popravi izmenu elemenata iz setup-a
            pass

    def send_file(self, file_path, receiver):
        qfile = QFile(file_path)
        size_of_file = qfile.size()
        self.this_device.send_file(file_path, receiver)
        rows = self.table_view_upload.rowCount()
        self.table_view_upload.setRowCount(rows+1)
        name = QtWidgets.QTableWidgetItem()
        name.setText(file_path)
        name.setFlags(name.flags() ^ QtCore.Qt.ItemIsEditable)
        size = QtWidgets.QTableWidgetItem()
        size.setText(Converter().size_to_string(size_of_file))
        size.setFlags(size.flags() ^ QtCore.Qt.ItemIsEditable)
        self.table_view_upload.setItem(rows, 0, name)
        self.table_view_upload.setItem(rows, 1, size)
        # dodati procenat koliko je zavrseno

    def receive_file(self, file_name):
        rows = self.table_view_download.rowCount()
        self.table_view_download.setRowCount(rows+1)
        name = QtWidgets.QTableWidgetItem()
        name.setText(file_name)
        name.setFlags(name.flags() ^ QtCore.Qt.ItemIsEditable)
        self.table_view_download.setItem(rows, 0, name)