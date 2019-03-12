from PySide2.QtCore import QFile

class MyFile(QFile):
    def __init__(self, name, path, size):
        super().__init__()
        self._name = name
        self._path = path
        self._size = size

    def get_name(self):
        return self._name

    def get_path(self):
        return self._path

    def get_size(self):
        return self._size