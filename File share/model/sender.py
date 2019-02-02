from PySide2 import QtNetwork
from PySide2.QtCore import QObject, Signal
from .transaction import Transaction
from .setup import Setup


class Sender():
    def __init__(self, socket, file_path, receiver):
        self._socket = socket
        self._transaction = None
        self._receiver = receiver
        self._file_path = file_path
        

    def start(self):
        self._transaction = Transaction(self._file_path, self._receiver, self._socket)
        self._transaction.write_datagram()