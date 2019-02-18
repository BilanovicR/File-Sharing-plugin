from PySide2 import QtNetwork
from PySide2.QtCore import QFile, QByteArray, Signal, QIODevice
from .setup import Setup
from .transaction_status_enum import TransactionStatus
import os


class Transaction():
    def __init__(self, file_path, file_size, other_device):
        self._file_path = file_path
        self._other_device = other_device
        self._file_size = file_size
        self._status = TransactionStatus.WAITING
        self._remaining_bytes = self._file_size
        self._sent_bytes = 0

    def get_sent_bytes(self):
        print(self._sent_bytes)
        return self._sent_bytes

    def set_sent_bytes(self, bytes):
        self._sent_bytes += bytes

    def get_file(self):
        return self._file_path

    def get_other_device(self):
        return self._other_device

    def get_size(self):
        return self._file_size

    def get_status(self):
        return self._status

    def get_remaining_bytes(self):
        return self._remaining_bytes

    def set_file(self, new_file):
        self._file_path = new_file

    def set_other_device(self, new_other):
        self._other_device= new_other

    def set_file_size(self, new_size):
        self._file_size = new_size

    def set_status(self, new_status):
        self._status = new_status

    def set_remaining_bytes(self, now_remaining_bytes):
        self._remaining_bytes = now_remaining_bytes
    