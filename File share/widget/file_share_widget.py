from PySide2 import QtWidgets, QtGui, QtCore
from .select_receiver_dialog import SelectReceiverDialog
from .setup_dialog import SetupDialog
from ..model.setup import Setup
from ..model.broadcaster import Broadcaster
from ..model.device import Device
from ..model.file import MyFile
from ..model.sender import Sender
from ..util.converter import Converter
from PySide2.QtCore import QFile, QDataStream, QObject, Signal, Slot
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
        self.table_view_upload.setColumnCount(4)
        self.header_upload = self.table_view_upload.horizontalHeader()
        self.header_upload.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        self.header_upload.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        self.header_upload.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)
        self.header_upload.setSectionResizeMode(
            3, QtWidgets.QHeaderView.ResizeToContents)
        self.table_view_upload.setHorizontalHeaderLabels(
            ["File", "Size", "Receiver", "Completed"])
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
        self.table_view_download.setColumnCount(4)
        self.header_download = self.table_view_download.horizontalHeader()
        self.header_download.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        self.header_download.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        self.header_download.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)
        self.header_download.setSectionResizeMode(
            3, QtWidgets.QHeaderView.ResizeToContents)
        self.table_view_download.setHorizontalHeaderLabels(
            ["File", "Size", "Sender", "Completed"])
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
        #self.this_device._server.newConnection.connect(self.receive_file)
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
        self.this_device.send_file(file_path, receiver)
        print("dodat upload")
        qfile = QFile(file_path)
        size_of_file = qfile.size()
        
        rows = self.table_view_upload.rowCount()
        self.table_view_upload.setRowCount(rows+1)

        name = QtWidgets.QTableWidgetItem()
        name.setText(file_path)
        name.setFlags(name.flags() ^ QtCore.Qt.ItemIsEditable)

        size = QtWidgets.QTableWidgetItem()
        size.setText(Converter().size_to_string(size_of_file))
        size.setFlags(size.flags() ^ QtCore.Qt.ItemIsEditable)

        send_progress = QtWidgets.QProgressBar()
        send_progress.setValue(0)

        receiver_name = QtWidgets.QTableWidgetItem()
        receiver_name.setText(receiver.get_name())
        receiver_name.setFlags(receiver_name.flags() ^ QtCore.Qt.ItemIsEditable)

        self.table_view_upload.setItem(rows, 0, name)
        self.table_view_upload.setItem(rows, 1, size)
        self.table_view_upload.setItem(rows, 2, receiver_name)
        self.table_view_upload.setCellWidget(rows, 3, send_progress)


    def receive_file(self):
        print("dodat download")
        rows = self.table_view_download.rowCount()
        self.table_view_download.setRowCount(rows+1)

        name = QtWidgets.QTableWidgetItem()
        name.setText(self.this_device._receiver.get_file_name())
        name.setFlags(name.flags() ^ QtCore.Qt.ItemIsEditable)
        self.table_view_download.setItem(rows, 0, name)

        size = QtWidgets.QTableWidgetItem()
        size.setText(str(self.this_device._receiver.get_file_size()))
        size.setFlags(size.flags() ^ QtCore.Qt.ItemIsEditable)
        self.table_view_download.setItem(rows, 1, size)

        sender = QtWidgets.QTableWidgetItem()
        sender.setText(str(self.this_device._receiver._socket.peerAddress()))
        sender.setFlags(sender.flags() ^ QtCore.Qt.ItemIsEditable)
        self.table_view_download.setItem(rows, 2, sender)

        receive_progress = QtWidgets.QProgressBar()
        receive_progress.setValue(0)
        self.table_view_download.setCellWidget(rows, 3, receive_progress)
        