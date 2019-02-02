from PySide2 import QtNetwork
from PySide2.QtCore import QByteArray, QIODevice, QFile, Signal
from .setup import Setup
from .receiver import Receiver
from .sender import Sender


class Device():
    def __init__(self):
        self._ip_address = None
        self._name = ""
        self._socket = QtNetwork.QUdpSocket()        
        self._receiver = None
        

    def set_this_device(self):
        adresses = QtNetwork.QNetworkInterface.allAddresses()
        for adress in adresses:
            if adress.isLinkLocal() or adress.isBroadcast() or adress.isMulticast() or adress.isLoopback():
                pass
            else:
                self._ip_address = adress
        info = QtNetwork.QHostInfo()
        self._name = info.localHostName()

        self._socket.bind(Setup().get_port())
        self._socket.readyRead.connect(self.receive_file)
        self._socket.disconnected.connect(self.reset)

    def get_name(self):
        return self._name

    def get_ip_address(self):
        return self._ip_address

    def set_name(self, new_name):
        self._name = new_name

    def set_ip_address(self, new_ip):
        self._ip_address = new_ip

    def send_file(self, file_path, receiver):
        if (file_path is not None) and (receiver is not None):
            sender = Sender(self._socket, file_path, receiver)
            sender.start()

    def receiving(self, file_name):
        return file_name

    def receive_file(self):
        if (self._receiver is None):
            self._receiver = Receiver(self._socket)           
            file_name = self._receiver.read_name_datagram()                        
        else:
            self._receiver.read_data_datagram()

    def reset(self):
        self._receiver = None
        print("disconnected, finished receiving")