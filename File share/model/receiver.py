from PySide2 import QtNetwork
from .setup import Setup
from PySide2.QtCore import QFile, QByteArray, QIODevice
from struct import *


class Receiver():
    def __init__(self, socket):
        print("napravljen Receiver")
        self._socket = socket
        #self._counter = 0
        #self._transaction = None
        #self._sender = None
        self._file_name = None
        #self._socket.readyRead.connect(self.start)
        self._receiving_file = None
        self._bytearray_to_file = QByteArray()

    def read_name_datagram(self):
        file_name, host, port = self._socket.readDatagram(self._socket.pendingDatagramSize())
        name = str(file_name.data(), encoding="utf8")
        self._file_name = name
        self._receiving_file = QFile(self._file_name)
        return self._file_name

        

    def read_data_datagram(self):
        datagram = self._socket.receiveDatagram(self._socket.pendingDatagramSize())
        new_size = self._receiving_file.size() + datagram.data().size()
        self._receiving_file.resize(new_size)
        self._bytearray_to_file.resize(new_size)
        self._bytearray_to_file.append(datagram.data())
        self._receiving_file.open(QIODevice.WriteOnly)
        self._receiving_file.write(self._bytearray_to_file)
        self._receiving_file.close()


        print("added bytes to file")


    # def start(self):
    #     print("receiver : start")
    #     while self._socket.hasPendingDatagrams():
    #         if (self._counter == 0):
    #             self.read_name_datagram()
    #         else:
    #             self.read_data_datagram()
    #         self._counter += 1
    #     self._receiving_file.open(QIODevice.WriteOnly)
    #     self._receiving_file.write(self._bytearray_to_file)
    #     self._receiving_file.close()
    #     print("finished writing, file should be done")    