from PySide2 import QtNetwork
from .setup import Setup
from PySide2.QtCore import QFile, QByteArray, QIODevice, Signal, QDataStream, QObject
from sys import getsizeof
from pathlib import Path


class Receiver():
    def __init__(self, socket):
        self._socket = socket
        self._transaction = None
        self._sender = None
        self._file_name = None
        self._socket.readyRead.connect(self.start)
        self._receiving_file = None
        self._bytearray_to_file = QByteArray()
        self._file_size = 0

    def get_file_name(self):
        return self._file_name

    def get_file_size(self):
        return self._file_size

    def get_sender(self):
        return self._sender

    def start(self):
        self._sender = self._socket.peerAddress()
        stream = QDataStream(self._socket)
        if(self._file_size == 0):
            if (self._socket.bytesAvailable() < getsizeof(int)):
                return
            self._file_size = stream.readUInt32()
        if(self._socket.bytesAvailable() < self._file_size):
            return
        self._file_name = stream.readString()
        line = QByteArray()
        line = self._socket.readAll()
        directory = Path(Setup().get_download_dir())
        if not (directory.exists() and directory.is_dir()):
            directory.mkdir()
        self._receiving_file = QFile(Setup().get_download_dir() + str(self._file_name))
        print(Setup().get_download_dir() + str(self._file_name))
        if not (self._receiving_file.open(QIODevice.WriteOnly)):
            print("can't open file")
            return
        self._receiving_file.write(line)
        self._receiving_file.close()
        self._socket.disconnectFromHost()
        print("finished")
        return self._receiving_file