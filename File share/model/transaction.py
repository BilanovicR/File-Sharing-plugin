from PySide2 import QtNetwork
from PySide2.QtCore import QFile, QByteArray, Signal, QIODevice
from .setup import Setup
from .transaction_status_enum import TransactionStatus
import os
from struct import *


class Transaction():
    def __init__(self, file_path, receiver, socket):
        self._file_path = file_path
        self._my_file = QFile(self._file_path)
        self._receiver_address = QtNetwork.QHostAddress(receiver.get_ip_address())
        self._file_size = self._my_file.size()
        self._status = TransactionStatus.WAITING
        self._remaining_bytes = self._file_size
        self._socket = socket

    def get_my_file(self):
        return self._my_file

    def get_receiver_address(self):
        return self._receiver_address

    def get_size(self):
        return self._file_size

    def get_status(self):
        return self._status

    def get_remaining_bytes(self):
        return self._remaining_bytes

    def set_my_file(self, new_file):
        self._my_file = new_file

    def set_receiver_address(self, new_receiver_address):
        self._receiver_address= new_receiver_address

    def set_file_size(self, new_size):
        self._file_size = new_size

    def set_status(self, new_status):
        self._status = new_status

    def set_remaining_bytes(self, now_remaining_bytes):
        self._remaining_bytes = now_remaining_bytes

    def write_datagram(self):
        file_name = os.path.split(self._file_path)[1]
        file_to_byte_array = QByteArray()
        data = QByteArray()        
        file_to_byte_array.resize(self._file_size)
        QFile.open(self._my_file, QIODevice.ReadOnly)
        file_to_byte_array = self._my_file.readAll()
        self._my_file.close()

        #size_string = str(self._file_size)
        self._socket.writeDatagram(QByteArray(bytes(file_name, "utf8")), QtNetwork.QHostAddress(self._receiver_address), Setup().get_port())
        #self._socket.writeDatagram(QByteArray(pack("N",self._size)), QtNetwork.QHostAddress(self._receiver_address), 17116)
        i = 0

        while (self._remaining_bytes > 0):
            if(self._remaining_bytes>Setup().get_buffer_size()):
                data.resize(Setup().get_buffer_size())
                data = file_to_byte_array.mid(0 , Setup().get_buffer_size())
            else:
                data.resize(file_to_byte_array.size())
                data = file_to_byte_array

            datagram = QtNetwork.QNetworkDatagram()            
            datagram.setData(data)
            datagram.setDestination(self._receiver_address, Setup().get_port())
            self._socket.writeDatagram(datagram)
            i += 1
            self._remaining_bytes -= data.size()
            file_to_byte_array.remove(0, data.size())
            if (self._remaining_bytes == 0):
                self._socket.disconnectFromHost()
    