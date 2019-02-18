from PySide2 import QtNetwork
from PySide2.QtCore import QObject, Signal, QDataStream, QIODevice, QByteArray, QFile
from .transaction import Transaction
from .transaction_status_enum import TransactionStatus
from .setup import Setup
import os
from sys import getsizeof


class Sender():
    def __init__(self, socket, file_path, receiver):
        self._socket = socket
        self._transaction = None
        self._receiver = receiver
        self._file_path = file_path
        self._file_name = os.path.split(self._file_path)[1]
        self._file = QFile(self._file_path)
        self._socket.connected.connect(self.send_file)        

    def start(self):
        self._transaction = Transaction(self._file_path, self._file.size(), self._receiver.get_name())
        self._socket.connectToHost(self._receiver.get_ip_address(), Setup().get_port())
        self._socket.waitForConnected(3000)
        print(self._socket.state())

    def send_file(self):
        self._transaction.set_status(TransactionStatus.SENDING)
        file_to_byte_array = QByteArray()
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        
        QFile.open(self._file, QIODevice.ReadOnly)
        stream.writeUInt32(0)
        stream.writeString(self._file_name)
        print("size of name ", getsizeof(self._file_name))
        file_to_byte_array = self._file.readAll()
        data.append(file_to_byte_array)
        self._file.close()

        stream.device().seek(0)
        stream.writeUInt32(data.size() - getsizeof(self._file_name))
        print("total  ", data.size() - getsizeof(self._file_name))

        x = 0
        while(x < data.size()):
            y = self._socket.write(data)
            print("poslato  ", y)
            x += y
            print("x  ", x)
        self._transaction.set_status(TransactionStatus.FINISHED)









