from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import QDir
from ..model.setup import Setup

class SetupDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Setup")
        self.setWindowIcon(QtGui.QIcon("resources/icons/wrench-screwdriver.png"))
        self.setup = Setup()

        self.nameLabel = QtWidgets.QLabel("Name")
        self.nameLineEdit = QtWidgets.QLineEdit(self)
        self.nameLineEdit.setText(self.setup.get_name())
        self.nameLineEdit.clearFocus() #TODO namesti da se izgubi fokus na input polja
        self.nameLabel.setBuddy(self.nameLineEdit)

        self.portLabel = QtWidgets.QLabel("Port")
        self.portLineEdit = QtWidgets.QLineEdit(self)
        self.portLineEdit.setText(str(self.setup.get_port()))
        self.portLabel.setBuddy(self.portLineEdit)

        self.download_dirLabel = QtWidgets.QLabel("Download directory")
        self.download_dirLineEdit = QtWidgets.QLineEdit(self)
        self.download_dirLineEdit.setText(self.setup.get_download_dir())
        self.download_dirButton = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/folder-smiley.png"), None)
        self.download_dirButton.setToolTip("Select directory..")
        self.download_dirButton.clicked.connect(self.on_select_dir)
        self.download_dirLabel.setBuddy(self.download_dirLineEdit)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.addWidget(self.nameLabel, 0, 0)
        self.gridLayout.addWidget(self.nameLineEdit, 0, 1)
        self.gridLayout.addWidget(self.portLabel, 1, 0)
        self.gridLayout.addWidget(self.portLineEdit, 1, 1)
        self.gridLayout.addWidget(self.download_dirLabel, 2, 0)
        self.gridLayout.addWidget(self.download_dirLineEdit, 2, 1)
        self.gridLayout.addWidget(self.download_dirButton, 2, 2)
        
        

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok 
            | QtWidgets.QDialogButtonBox.Cancel, parent=self)
        self.button_box.accepted.connect(self.on_accept)
        self.button_box.rejected.connect(self.reject)
        self.gridLayout.addWidget(self.button_box)
        self.setLayout(self.gridLayout)

    def on_accept(self):
        self.setup.set_download_dir(self.download_dirLineEdit.text())
        self.setup.set_port(self.portLineEdit.text())
        self.setup.set_name(self.nameLineEdit.text())

    def on_select_dir(self):
        #TODO
        self.dir = QtWidgets.QFileDialog()
        self.dir.setWindowIcon(QtGui.QIcon("resources/icons/folder-smiley.png"))
        self.selected_dir = self.dir.getExistingDirectory(self, "Select Directory",
                                       ".",
                                       QtWidgets.QFileDialog.ShowDirsOnly
                                       | QtWidgets.QFileDialog.DontResolveSymlinks)
        
        print(self.selected_dir)#sacuvaj izabrani dir i upisi sve vrednosti da se ucitaju
        self.setup.set_download_dir(self.selected_dir)
        

