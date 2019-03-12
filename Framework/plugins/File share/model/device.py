from PySide2 import QtNetwork
from PySide2.QtCore import QByteArray, QIODevice, QFile, Signal, QObject
from .setup import Setup
from .receiver import Receiver
from .sender import Sender


class Device():
    def __init__(self):
        self._ip_address = None
        self._name = ""
        self._socket = QtNetwork.QTcpSocket()        
        self._receiver = None
        self._sender = None      

    def set_this_device(self):
        addresses = QtNetwork.QNetworkInterface.allAddresses()
        for address in addresses:
            if not (address.isLinkLocal() or address.isBroadcast() or address.isMulticast() or address.isLoopback() or address.protocol() == QtNetwork.QAbstractSocket.IPv6Protocol):
                self._ip_address = address                
        info = QtNetwork.QHostInfo()
        self._name = info.localHostName()
        self._server = QtNetwork.QTcpServer()
         
        self._server.setSocketDescriptor(self._socket.socketDescriptor()) 
        self._server.listen(self._ip_address, Setup().get_port())
        self._server.newConnection.connect(self.receive)

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
            self._sender = Sender(self._socket, file_path, receiver)
            self._sender.start()

    def receive(self):
        self._socket = self._server.nextPendingConnection()
        self._socket.waitForBytesWritten(3000)
        self._receiver = Receiver(self._socket)
        received_file = self._receiver.start()
        return received_file
